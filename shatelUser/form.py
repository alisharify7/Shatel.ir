from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField
from wtforms.validators import Length, DataRequired, InputRequired, Email as EmailValidator, Regexp
from flask_babel import lazy_gettext as _l


class TicketForm(FlaskForm):
    """
    Sending a Ticket Html Form
    """
    Title = StringField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(min=6, max=64,
                   message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-64"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("عنوان تیکت")
        }
    )

    Caption = TextAreaField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(min=6, max=512,
                   message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-512"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("توضیحات"),
            "rows": '10',
            "cols": '10'
        }
    )

    Submit = SubmitField(
        render_kw={
            "value": _l('ثبت'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0 fs-4"
        }
    )


class Setting(FlaskForm):
    """
    Sending a Ticket Html Form
    """
    FirstName = StringField(
        validators=[
            # DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # Length(min=6, max=256,
            #        message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-64"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("نام")
        }
    )

    LastName = StringField(
        validators=[
            # DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # Length(min=6, max=64,
            #        message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-64"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("نام خانوادگی"),
        }
    )
    Username = StringField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(min=6, max=128,
                   message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-64"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("نام کاربری"),
        }
    )
    Password = PasswordField(
        validators=[
            # DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # Length(min=6, max=256,
            #        message=_l('حداقل و حداکثر طول داده در این فیلد %(length)s می باشد', length="6-64"))
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("گذرواژه"),
        }
    )

    Email = EmailField(
        validators=[
            EmailValidator(message=_l("ایمیل وارد شده نامعتبر می باشد")),
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("آدرس ایمیل"),
        }
    )

    Address = TextAreaField(
        validators=[
            # DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("آدرس منزل"),
            "rows": 10,
            "cols": 20
        }
    )
    PhoneNumber = StringField(
        validators=[
            Regexp(regex=r"^((0|0098|\+98)?9\d{9})?$", message=_l("فرمت وارد شده برای تلفن نامعتبر می باشد")),
            # DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            # InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": _l("شماره تلفن همراه"),
        }
    )

    Submit = SubmitField(
        render_kw={
            "value": _l('آپدیت'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0 fs-4"
        }
    )
