# build in
import os

# framework
from flask import send_from_directory, \
    current_app, render_template, redirect, flash, request, url_for

# lib
from flask_babel import lazy_gettext as _l

# app
from . import web, form as WebForm
from . import utils as WebUtils

@web.get("/StorageFiles/<path:path>/")
def ServeStorageFiles(path: os.path):
    """ This view only serve files for development only!!"""
    if current_app.config.get("DEBUG") and os.path.exists(current_app.config.get("STORAGE_DIR") / path):
        return send_from_directory(current_app.config.get("STORAGE_DIR"), path)
    else:
        return "404", 404


@web.route("/", methods=["GET"])
def index_get():
    """
    This View return main index page of the site
    """
    return render_template("index.html")


@web.route("/about-us/", methods=["GET"])
def about_us_get():
    """
    This View return About us page of the site
    """
    return render_template("pages/about-us.html")


@web.route("/logo/", methods=["GET"])
def logo_get():
    """
    this View return Logo page of the Site
    """
    return render_template("pages/logos.html")


@web.route("/faq/", methods=["GET"])
def faq_get():
    """
    this View return faq page
    """
    faq_questions = [{"question": _l("آیا امکان خرید مستقیم از شاتل وجود دارد؟"),
                      "answer": _l("آیا امکان خرید مستقیم از شاتل وجود دارد؟")} for i in range(20)]
    # TODO: read faq from db
    return render_template("pages/faq.html", question=faq_questions)


@web.route("/contact-us/", methods=["GET"])
def contact_us_get():
    """
    this View return faq page
    """
    return render_template("pages/contact-us.html")


@web.route("/job/", methods=["GET"])
def job_get():
    """
    this View return jon offers page
    """
    return render_template("pages/job-hire.html")


@web.route("/representatives/", methods=["GET"])
def proxy_get():
    """
    this View return proxy state page
    """
    return render_template("pages/proxies.html")


@web.route("/warranty-validation/", methods=["GET"])
def warranty_validation_get():
    """
    this View return proxy state page
    """
    form = WebForm.ValidateVarrantyForm()
    return render_template("pages/warranty-validation.html", form=form)




@web.route("/register/newsletter/", methods=["POST"])
def register_news_letter_post():
    """
    register new user in newsletter
    """
    if not current_app.extensions['captcha3'].is_verify():
        flash("کپچا به درستی وارد نشده است", "danger")
        return redirect(request.referrer)

    form = WebForm.NewsLetterForm()
    if not form.validate():
        flash("برخی موارد به درستی وارد نشده اند", "danger")
        return redirect(request.referrer)

    query = db.session.query(WebModel.NewsLetter).filter_by(Email=form.Email.data)
    if db.session.execute(query).scalar_one_or_none():
        flash("آدرس ایمیل در خبرنامه عضو می باشد.", "danger")
        return redirect(request.referrer)

    if WebUtils.redis_exists_newsletter_mail(email=form.Email.data):
        ttl = WebUtils.redis_ttl_newsletter_mail(email=form.Email.data)
        flash("ایمیل تایید عضویت در خبرنامه برای کاربر ارسال شده است", "danger")
        flash(f"میتوانید پس از {ttl} دقیقه دوباره اقدام کنید", "danger")
        return redirect(request.referrer)

    token = WebUtils.generate_newsletter_confirm_token()
    WebUtils.redis_set_newsletter_token(email=form.Email.data, newsletter_token=token)

    sendNewsLetterMail(
        context={"token": token},
        recipients=[form.Email.data],
        async_celery=True
    )

    flash("ایمیل مورد با موفقیت در صف عضویت خبرنامه قرار گرفت", "danger")
    flash("لطفا جهت تایید عضویت صندوق ورودی ایمیل خود را چک کنید", "danger")
    return redirect(request.referrer)


@web.route("/confirm/newsletter/<string:token>", methods=["GET"])
def confirm_news_letter_get(token):
    UserEmail = WebUtils.redis_get_newsletter_token(newsletter_token=token)
    if not UserEmail:
        abort(404)


    newsLetter = WebModel.NewsLetter()
    if not newsLetter.setEmail(UserEmail):
        flash("آدرس ایمیل در خبرنامه عضو می باشد.", "danger")
        return redirect(url_for('web.index_get'))

    newsLetter.SetPublicKey()
    if not newsLetter.save():
        flash("خطایی رخ داد. بعدا امتحان کنید", "danger")
        return redirect(url_for('web.index_get'))

    WebUtils.redis_delete_newsletter_token_email(newsletter_token=token, email=UserEmail)
    flash("ایمیل با موفقیت عضو خبرنامه شد", "danger")
    return redirect(url_for('web.index_get'))