from . import admin


@admin.route("/", methods=["GET"])
def index_get():
    return ""
