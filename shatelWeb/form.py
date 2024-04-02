from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, InputRequired, Length, Email as EmailValidator


class ValidateVarrantyForm(FlaskForm):
    """Login Users Form"""
    ProductNumber = StringField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=4,
                max=128,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="4-128")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": "IB-MM-000000000000000000000",
            "dir": "ltr",
            "id": "ProductNumber"
        }
    )

    Submit = SubmitField(
        render_kw={
            "value": _l('اعتبار سنجی'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0",
            "id": "submitBtn"
        }
    )




class NewsLetterForm(FlaskForm):
    Email = EmailField(
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی می باشد"),
            InputRequired(message="ورود داده در این فیلد الزامی می باشد"),
            EmailValidator(message="ایمیل وارد شده نامعتبر می باشد")],
        render_kw={
            "class": "form-control rounded-0 rounded-start text-start",
            "placeholder": _l("آدرس ایمیل")
        }

    )
    Submit = SubmitField(
        render_kw={
            "value": _l("عضویت"),
            "class":"btn bg-orange text-white input-group-text rounded-0 rounded-end"
        }
    )

