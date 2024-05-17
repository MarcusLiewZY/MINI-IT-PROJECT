from flask import render_template
from flask_login import current_user
from app.utils.decorators import login_required
from . import ABOUT_bp

@ABOUT_bp.route('/ABOUT')
@login_required
def ABOUT():
    return render_template('ABOUT/ABOUT.html', user = current_user)