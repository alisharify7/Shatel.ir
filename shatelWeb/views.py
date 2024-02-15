# build in
import os

# framework
from flask import send_from_directory, \
    current_app, render_template

# lib
from flask_babel import lazy_gettext as _l

# app
from . import web, form as WebForm

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
