from flask import (Blueprint, render_template, request, 
                   redirect, session)
from functools import wraps
from uuid import uuid4

from helpers.helper_functions import save_pictures, save_choices
from helpers.db_helper import (get_pictures_count,
                               get_labeled_count,
                               get_statistics,
                               get_other_statistics)

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
    total = get_pictures_count()
    labeled = get_labeled_count()
    choice_list = get_statistics()
    other_choice_count = get_other_statistics()
    data = {}
    for choice in choice_list:
        data[choice[0].capitalize()+'s'] = choice[1]
    if other_choice_count > 0:
        data["Others"] = other_choice_count

    return render_template('statistics.html', total=total,
                           labeled=labeled, data=data)
