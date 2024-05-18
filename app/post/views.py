from uuid import UUID
from flask import flash, redirect, url_for, render_template, request
from flask_login import current_user

from . import post
from app.main import main
from app.models.post import Post, Status
from app.models.user import User
from app.dto.post_dto import PostDTO
from app.utils.decorators import login_required
from app.forms.postForms import CreatePostForm
from app.services.post_service import edit_post


@post.route("/<post_id>", methods=["GET", "POST"])
@login_required
def get_post(post_id):

    user = User.query.get(current_user.id)
    post = Post.query.get(UUID(post_id))

    editPostForm = CreatePostForm()
    editPostForm.set_tag_choices()

    if request.method == "POST":
        if editPostForm.validate_on_submit():

            isSuccess, message = edit_post(post, editPostForm)
            flash(message, "success" if isSuccess else "error")

    editPostForm.title.data = post.title
    editPostForm.content.data = post.content
    editPostForm.tags.data = [tag.name for tag in post.tags]
    editPostForm.image_url.data = post.image_url if post.image_url else None

    if not post or post.is_delete:
        flash("Post not found", "error")
        return redirect(url_for(main.index))

    postCreator = User.query.get(post.user_id)

    postDTO = PostDTO(post, postCreator, user)

    return render_template(
        "post/postDetail.html",
        post=postDTO.to_dict(),
        user=current_user,
        editPostForm=editPostForm,
    )
