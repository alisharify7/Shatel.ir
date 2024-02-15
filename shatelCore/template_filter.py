from flask import url_for

from . import app


@app.template_filter('StorageUrl')
def StorageUrl(path: str):
    """This template filter generate dynamic urls base of app.debug mode for serving via flask or nginx
        if debug mode this filter redirect  users to flask.serve function
        but in production mode this filter redirect users to serve static via nginx
    """

    if app.config.get("DEBUG"):
        return url_for("web.ServeStorageFiles", path=path)  # flask serve
    else:
        return f"/Storage/{path}"  # Nginx Serve Files
