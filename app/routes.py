from flask import (Blueprint, render_template, request, 
                   redirect, session)
from functools import wraps
from uuid import uuid4

from helpers.helper_functions import save_pictures, save_choices
from helpers.db_helper import (_get_pictures_count,
                               _get_labeled_count,
                               _get_statistics)

bp = Blueprint('routes', __name__)

# Initialize admin credentials with hardcoded values.
admin_login, admin_password = 'admin', 'admin'


def signin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' == session.get("name"):
            return f(*args, **kwargs)
        else:
            return redirect('/signin')
    return wrap


@bp.route('/', methods=["GET", "POST"])
def home():
    return redirect('/admin')


@bp.route('/signin', methods=["GET", "POST"])
def main():
    session.clear()
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login == admin_login and password == admin_password:
            session["name"] = "logged_in"
            return redirect('/admin')
    return render_template('signin.html')


@bp.route("/admin", methods=["GET", "POST"])
@signin_required
def admin():
    if request.method == "POST":
        choises = request.form.get("choises")
        uuid = str(uuid4())
        files = request.files.getlist('file')
        save_pictures(files, uuid)
        save_choices(choises, uuid)
    return render_template('admin.html')


@bp.route("/statistics")
@signin_required
def statistics():
    if request.method == "POST":
        return redirect('/main')
    total = _get_pictures_count()
    labeled = _get_labeled_count()
    choice_list = _get_statistics()

    data = {}
    for choice in choice_list:
        data[choice[1].capitalize()+'s'] = choice[0]

    return render_template('statistics.html', total=total,
                           labeled=labeled, data=data)
