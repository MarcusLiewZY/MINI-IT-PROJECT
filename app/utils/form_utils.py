from wtforms import SubmitField
from wtforms.widgets import html_params
from markupsafe import Markup


class SubmitButtonWidget:
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        return Markup(
            '<button type="submit" %s>%s</button>'
            % (html_params(name=field.name, **kwargs), field.label.text)
        )


class SubmitButtonField(SubmitField):
    widget = SubmitButtonWidget()
