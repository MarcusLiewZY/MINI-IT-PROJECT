from markupsafe import Markup


def preserve_line_breaks(content):
    return Markup(content.replace("\n", "<br>"))
