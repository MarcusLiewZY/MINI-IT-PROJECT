from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, Length


class CreatePostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=120, message="Title must be less than 120 characters"),
        ],
    )
    tags = SelectMultipleField(
        "Tags",
        choices=[],
        validators=[
            DataRequired(),
            Length(
                max=5,
                message="You can select up to 5 tags.",
            ),
            Optional(),
        ],
    )
    content = TextAreaField("Content", validators=[DataRequired()])
    image_url = FileField(
        "Image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg", "gif"],
                message="Only support png, jpg, jpeg, gif files.",
            ),
            Optional(),
        ],
    )

