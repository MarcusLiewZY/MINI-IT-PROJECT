from uuid import UUID
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

from . import post
from app.main import main
from app.models.post import Post, Status
from app.models.user import User
from app.dto.post_dto import PostDTO
from app.utils.decorators import login_required


@post.route("/<post_id>")
@login_required
def get_post(post_id):
    user = User.query.get(current_user.id)
    post = Post.query.get(UUID(post_id))
    if not post or post.is_delete or post.status == Status.REJECTED:
        flash("Post not found", "error")
        return redirect(url_for(main.index))

    if post.status == Status.PENDING:
        flash("Post is still pending", "error")
        return redirect(url_for(main.index))

    postCreator = User.query.get(post.user_id)

    postDTO = PostDTO(post, postCreator, user)
    return render_template(
        "post/postDetail.html", post=postDTO.to_dict(), user=current_user
    )


# @post.route("/update-post/<post_id>", methods=["GET", "POST"])
# @login_required
# def update_post(post_id):
#     post = Post.query.get(UUID(post_id))

#     new_post = request.form

#     if not post:
#         flash("Post not found, please try again", "error")
#         return redirect(url_for("main.index"))

#     post.title = new_post.get("title")
#     post.content = new_post.get("content")
#     post.image_url = new_post.get("image_url")
#     post.updated_at = format_datetime(datetime.now())

#     for tag_name in new_post.getlist("tags"):
#         tag = Tag.query.filter_by(name=tag_name).first()
#         if not tag:
#             flash("Tag not found, please try again", "error")
#             return redirect(url_for("main.index"))

#         post.tags.append(tag)

#     db.session.commit()

#     flash("Post updated successfully", "success")
#     return redirect(url_for("main.index"))


# @post.route("/delete-post/<post_id>", methods=["GET", "POST"])
# @login_required
# def delete_post(post_id):

#     post = Post.query.get(UUID(post_id))

#     if not post:
#         flash("Post not found, please try again", "error")
#         return redirect(url_for("main.index"))

#     db.session.delete(post)
#     db.session.commit()

#     flash("Post deleted successfully", "success")
#     return redirect(url_for("main.index"))


# # get one post by id
# @post.route("/posts/<post_id>")
# @login_required
# def get_post(post_id):
#     tags = Tag.query.all()
#     post = Post.query.get(UUID(post_id))

#     if not post:
#         flash("Post not found, please try again", "error")

#     # find the author of the post
#     author = User.query.get(post.user_id)

#     post.author = author

#     return render_template(
#         "post/postDetail.html", post_stuff=post, tags=tags, isSinglePost=True
#     )


#         new_post.user_id = current_user.id

#         # todo: delete the approved status once the admin feature is implemented
#         new_post.status = Status.APPROVED

#         for tag_name in post_form.getlist("tags"):
#             tag = Tag.query.filter_by(name=tag_name).first()
#             if not tag:
#                 flash("Tag not found, please try again", "error")
#                 return redirect(url_for("main.index"))

#             new_post.tags.append(tag)

#         db.session.add(new_post)
#         db.session.commit()

#         flash("Post created successfully", "success")
#         return redirect(url_for("main.index"))

#     posts = Post.query.order_by(Post.updated_at.desc()).all()
#     tags = Tag.query.all()

#     return render_template(
#         "post/postDetail.html", post_stuff=posts, tags=tags, isSinglePost=False
#     )


# api to upload file
# @post.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"})
#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "No selected file"})
#     if file:
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#         return jsonify({"message": "File uploaded successfully"})
