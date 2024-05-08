from uuid import UUID
from flask import jsonify, request
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models.tag import Tag
from app.models.user import User
from app.models.post import Post, Status
from app.dto.post_dto import PostDTO


@api.route("/accounts/<account_id>", methods = ['DELETE'])
def delete_account(account_id):
    """
    Delete an account by its ID permanently.
    Args:
        account_id: The ID of the account to delete.
    Returns:
        A JSON object containing the account's record and an HTTP status code.
    """
    try:
        if account_id is None:
            return (
                jsonify({'error': 'Account ID is required.'}), responseStatus.BAD_REQUEST                
            )
        
        user = User.query.get(UUID(account_id))

        if user is None:
            return (
                jsonify({'error': 'Account not found.'}), responseStatus.NOT_FOUND
            )
        
        db.session.delete(user)
        db.session.commit()

        return (
            jsonify({'message': 'Account deleted successfully.'}), responseStatus.OK
        )

    except Exception as e:
        print(e)
        return (
            jsonify({'error': 'Internal Server Error'}), responseStatus.INTERNAL_SERVER_ERROR
        )

@api.route("/tags", methods=["GET"])
def get_tags():
    """
    Get all tag-name and tag-color pairs.
    Returns:
        A JSON object where the keys are tag names and t
        he values are tag colors,
        and an HTTP status code.
    """
    try:
        tags = Tag.query.all()
        tags_dict = {}
        for tag in tags:
            tags_dict[tag.name] = tag.color
        return jsonify(tags_dict), responseStatus.OK
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )

@api.route("/posts", methods=["GET"])
def get_posts():
    """
    Get all posts ordered by the updated_at field in descending order.
    Args:
        isPreview: A boolean indicating whether to return a preview of the post. Default is False.
        isDeleted: A boolean indicating whether to return the soft deleted posts. Default is False.
        isApproved: A boolean indicating whether to return approved posts. Default is False.
    Returns:
        A JSON object containing all posts and an HTTP status code.
    """
    try:
        isPreview = request.args.get("isPreview", "false").lower() == "true"
        isDeleted = request.args.get("isDeleted", "false").lower() == "true"
        isApproved = request.args.get("isApproved", "true").lower() == "true"

        query = Post.query

        if isDeleted:
            query = query.filter(Post.is_delete == True)

        if isApproved:
            query = query.filter(Post.status == Status.APPROVED)

        posts = query.order_by(Post.updated_at.desc()).all()
        postDTOs = [
            PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()
            for post in posts
        ]

        return jsonify({"posts": postDTOs}), responseStatus.OK

    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
@api.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    """
    Get a post by its ID.
    Args:
        post_id: The ID of the post to get.
        isPreview: A boolean indicating whether to return a preview of the post. Default is False.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        isPreview = request.args.get("isPreview", "false").lower() == "true"
        post = Post.query.get(UUID(post_id))
        if post is None:
            return (
                jsonify({"error": "Post not found"}),
                responseStatus.NOT_FOUND,
            )

        postDTO = PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()

        return jsonify({"post": postDTO}), responseStatus.OK
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id, isSoftDelete):
    """
    Delete a post by its ID.
    Args:
        post_id: The ID of the post to delete.
        isSoftDelete: A boolean indicating whether to soft delete the post. Default is True.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        post = Post.query.get(UUID(post_id))
        isSoftDelete = request.args.get("isSoftDelete", "true").lower() == "true"

        if post is None:
            return (
                jsonify({"error": "Post not found"}),
                responseStatus.NOT_FOUND,
            )

        if isSoftDelete:
            if post.is_delete:
                return (
                    jsonify({"error": "Post already soft deleted"}),
                    responseStatus.BAD_REQUEST,
                )
            post.is_delete = True
        else:
            db.session.delete(post)

        db.session.commit()

        return jsonify({"message": f"Post is{"soft" if isSoftDelete else ""} deleted successfully"}), responseStatus.OK
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
