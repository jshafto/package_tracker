from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from config import Config
from app.shipping_form import ShippingForm
from app.login_form import LoginForm, SignupForm
from flask_migrate import Migrate
from app.models import db, Package, User
from flask_login import login_required, current_user, login_user, logout_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@login_required
def index():
    packages = Package.query.filter_by(user_id=current_user.id).all()
    return render_template('package_status.html', packages=packages)


@app.route('/new_package', methods=['GET', 'POST'])
def new_package():
    form = ShippingForm()
    if form.validate_on_submit():
        print(current_user.id)
        data = form.data
        new_package = Package(sender=data["sender"],
                              recipient=data["recipient"],
                              origin=data["origin"],
                              destination=data["destination"],
                              location=data["origin"],
                              user_id=current_user.id)
        db.session.add(new_package)
        db.session.commit()
        Package.advance_all_locations()
        return redirect('/')
    return render_template('shipping_request.html', form=form)


@app.route("/session", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter(User.username == username).first()
        if not user or not user.check_password(form.password.data):
            return redirect(url_for(".login"))
        login_user(user)
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(
            username=form.username.data).first()
        if existing_user is None:
            user = User(
                username=form.username.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('index'))
        # do something here so users know the username is taken?
    return render_template("signup.html", form=form)


@app.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for('.login'))
