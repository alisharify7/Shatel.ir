from flask import Blueprint

auth = Blueprint(
    "auth",
    __name__,
    static_folder="static/auth",
    template_folder="templates/auth",
    static_url_path="AuthPublicStatic"
)

from . import views, model
