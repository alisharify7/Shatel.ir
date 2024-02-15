from flask import Blueprint

web = Blueprint(
    "web",
    __name__,
    static_folder="static/web/",
    template_folder="templates/web/",
    static_url_path="WebPublicStatic"
)

from . import views
