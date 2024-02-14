from . import app
from flask import request


@app.context_processor
def app_context():
    def currentLanguage():
        """
            this template filter returns users current language
        """
        return request.current_language

    def renderLogo():
        return "media/logo/logo.png"

        # if request.current_language in ["ar", "fa"]:
        #     return "media/logo/fa-logo.png"
        # else:
        #     return "media/logo/eng-logo.png"

    ctx = {
        "languages": app.config.get("LANGUAGES"),
        "currentLanguage": currentLanguage,
        "renderLogo": renderLogo,

    }

    return ctx
