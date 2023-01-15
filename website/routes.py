from website import app, db, bcrypt, basic_auth
from sqlalchemy import func
from flask import render_template, request, redirect, url_for, session, g, flash

from flask_login import login_user, current_user, logout_user
from werkzeug.urls import url_parse
from website.forms import LoginForm, RegistrationForm, QuestionForm
from website.models import User, Questions


@app.before_request
def before_request():
    g.user = None

    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        g.user = user


@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(
                    user.password, form.password.data
                ):
                    flash(f"Either username or password incorrect.  ", "inv-cred")
                    return redirect(url_for("login"))
        session['user_id'] = user.id
        session['marks'] = 0
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode(
            "UTF-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hash_password
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    if g.user:
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/question/<int:id>", methods=["GET", "POST"])
def question(id):
    form = QuestionForm()
    q = Questions.query.filter_by(q_id=id).first()
    if not q:
        return redirect(url_for("score"))
    if not g.user:
        return redirect(url_for("login"))
    if request.method == "POST":
        option = request.form["options"]
        if option == q.ans:
            session["marks"] += 10
        return redirect(url_for("question", id=(id + 1)))
    form.options.choices = [(q.a, q.a), (q.b, q.b), (q.c, q.c), (q.d, q.d)]
    return render_template(
        "question.html", form=form, q=q, title="Question {}".format(id)
    )


@app.route("/score")
def score():
    if not g.user:
        return redirect(url_for("login"))
    g.user.marks = session["marks"]
    hs = db.session.query(func.max(User.marks)).scalar()
    print(type(hs))

    huser = User.query.filter_by(marks=hs).first()
    # db.session.commit()
    return render_template("score.html", hs=huser, title="Final Score")


@app.route("/logout")
def logout():
    if not g.user:
        return redirect(url_for("login"))
    session.pop("user_id", None)
    session.pop("marks", None)
    return redirect(url_for("home"))
