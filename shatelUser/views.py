import os

from flask import (render_template, send_from_directory, jsonify,
                   request, flash, redirect, current_app, session, url_for)
from flask_babel import lazy_gettext as _l, format_datetime

from shatelAuth.Access.decorator import login_required
from shatelCore.extensions import db
from shatelAuth.model import Ticket
from shatelCore.extensions import ServerCaptcha2

from . import user
from . import form as UserForm


@user.route("/UserStatic/<path:filename>", methods=["GET"])
@login_required
def Serve(filename):
    """
        Serve Static file only to users that logged in to their account
    """
    static = current_app.config.get("BASE_DIR") / "shatelUser" / "private_static"
    if os.path.exists(os.path.join(static, filename)):
        return send_from_directory(static, filename)
    else:
        return "File Not Founded", 404


@user.route("/", methods=["GET"])
@login_required
def user_index():
    ctx = {
        "dashboard": "active"
    }
    return render_template("user/index.html", ctx=ctx)


@user.route("/send-ticket/", methods=["GET"])
@login_required
def send_ticket_get():
    ctx = {
        "send_ticket": "active"
    }
    form = UserForm.TicketForm()
    return render_template("user/send-ticket.html", ctx=ctx, form=form)


@user.route("/send-ticket/", methods=["POST"])
@login_required
def send_ticket_post():
    ctx = {
        "send_ticket": "active"
    }

    form = UserForm.TicketForm()

    if not ServerCaptcha2.is_verify():
        flash(_l('کپچا به درستی وارد نشده است'), "danger")
        return render_template("user/send-ticket.html", ctx=ctx, form=form)

    if not form.validate():
        flash(_l('برخی موارد به درستی وارد نشده است'), "danger")
        current_app.logger.info(
            msg=f"\nError for User: {request.user_object.getName(True)}\nForm Validate Error.\n\t{form.errors}\n")
        return render_template("user/send-ticket.html", ctx=ctx, form=form)

    ticket = Ticket()
    ticket.Title = form.Title.data
    ticket.Caption = form.Caption.data
    ticket.SetPublicKey()
    ticket.setUserID(request.user_object)

    try:
        db.session.add(ticket)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"\nError for User: {request.user_object.getName(True)}\n\tError: {e}")
        current_app.log_exception(exc_info=e)
        print(e)
        db.session.rollback()
        flash(_l("خطایی رخ داد!"), "danger")
        return redirect(request.referrer)
    else:
        flash(_l("عملیات با موفقیت انجام شد"), "success")
        return redirect(url_for('user.history_tickets_get'))


@user.route("/history-ticket/", methods=["GET"])
@login_required
def history_tickets_get():
    """
        This View return users all tickets
    """
    ctx = {
        "history_ticket": "active"
    }

    page = request.args.get(key="page", default=1, type=int)
    ctx["tickets"] = db.paginate(max_per_page=15, per_page=10, page=page,
                                 select=db.select(Ticket).filter(Ticket.UserID == request.user_object.id).order_by(
                                     Ticket.CreatedTime.desc())
                                 )
    ctx["current_page"] = page
    return render_template("user/history-tickets.html", ctx=ctx)


@user.route("/ticket-info/", methods=["POST"])
@login_required
def ticket_info_post():
    """
    this view take a post request PublicKey for each
    """
    ctx = {}
    ticketID = request.form.get("TICKET_ID", None)
    if not ticketID:
        return jsonify(
            {"status": "failed", "message": _l('برخی مقادیر به نظر گم شده اند!') + "TICKET_ID:string:missing"}), 400

    ticket = db.session.execute(db.select(Ticket).filter_by(PublicKey=ticketID).filter_by(
        UserID=request.user_object.id)).scalar_one_or_none()
    if not ticket:
        return jsonify({"status": "failed", "message": _l('تیکتی با شماره وارد شده یافت نشد')}), 404

    data = {
        "ticket_number": ticket.id,
        "title": ticket.Title,
        "message": ticket.Caption,
        "created_at": format_datetime(ticket.CreatedTime),
        "answer": ticket.Answer or None,
        "answer_error": _l("پاسخی به تیکت مورد نظر داده نشده است")
    }

    return jsonify({"status": "success", "message": data}), 200


@user.route("/setting/", methods=["GET"])
@login_required
def setting_get():
    """
    """
    ctx = {
        "setting": "active"
    }
    form = UserForm.Setting()

    form.Username.data = request.user_object.Username
    form.FirstName.data = request.user_object.FirstName or None
    form.LastName.data = request.user_object.LastName or None
    form.Email.data = request.user_object.Email or None
    form.Address.data = request.user_object.Address or None
    form.PhoneNumber.data = request.user_object.PhoneNumber or None

    return render_template("user/setting.html", ctx=ctx, form=form)


@user.route("/setting/", methods=["POST"])
@login_required
def setting_post():
    """
    """
    ctx = {
        "setting": "active"
    }
    form = UserForm.Setting()
    if not form.validate():
        flash(_l("برخی مقادیر مقدار دهی نشده اند"), "danger")
        current_app.logger.error(form.errors)
        return render_template("user/setting.html", ctx=ctx, form=form)

    user = request.user_object
    if form.Password.data:
        if len(form.Password.data) >= 6:
            user.setPassword(form.Password.data)
        else:
            form.Password.errors.append(_l("حداقل طول گذرواژه باید 6 کاراکتر باشد"))
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.Username.data and not (form.Username.data == user.Username):
        if not user.setUsername(form.Username.data):
            form.Username.errors.append(_l("نام کاربری توسط کاربر دیگری گرفته شده است"))
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.Address.data:
        user.Address = form.Address.data

    if form.Email.data and not (form.Email.data == user.Email):
        if not user.setEmail(form.Email.data):
            form.Email.errors.append(_l("آدرس ایمیل توسط کاربر دیگری گرفته شده است"))
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.PhoneNumber.data and not (form.PhoneNumber.data == user.PhoneNumber):
        if not user.setPhonenumber(form.PhoneNumber.data):
            form.PhoneNumber.errors.append(_l("شماره تلفن همراه توسط کاربر دیگری گرفته شده است"))
            return render_template("user/setting.html", ctx=ctx, form=form)

    user.FirstName = form.FirstName.data
    user.LastName = form.LastName.data

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(msg=e)
        current_app.log_exception(exc_info=e)
        db.session.rollback()
        flash(_l("خطایی رخ داد بعدا امتحان کنید"), "danger")
    else:
        session["password"] = user.Password
        flash(_l("عملیات با موفقیت انجام شد"), "success")

    return render_template("user/setting.html", ctx=ctx, form=form)
