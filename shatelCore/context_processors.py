from flask import request, current_app
from shatelWeb.form import NewsLetterForm


def contexts():
    def currentLanguage():
        """
            this template filter returns users current language
        """
        return request.current_language

    def getnewsLetterForm():
        """this context return a newsletter form"""
        return NewsLetterForm()


    def renderLogo():
        return "media/logo/logo.png"

        # if request.current_language in ["ar", "fa"]:
        #     return "media/logo/fa-logo.png"
        # else:
        #     return "media/logo/eng-logo.png"

    ctx = {
        "languages": current_app.config.get("LANGUAGES"),
        "currentLanguage": currentLanguage,
        "renderLogo": renderLogo,
        "newsLetterForm": getnewsLetterForm,

    }

    return ctx
