import { insertLineBreaks } from "./utils.js";
import { autoResizeCommentInput } from "./postCardHandler.js";
import { fetchAPI, scrollToTopElement } from "./utils.js";

class CommentHandler {
  constructor() {
    this.isEventListenersAttached = false;
  }

  setupCommentHandler() {
    this.setupEventListeners();
  }

  setupEventListeners() {
    if (this.isEventListenersAttached) return;

    this.isEventListenersAttached = true;
  }
}

class CommentFormHandler {
  constructor() {
    this.isEventListenersAttached = false;

    this.postId = null;
    this.createCommentForm = null;
    this.createCommentFormOutermostContainer = null;
    this.outermostCommentGroupContainer = null;

    // bind the method to the instance
    this.onCreateCommentFormSubmit = this.onCreateCommentFormSubmit.bind(this);
  }

  setupCommentFormHandler(postCard) {
    if (!postCard) return;

    this.postId = postCard.dataset.postId;
    this.createCommentForm = postCard.querySelector(
      `#addCommentForm-${this.postId}`,
    );
    this.outermostCommentGroupContainer = postCard.querySelector(
      ".post-card__post-comment-container .comment-group-container",
    );
    this.createCommentFormOutermostContainer = postCard.querySelector(
      ".post-card__add-comment-container",
    );

    this.setupEventListeners();
  }

  setupEventListeners() {
    if (this.isEventListenersAttached) return;

    this.createCommentForm.addEventListener(
      "submit",
      this.onCreateCommentFormSubmit,
    );

    this.isEventListenersAttached = true;
  }

  async onCreateCommentFormSubmit(e) {
    e.preventDefault();

    const commentFormData = new FormData(this.createCommentForm);

    const commentFormDataObj = Object.fromEntries(commentFormData.entries());

    const { status: createPostStatus, comment_id: commentId } = await fetchAPI(
      "/api/comments",
      "POST",
      {
        ...commentFormDataObj,
        postId: this.postId,
      },
    );

    if (createPostStatus !== 201) throw new Error("Failed to create a comment");

    // construct a new comment element by calling the construct api
    const { status: constructCommentStatus, html: newCommentHTML } =
      await fetchAPI(`/api/comments/${commentId}/construct-comment`, "PUT", {
        commentLevel: 1,
      });

    if (constructCommentStatus !== 200)
      throw new Error("Failed to construct a comment");

    const newComment = document.createElement("div");
    newComment.innerHTML = newCommentHTML;

    this.outermostCommentGroupContainer.appendChild(newComment);

    // clear the comment form
    this.createCommentForm.reset();

    // navigate to the newly created comment
    newComment.scrollIntoView({ behavior: "smooth" });

    scrollToTopElement(this.createCommentFormOutermostContainer, 20);
  }
}

const commentHandler = new CommentHandler();
const commentFormHandler = new CommentFormHandler();

["DOMContentLoaded", "postCardsPaginationLoaded"].forEach((e) => {
  document.addEventListener(e, () => {
    const postCards = document.querySelectorAll(".post-card");

    postCards.forEach((postCard) => {
      commentFormHandler.setupCommentFormHandler(postCard);
    });
  });
});
