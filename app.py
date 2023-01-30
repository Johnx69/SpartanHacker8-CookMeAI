from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, PostForm, PasswordForm, UserForm, SearchForm, LocationForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from output import output
import googlemaps
import re
from statistics import mean
from operator import itemgetter

api_key = 'AIzaSyA8PNVoxVIPapjZNxqzJWISAOvenn4YhwA'

# Initial application
app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/'
# Config for application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "Hello"

# Setup database
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

# Ckeditor
ckeditor = CKEditor(app)

# Define for login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Define for search in navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Index page


@app.route('/')
def index():
    return render_template('index.html')

# Login Page


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("That user doesn't exist! Try again")
        else:
            flash('Wrong password - Try again!')
    return render_template('login.html', form=form)

# Logout page


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

########### User route ###########
# Register (Add user)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hash_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
                         password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash = ''
        flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

# Update User


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
        except:
            db.session.commit()
            flash("Error! Looks like there was an problem,")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)

# Create search user


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        # Query database
        posts = posts.filter(Posts.content.like(f'%{ post.searched }%'))
        posts = posts.order_by(Posts.title).all()

        return render_template('search.html', form=form, searched=post.searched, posts=posts)

######## Posts ############
# DashBoard page


@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']

        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']
            # Save the images
            # Grab Image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            name_to_update.profile_pic.save(os.path.join(
                app.config['UPLOAD_FOLDER'], pic_name))
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)
            except:
                db.session.commit()
                flash("Error! Looks like there was an problem,")
                return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)
        else:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)
    return render_template('dashboard.html')

# Single Post Page


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id or id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Return a message
            flash('Blog Post was deleted')
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
        except:
            flash("There was a problem deleting post. Try again!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
    else:
        flash("You aren't authorized to delete the post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# All Posts Edit Pages


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = post.slug
        post.content = form.content.data

        # Update database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:

        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content

        return render_template('edit_post.html', form=form)
    else:
        flash("You aren't authorized to edit the post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)

# All Post Page


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template('posts.html', posts=posts)

# Add Post Page


@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster,
                     slug=form.slug.data)

        # Clear the form
        form.title.data = ''
        form.content.date = ''
        form.slug.data = ''

        # add to db
        db.session.add(post)
        db.session.commit()

        flash("Blog post submitted Successfully!")

        # Redirect to the webpage
    return render_template('add_post.html', form=form)

# Delete Post Page


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        name = None
        form = UserForm()
        user_to_delete = Users.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User delete Successfully!')
            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form=form, name=name, our_users=our_users)
        except:
            flash("There was a problem deleting user. Try again!")
            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form=form, name=name, our_users=our_users)
    else:
        flash("Sorry, you can't delete that user")
        return redirect(url_for('dashboard'))

######## About us ########


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
######### AI #############


@app.route('/img2ing', methods=['GET'])
def img2ing():
    return render_template('img2ing.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/img2ing', methods=['POST', 'GET'])
def predict():
    imagefile = request.files['imagefile']
    image_path = os.path.join(
        app.root_path, 'static/images/user_images', imagefile.filename)
    imagefile.save(image_path)
    img = "/images/demo_imgs/"+imagefile.filename
    title, ingredients, recipe = output(image_path)
    return render_template('predict.html', title=title, ingredients=ingredients, recipe=recipe, img=img)


########### eat2gether ##########
@app.route('/eat2gether', methods=['GET', 'POST'])
def eat2gether():
    result_locations = None
    form = LocationForm()
    if form.validate_on_submit():
        origins = request.form['location'].split(',')
        result_locations = process(origins)

    return render_template('eat2gether.html', form=form, result_locations=result_locations)


def process(origins):

    gmaps = googlemaps.Client(api_key)

    # Mode of transportation
    mode = "walking"

    # Get distance and duration
    destinations = ['BRODY SQUARE', 'LANDON HALL MSU', 'HOLDEN DINING HALL', 'HOLMES DINING HALL MSU', 'SOUTH POINTE AT CASE', 'THE EDGE AT AKERS', 'THE GALLERY AT SYNDER PHILLIPS', 'THE VISTA AT SHAW', 'THRIVE AT OWEN',
                    'MSU INTERNATIONAL CENTER', 'MSU UNION', 'HUBBARD HALL MSU', 'WONDERS HALL MSU', 'HANNAH ADMIN BUILDING MSU', 'MCDONEL HALL MSU', '1855 PLACE MSU', 'KELLOGG CENTER MSU', 'MINSKOFF PAVILION', 'WELLS HALL', 'MSU BAKERS']

    result = gmaps.distance_matrix(origins, destinations, mode)

    dist_dict = {}

    for m in range(len(destinations)):
        dist_dict[destinations[m]] = []

    for k in range(len(destinations)):
        for j in range(len(origins)):
            dist_dict[destinations[k]].append(
                result['rows'][j]['elements'][k]['duration']['text'])
            dist_dict[destinations[k]][j] = int(
                re.sub("[^0-9]", "", dist_dict[destinations[k]][j]))

    mean_dict = {}

    for l in range(len(destinations)):
        mean_dict[destinations[l]] = int(mean(dist_dict[destinations[l]]))

    resultList = list(mean_dict.items())
    resultList.sort(key=itemgetter(1))
    result_locations = []
    for index in range(0, 5):
        item = resultList[index]
        item = list(item)
        result_locations.append(item)
    return result_locations

#  Error page


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

######### Models ##########


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    about_author = db.Column(db.Text(500), nullable=True)
    profile_pic = db.Column(db.String(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Password
    password_hash = db.Column(db.String(128))

    # User can have many post
    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    # Create a representation

    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign key to link users
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


if __name__ == '__main__':
    app.run(debug=True)
