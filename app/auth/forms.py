from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import User


class AdminRegisterForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email."),
            Length(min=6, max=50),
        ],
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(AdminRegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered.")
            return False
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Passwords must match.")
            return False
        return True
