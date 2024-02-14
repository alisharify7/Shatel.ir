# build in
from urllib.parse import urlparse as url_parse

# app
from . import auth
from . import form as AuthForm
from . import model as AuthModel
from . import utils as AuthUtils

# framework
from flask import render_template, session, \
    abort, url_for, redirect, flash, jsonify, \
    get_flashed_messages, request, current_app
from flask_babel import lazy_gettext as _l
from sqlalchemy.exc import SQLAlchemyError

# app
from shatelCore.extensions import ServerCaptcha2
from shatelCore.email import sendActivAccounteMail, sendResetPasswordMail
from shatelCore.extensions import RedisServer, db
from shatelConfig import Setting
from shatelAdmin.model import Admin
from .Access import only_reset_password


@auth.route("/login/", methods=["GET"])
def login_get():
    """
    This View return login page for user
    """
    form = AuthForm.LoginForm()
    return render_template("login.html", form=form)


@auth.route("/login/", methods=["POST"])
def login_post():
    """
    this view take a post request for check user credential
    """
    form = AuthForm.LoginForm()
    if not form.validate():
        flash(_l("برخی موارد مقداردهی نشده اند"), "danger")
        return render_template("login.html", form=form)

    next_page = request.args.get("next", False)
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("user.user_index")

    username, password = form.Username.data, form.Password.data
    if not (user := AuthModel.User.query.filter_by(Username=username).first()):
        flash(_l("کاربری با مشخصات وارد شده یافت نشد"), "danger")
        return render_template("login.html", form=form)
    else:
        if not user.checkPassword(password):
            flash(_l("اعتبارسنجی نادرست می باشد"), "danger")
            return render_template("login.html", form=form)
        if not user.Active:
            flash(_l("حساب کاربری مورد نظر فعال نمی باشد"), "danger")
            return render_template("login.html", form=form)

        else:
            # this function login user to its account
            session["login"] = True
            session["account-id"] = user.id
            session["password"] = user.Password
            session.permanent = True # SET session lifetime


    return redirect(next_page)


@auth.route("/register/", methods=["GET"])
def register_get():
    """
        This View return Register template for user
    """
    form = AuthForm.RegisterForm()
    return render_template("register.html", form=form)


