from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=10)
    templates = render_template("home.html", useri = current_user, posts=posts)
    return templates


@views.route("/createpost", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            flash("Post cannot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", useri=current_user)

@views.route('/delete_post/<int:post_id>', methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.user:
        flash("You cannot delete this post", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", category="success")
    return redirect(url_for('views.home'))

@views.route('posts/<username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Post.query.filter_by(author=user.id).all()
        return render_template("posts.html", user=user, posts=posts)
    else:
        return "User not found", 404