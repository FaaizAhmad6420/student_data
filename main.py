from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap5(app)


class User(db.Model):
    roll_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    Class = db.Column(db.String(1000))
    section = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    Class = StringField("Class", validators=[DataRequired()])
    section = StringField("Section", validators=[DataRequired()])
    submit = SubmitField("Submit!")


class SearchForm(FlaskForm):
    roll_no = StringField("Roll_No", validators=[DataRequired()])
    submit = SubmitField("Submit!")


@app.route('/', methods=["GET", "POST"])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        roll_no = form.roll_no.data
        return redirect(url_for("search", roll_no=roll_no))
    return render_template("index.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            Class=form.Class.data,
            section=form.section.data,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/search/<int:roll_no>', methods=["GET", "POST"])
def search(roll_no):
    user = User.query.filter_by(roll_no=roll_no).first()
    return render_template("search.html", user=user)


@app.route('/update/<int:roll_no>', methods=["GET", "POST"])
def update(roll_no):
    user_to_update = User.query.get_or_404(roll_no)
    edit_form = RegisterForm(
        name=user_to_update.name,
        email=user_to_update.email,
        Class=user_to_update.Class,
        section=user_to_update.section,
    )
    if edit_form.validate_on_submit():
        user_to_update.name = edit_form.name.data
        user_to_update.email = edit_form.email.data
        user_to_update.Class = edit_form.Class.data
        user_to_update.section = edit_form.section.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", form=edit_form)


@app.route('/delete/<int:roll_no>', methods=["GET", "POST"])
def delete(roll_no):
    user_to_delete = User.query.get_or_404(roll_no)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