@auth.route("/register/", methods=["POST"])
def register_post():
    """
    this view take a post request that contain users information for register a new account
    """
    form = AuthForm.RegisterForm()
    if not form.validate():
        return render_template("register.html", form=form)

    if not ServerCaptcha2.is_verify():
        form.Submit.errors = [_l('کپچا به درستی وارد نشده است')]
        return render_template("register.html", form=form)

    User = AuthModel.User()
    if (user := AuthModel.User.query.filter_by(Email=form.EmailAddress.data).first()):
        if user.Active:
            form.Submit.errors = [_l('آدرس ایمیل توسط کاربر دیگری گرفته شده است')]
            return render_template("register.html", form=form)
        else:
            # check if someone else is waiting for an email validation
            key = f"ActiveEmail:{form.EmailAddress.data}"
            if RedisServer.get(key):
                form.EmailAddress.errors = [_l("لطفا دقایقی دیگر دوباره امتحان کنید ...")]
                return render_template("register.html", form=form)
            else:
                try:
                    db.session.delete(user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(e)
                    flash(_l('خطایی رخ داد, بعدا امتحان کنید'), "danger")
                    return render_template("register.html", form=form)

    if not User.setUsername(form.Username.data):
        form.Username.errors = [_l("نام کاربری توسط کاربر دیگری گرفته شده است")]
        return render_template("register.html", form=form)

    if not User.setEmail(form.EmailAddress.data):
        form.EmailAddress.errors = [_l("آدرس ایمیل توسط کاربر دیگری گرفته شده است")]
        return render_template("register.html", form=form)

    User.SetPublicKey()
    User.setPassword(form.Password.data)
    try:
        db.session.add(User)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        form.Submit.errors = [_l('خطایی رخ داد بعدا امتحان کنید')]
        return render_template("register.html", form=form)

    else:
        if not (slug := AuthUtils.gen_and_set_activation_slug(email=form.EmailAddress.data)):
            form.EmailAddress.errors = [_l("لطفا دقایقی دیگر دوباره امتحان کنید ...")]
            return render_template("register.html", form=form)

        sendActivAccounteMail(
            context={"token": slug},
            recipients=[str(form.EmailAddress.data)],
            async_thread=False,  # not recommended but just for now !
            async_celery=True,
        )
        return render_template("register.html", showSendActiveMail=True, form=form)


@auth.route("/Active/<string:token>/")
def active_account(token: str):
    """
    This View Activate User Account

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    this view take user unique activator key (uuid) and then validate 
    that key and in the end activate user's account
    """

    resultEmail = RedisServer.get(name=f"ActivateAccountToken:{token}")
    if not resultEmail:
        abort(404)
    if not resultEmail:
        abort(404)
    resultEmail = str(resultEmail.decode("utf-8"))

    User = AuthModel.User.query.filter_by(Email=resultEmail).first_or_404()
    if User.Active:
        abort(404)
    else:

        # set users new language
        language = request.args.get("language", "en")  # get user language from args(GET)
        if language in current_app.config.get("LANGUAGES", list()):
            session['language'] = language

        User.Active = True
        try:
            db.session.add(User)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash(_l("خطایی هنگام پردازش درخواست رخ داد. دوباره امتحان کنید"), "success")
            return redirect(url_for('auth.login_get'))
        else:
            RedisServer.delete(f"ActivateAccountToken:{token}")
            flash(_l("عملیات با موفقیت انجام شد"), "success")
            return redirect(url_for('auth.login_get'))


@auth.get("/get/notifications/")
def get_notification():
    """Notification Messages view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This view return user all flash messages in a json
    

    arguments:
        None -- clear

    return:
        return all flash messages in a json format 
    """
    flashes = []
    messages = get_flashed_messages(with_categories=True)

    for category, message in messages:
        temp = {"message": message, "category": category}
        flashes.append(temp)
    return jsonify(flashes)


@auth.route("/forget_password/", methods=["GET"])
def forget_password_get():
    """
    this view return a  html page for users for Reset Password of  there accounts
    """
    ctx = {}
    form = AuthForm.ForgetPasswordForm()
    return render_template("forget_password.html", form=form, ctx=ctx)


@auth.route("/forget_password/", methods=["POST"])
def reset_password_post():
    """
    this view take a post request and check if users email is valid send a reset password to users mail account
    """

    ctx = {}
    form = AuthForm.ForgetPasswordForm()

    if not ServerCaptcha2.is_verify():
        flash(_l("کپچا به درستی وارد نشده است"), "danger")
        return render_template("forget_password.html", form=form, ctx=ctx)

    if not form.validate():
        return render_template("forget_password.html", form=form, ctx=ctx)

    if not (
            user := db.session.execute(
                db.select(AuthModel.User).filter_by(Email=form.EmailAddress.data)).scalar_one_or_none()):
        form.EmailAddress.errors.append(_l("کاربری با آدرس ایمیل وارد شده یافت نشد"))
        return render_template("forget_password.html", form=form, ctx=ctx)

    resetCounterSlug = "ResetPasswordAccountCounter:"
    if (lastToken := RedisServer.get(
            f"lastRestToken:{user.Email}")):  # if here is an old token for reset password and its valid delete that
        RedisServer.delete(f"ResetPasswordToken:{str(lastToken.decode('utf-8'))}")

    if not (previousResetCounter := RedisServer.get(name=f"{resetCounterSlug}{user.Email}")):
        RedisServer.set(name=f"{resetCounterSlug}{user.Email}", value=1, ex=3600)  # 3600 in second mean 1 day
    else:
        previousResetCounter = int(str(previousResetCounter.decode('utf-8')))
        if previousResetCounter >= 10:
            flash(_l('کاربر گرامی در یک روز تنها 10 بار میتوانید درخواست بازنشانی گذرواژه دهید'), "danger")
            return redirect(request.referrer)
        else:
            previousResetCounter += 1
            RedisServer.set(name=f"{resetCounterSlug}{user.Email}", value=previousResetCounter,
                            ex=RedisServer.ttl(name=f"{resetCounterSlug}{user.Email}") or 60)

    if not (token := AuthUtils.gen_and_set_reset_slug(email=user.Email)):
        form.EmailAddress.errors.append(_l("خطایی رخ داد"))
        return render_template("forget_password.html", form=form, ctx=ctx)

    sendResetPasswordMail(
        context={"token": token},
        recipients=[str(user.Email)],
        async_thread=False,  # not recommended but just for now !
        async_celery=True,
    )

    ctx["ResetPasswordMail"] = True
    return render_template("forget_password.html", form=form, ctx=ctx)


@auth.route("/check-reset-password/<string:token>", methods=["GET"])
def check_reset_password(token: str):
    """
    this view check reset password in url get params and if its valid
    redirect user to set password page
    """
    language = request.args.get("language", "en")  # get user language from args(GET)
    if language in current_app.config.get("LANGUAGES", list()):
        session['language'] = language

    if not (UserEmail := RedisServer.get(name=f"ResetPasswordToken:{token}")):
        abort(404)

    UserEmail = str(UserEmail.decode('utf-8'))
    if not (lastToken := RedisServer.get(name=f"lastRestToken:{UserEmail}")):
        abort(404)

    lastToken = str(lastToken.decode('utf-8'))
    if lastToken != token:
        abort(404)
    else:
        session["allow-set-password"] = True
        session["mail"] = UserEmail
        session["token"] = f"ResetPasswordToken:{token}"
        session["raw-token"] = token
        return redirect(url_for('auth.set_password_get'))


@auth.route("/set-password/", methods=["GET"])
@only_reset_password
def set_password_get():
    form = AuthForm.SetNewPasswordForm()
    form.Token.data = session["token"]
    return render_template("set_password.html", form=form)


@auth.route("/set-password/", methods=["POST"])
@only_reset_password
def set_password_post():
    form = AuthForm.SetNewPasswordForm()

    if not form.validate():
        return render_template("set_password.html", form=form)

    token = RedisServer.get(form.Token.data)
    if not token:
        abort(404)

    userEmail = str(token.decode('utf-8'))
    if not (user := db.session.execute(db.select(AuthModel.User).filter_by(Email=userEmail)).scalar_one_or_none()):
        abort(404)

    user.setPassword(form.Password.data)
    RedisServer.delete(form.Token.data)
    RedisServer.delete(f"lastRestToken:{session.get('raw-token', None)}")

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.exception(exc_info=e)
        db.session.rollback()
        flash(_l('خطایی رخ داد'), "danger")
    else:
        flash(_l('عملیات با موفقیت انجام شد'), "success")

    return redirect(url_for('auth.login_get'))



@auth.route("/logout/", methods=["GET"])
def logout():
    """
    logout view
    """
    lang = session.get("language", "fa")
    session.clear()
    session["language"] = lang
    flash(_l("با موفقیت از حساب کاربری خود خارج شدید"), "success")
    return redirect(url_for("web.index_get"))


@auth.route(f"/login/admin/{Setting.ADMIN_LOGIN_TOKEN}/", methods=["GET"])
def admin_logout_get():
    """
    admin special logout view
    """
    form = AuthForm.LoginForm()
    form.remote_address = request.headers.get("X-Real-Ip", "null")
    form.device_info = request.headers.get("Sec-Ch-Ua-Platform", "null")
    return render_template("admin/admin_login.html", form=form)


@auth.route(f"/login/admin/{Setting.ADMIN_LOGIN_TOKEN}/", methods=["POST"])
def admin_login_post():
    """
    admin special login view
    """
    form = AuthForm.LoginForm()
    if not ServerCaptcha2.is_verify():
        flash(_l('کپچا به درستی وارد نشده است'), "danger")
        return render_template("admin/admin_login.html", form=form)

    if not form.validate():
        flash(_l('برخی موارد به نظر گم شده اند'), "danger")
        return render_template("admin/admin_login.html", form=form)

    admin_db: Admin = db.session.execute(db.select(Admin).filter_by(Username=form.Username.data)).scalar_one_or_none()
    if not admin_db or admin_db.checkPassword(form.Password.data):  # check username and password
        flash(_l('اعتبارسنحی ناموفق بود'), "danger")
        return render_template("admin/admin_login.html", form=form)

    if not admin_db.allowToLogin():
        flash(_l('حساب کاربری توسط سیستم به صورت خودکار قفل گردیده است'), "danger")
        return render_template("admin/admin_login.html", form=form)

    admin_db.TryNumber += 1
    admin_db.setLog(ip=request.real_ip)
    admin_db.save()


    return redirect(url_for('admin.index_get'))
