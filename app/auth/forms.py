from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app import bcrypt
from app.models import User


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False

        # if the user mail is not end with mmu.edu.my
        if not self.email.data.endswith("mmu.edu.my"):
            self.email.errors.append("Please use your MMU email to sign up")
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append("Email already registered, sign in instead")
            return False

        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate(self, extra_validators=None):
        initial_validation = super(LoginForm, self).validate(extra_validators)

        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if not user:
            self.email.errors.append("Invalid email")
            return False

        if bcrypt.check_password_hash(user.password, self.password.data) == False:
            self.password.errors.append("Invalid password")
            return False

        return True


class ForgotPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])

    def validate(self, extra_validators=None):
        initial_validation = super(ForgotPasswordForm, self).validate(extra_validators)

        if not initial_validation:
            return False

        user = User.query.filter(User.email == self.email.data).first()

        if not user:
            self.email.errors.append("Email not found")
            return False

        return True


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(ResetPasswordForm, self).validate(extra_validators)

        if not initial_validation:
            return False

        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False

        return True


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
