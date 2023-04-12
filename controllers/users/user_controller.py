from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user
from models.users import User
from main import app


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        user = User().get_obj('username', username)
        if user and user.authenticated(password):
            if login_user(user, remember=True):
                user.update_activity()
                #handle optionally redirecting to the next URL safely
                next_url = form.next.data
                if next_url:
                    return redirect(safe_next_url(next_url))
                return redirect(url_for('page/dashboard.html'))
            else:
                flash('This account is not active','error')
        else: 
            flash('Login or password is incorrect','error')
    return render_template("page/login.html", form=form)
