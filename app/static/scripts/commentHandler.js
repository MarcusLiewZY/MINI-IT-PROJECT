import { setConnectionLine } from "./connectionLine.js";
import { autoResizeCommentInput } from "./postCardHandler.js";
import { fetchAPI, scrollToTopElement } from "./utils.js";

export class CommentHandler {
  constructor(commentContainer) {
    this.commentContainer = commentContainer;
    this.userId = document.querySelector(".current-user-id").dataset.userId;
    this.postId = this.commentContainer.closest(".post-card").dataset.postId;
    this.commentId = this.commentContainer.id.split("-").slice(1).join("-");
    this.commentLevel = parseInt(this.commentContainer.dataset.commentLevel);

    this.commentInfoContainer =
      this.commentContainer.querySelector(".comment-info");

    // like elements
    this.commentLikeButton =
      this.commentInfoContainer.querySelector(".comment-like");

    //   edit elements
    this.editCommentButton =
      this.commentInfoContainer.querySelector(".comment-edit");
    this.editCommentCancelButton = this.commentInfoContainer.querySelector(
      ".edit-comment__cancel-button",
    );
    this.editCommentSaveButton = this.commentInfoContainer.querySelector(
      ".edit-comment__save-button",
    );

    // delete elements
    this.deleteCommentButton =
      this.commentInfoContainer.querySelector(".comment-delete");

    // report elements
    this.reportCommentButton = commentContainer.querySelector(".report-button");

    // flags
    this.isCommentLikedByUser =
      this.commentLikeButton.dataset.isCommentLikedByUser.toLowerCase() ===
      "true";
    this.isReported = false;

    // bind the context of the class methods
    this.onCommentLikeClick = this.onCommentLikeClick.bind(this);
    this.onCommentEditClick = this.onCommentEditClick.bind(this);
    this.onCommentSaveButtonClick = this.onCommentSaveButtonClick.bind(this);
    this.onCommentCancelButtonClick =
      this.onCommentCancelButtonClick.bind(this);
    this.onCommentDeleteClick = this.onCommentDeleteClick.bind(this);
    this.onCommentReportClick = this.onCommentReportClick.bind(this);

    this.isEventListenersAttached = false;

    if (this.commentContainer) {
      this.attachEventListeners();
    }
  }

  attachEventListeners() {
    if (this.isEventListenersAttached) return;

    this.commentLikeButton?.addEventListener("click", this.onCommentLikeClick);
    this.editCommentButton?.addEventListener("click", this.onCommentEditClick);
    this.deleteCommentButton?.addEventListener(
      "click",
      this.onCommentDeleteClick,
    );
    this.reportCommentButton?.addEventListener(
      "click",
      this.onCommentReportClick,
    );

    this.isEventListenersAttached = true;
  }

  async onCommentLikeClick() {
    this.commentLikeButton.disabled = true;

    try {
      const { status } = await fetchAPI(
        `/api/comments/${this.commentId}?isLike=${!this.isCommentLikedByUser}`,
        "POST",
        null,
      );

      if (status !== 200) throw new Error("Failed to like the comment");

      const likeCommentCount = document.querySelector(
        `#like-count-${this.commentId}`,
      );

      this.isCommentLikedByUser = !this.isCommentLikedByUser;
      this.commentLikeButton.dataset.isCommentLikedByUser =
        this.isCommentLikedByUser.toString();

      // if the comment is liked by the user
      if (this.isCommentLikedByUser) {
        // if the comment has no likes, increment the count, and show the count
        if (likeCommentCount.textContent === "0") {
          likeCommentCount.parentNode.classList.remove("d-none");
          likeCommentCount.textContent = 1;
        }

        // if the comment has likes, increment the count
        else {
          likeCommentCount.textContent =
            parseInt(likeCommentCount.textContent) + 1;
        }

        likeCommentCount.parentNode.classList.add("text-active");
        this.commentLikeButton.classList.add("text-active");
      }

      //   if the comment is disliked by the user
      else {
        // if the comment has only one like, hide the count
        if (likeCommentCount.textContent === "1") {
          likeCommentCount.parentNode.classList.add("d-none");
          likeCommentCount.textContent = 0;
        }

        // if the comment has more than one like, decrement the count
        else {
          likeCommentCount.textContent = parseInt(
            likeCommentCount.textContent - 1,
          );
        }

        likeCommentCount.parentNode.classList.remove("text-active");
        this.commentLikeButton.classList.remove("text-active");
      }

      likeCommentCount.nextElementSibling.textContent =
        likeCommentCount.textContent === "1" ? "like" : "likes";
    } catch (error) {
      console.error("Error from onCommentLikeClick:", error);
    } finally {
      this.commentLikeButton.disabled = false;
    }
  }

  async onCommentEditClick() {
    const comment = this.commentContainer.querySelector(".comment");
    const commentContent = comment.querySelector(".reply");

    [...this.commentInfoContainer.children].forEach((commentInfo) => {
      commentInfo.classList.add("d-none");
    });

    this.reportCommentButton.classList.add("d-none");

    const oldCommentContent = commentContent.textContent;

    comment.classList.add("editing");
    this.editCommentCancelButton.classList.remove("d-none");
    this.editCommentSaveButton.classList.remove("d-none");

    // attach event listeners to the save button
    this.editCommentCancelButton.addEventListener("click", () =>
      this.onCommentCancelButtonClick(
        comment,
        commentContent,
        oldCommentContent,
      ),
    );

    commentContent.contentEditable = true;
    commentContent.focus();

    // Place cursor at the end of the text content
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(commentContent);
    range.collapse(false); // Collapse the range to the end point
    selection.removeAllRanges();
    selection.addRange(range);

    // attach event listeners to the save button
    let isEditSuccess = false;

    this.editCommentSaveButton.addEventListener("click", async () => {
      isEditSuccess = await this.onCommentSaveButtonClick(commentContent);

      if (!isEditSuccess) throw new Error("Failed to edit the comment");

      this.editCommentSaveButton.disabled = false;

      // update the comment info element
      [...this.commentInfoContainer.children].forEach((commentInfo) => {
        commentInfo.classList.remove("d-none");
      });

      this.editCommentCancelButton.classList.add("d-none");
      this.editCommentSaveButton.classList.add("d-none");
      comment.classList.remove("editing");
      this.reportCommentButton.classList.remove("d-none");

      this.editCommentButton.textContent = "Edited";
      this.editCommentButton.classList.add("text-active");

      this.commentInfoContainer.querySelector(".date").textContent = "just now";
    });
  }

  async onCommentSaveButtonClick(commentContent) {
    this.editCommentSaveButton.disabled = true;

    try {
      const { comment: commentObj, status } = await fetchAPI(
        `/api/comments/${this.commentId}`,
        "PUT",
        {
          postId: this.postId,
          comment: commentContent.textContent,
        },
      );

      if (status !== 200) throw new Error("Failed to edit the comment");

      const { content } = commentObj;

      commentContent.contentEditable = false;
      commentContent.textContent = content;

      return true;
    } catch (error) {
      console.error("Error from commentEditHandler: ", error);
    }
  }

  onCommentCancelButtonClick(comment, commentContent, oldCommentContent) {
    commentContent.contentEditable = false;
    commentContent.textContent = oldCommentContent;
    [...this.commentInfoContainer.children].forEach((commentInfo) => {
      commentInfo.classList.remove("d-none");
    });

    comment.classList.remove("editing");
    this.editCommentCancelButton.classList.add("d-none");
    this.editCommentSaveButton.classList.add("d-none");
  }

  async onCommentDeleteClick() {
    this.deleteCommentButton.disabled = true;

    try {
      const { status, replied_comment_id: repliedCommentId } = await fetchAPI(
        `/api/comments/${this.commentId}`,
        "DELETE",
      );

      if (status !== 200) throw new Error("Failed to delete the comment");

      // update the comment count
      const commentCount = document.querySelector(
        `#comment-count-${this.postId}`,
      );

      if (commentCount.textContent === "1") {
        commentCount.textContent = 0;
      } else {
        commentCount.textContent = parseInt(commentCount.textContent - 1);
      }

      commentCount.nextElementSibling.textContent =
        commentCount.textContent === "1" ? " comment" : " comments";

      const postCard = this.commentContainer.closest(`#post-${this.postId}`);

      const otherCreatedComments = [
        ...postCard.querySelectorAll(
          ".post-card__post-comment-container .comment-container",
        ),
      ].filter(
        (commentContainer) =>
          commentContainer.querySelector(".avatar-container .avatar")?.dataset
            .userId === this.userId,
      );

      if (otherCreatedComments.length <= 1) {
        commentCount.parentNode.classList.remove("text-active");
      }

      // update the replied comment button
      const commentGroupContainer = this.commentContainer.closest(
        ".comment-group-container",
      );
      let previousReply = commentGroupContainer.previousElementSibling;
      let nextReply = commentGroupContainer.nextElementSibling;
      let replies = [];

      while (previousReply?.classList.contains("comment-group-container")) {
        replies.push(previousReply);
        previousReply = previousReply.previousElementSibling;
      }

      while (nextReply?.classList.contains("comment-group-container")) {
        replies.push(nextReply);
        nextReply = nextReply.nextElementSibling;
      }

      replies = replies.filter(
        (reply) =>
          reply.querySelector(".avatar-container .avatar").dataset.userId ===
          this.userId,
      );

      if (replies.length === 0) {
        const repliedComment = document.querySelector(
          `#comment-${repliedCommentId}`,
        );

        const replyCount = repliedComment?.querySelector(
          `#reply-count-${repliedCommentId}`,
        );

        repliedComment
          ?.querySelector(".comment-reply")
          .classList.remove("text-active");

        replyCount?.parentNode.classList.remove("text-active");
        replyCount?.classList.remove("text-active");
      }

      if (this.commentLevel === 1) {
        this.commentContainer.remove();
        return;
      }

      // dynamically show the delete button for the replied comment
      const previousComment = commentGroupContainer.previousElementSibling;
      const nextComment = commentGroupContainer.nextElementSibling;

      // if the comment level is 2
      if (this.commentLevel === 2) {
        // if the previous comment is the replied comment and the next comment is not a reply
        if (
          previousComment?.dataset.commentLevel === "1" &&
          (nextComment?.dataset.commentLevel === "1" || !nextComment)
        ) {
          previousComment
            .querySelector(".comment-info .comment-delete")
            ?.classList.remove("d-none");

          previousComment
            .querySelector(".comment-info .comment-edit")
            ?.classList.remove("d-none");
        }
      }

      // if the comment level is greater than 2
      else {
        if (
          previousComment?.classList.contains("comment-container") &&
          !nextComment
        ) {
          previousComment
            .querySelector(".comment-info .comment-delete")
            ?.classList.remove("d-none");

          previousComment
            .querySelector(".comment-info .comment-edit")
            ?.classList.remove("d-none");
        }
      }

      // update the reply count
      const replyCount = document.querySelector(
        `#reply-count-${repliedCommentId}`,
      );

      if (replyCount.textContent === "1") {
        replyCount.parentNode.classList.add("d-none");
        replyCount.textContent = 0;
      } else {
        replyCount.textContent = parseInt(replyCount.textContent) - 1;
      }

      replyCount.nextElementSibling.textContent =
        replyCount.textContent === "1" ? " reply" : " replies";

      commentGroupContainer.remove();
    } catch (error) {
      console.error("Error from onCommentDeleteClick:", error);
    } finally {
      this.deleteCommentButton.disabled = false;
    }
  }

  async onCommentReportClick() {
    this.isReported =
      this.reportCommentButton.dataset.isReported.toLowerCase() === "true";

    if (this.isReported === true) return;

    this.reportCommentButton.disabled = true;

    try {
      const { status } = await fetchAPI(
        `/api/comments/${this.commentId}/reporting?isReport=${!this.isReported}`,
        "PUT",
      );

      if (status !== 200) throw new Error("Failed to report the comment");

      this.isReported = !this.isReported;

      this.reportCommentButton.classList.add("text-error");

      this.reportCommentButton.textContent = "Reported";

      this.reportCommentButton.dataset.isReported = this.isReported.toString();
    } catch (error) {
      console.error("Error from likeButtonHandler:", error);
    } finally {
      this.reportCommentButton.disabled = false;
    }
  }
}

export const onLoadCommentHandler = () => {
  const commentContainers = document.querySelectorAll(".comment-container");

  commentContainers.forEach((commentContainer) => {
    new CommentHandler(commentContainer);
  });
};

const onCreateCommentHandlerSubmit = async (
  e,
  {
    postId,
    postCard,
    createCommentForm,
    createCommentFormContainer,
    outermostCommentGroupContainer,
    isSubmitting,
  },
) => {
  e.preventDefault();

  if (isSubmitting) return;

  isSubmitting = true;
  createCommentForm.disabled = true;

  try {
    const commentFormData = new FormData(createCommentForm);

    const commentFormDataObj = Object.fromEntries(commentFormData.entries());

    // clear the comment form
    createCommentForm.reset();

    const { status: createPostStatus, comment_id: commentId } = await fetchAPI(
      "/api/comments",
      "POST",
      {
        ...commentFormDataObj,
        postId: postId,
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

    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = newCommentHTML;

    const newComment = tempDiv.firstChild;

    outermostCommentGroupContainer.appendChild(newComment);

    // update the comment counts of the postcard
    const commentCount = postCard.querySelector(`#comment-count-${postId}`);

    commentCount.textContent =
      commentCount.textContent === "0"
        ? 1
        : parseInt(commentCount.textContent) + 1;

    commentCount.nextElementSibling.textContent =
      commentCount.textContent === "1" ? " comment" : " comments";

    commentCount.parentNode.classList.add("text-active");

    // if the current page is not the post detail page, return the newComment
    if (
      window.location.pathname === `/posts/${postId}` &&
      document.body.offsetHeight > 1500
    ) {
      // navigate to the newly created comment
      newComment.scrollIntoView({ behavior: "smooth" });

      scrollToTopElement(createCommentFormContainer, 20);
    }

    return newComment;
  } catch (error) {
    console.error("Error from createCommentHandler:", error);
  }
};

const onLoadCreateCommentHandler = () => {
  const createCommentFormContainers = document.querySelectorAll(
    ".post-card__add-comment-container",
  );

  createCommentFormContainers.forEach((createCommentFormContainer) => {
    if (!createCommentFormContainer) return;

    const postId =
      createCommentFormContainer.closest(".post-card").dataset.postId;

    const createCommentForm = createCommentFormContainer.querySelector(
      `#comment-form-${postId}`,
    );

    const postCard = createCommentFormContainer.closest(".post-card");

    const outermostCommentGroupContainer = postCard?.querySelector(
      ".post-card__post-comment-container .comment-group-container",
    );

    let isSubmitting = false;

    const createCommentFormObj = {
      postId,
      postCard,
      createCommentForm,
      createCommentFormContainer,
      outermostCommentGroupContainer,
      isSubmitting,
    };

    createCommentForm.addEventListener("submit", async (e) => {
      try {
        const newComment = await onCreateCommentHandlerSubmit(
          e,
          createCommentFormObj,
        );

        if (!newComment) throw new Error("Failed to create a comment");

        isSubmitting = false;
        createCommentForm.disable = false;

        // initialize the comment handler for the new comment
        new CommentHandler(newComment);
        onCommentReplyHandler();
      } catch (error) {
        console.error("Error from createCommentHandler:", error);
      }
    });
  });
};

const onCreateReplyHandlerSubmit = async (
  e,
  {
    postId,
    commentId,
    isCommentRepliedByUser,
    commentContainer,
    commentReplyForm,
    commentReplyFormContainer,
    commentReplyButton,
    isSubmitting,
  },
) => {
  if (isSubmitting) return;

  isSubmitting = true;
  commentReplyForm.disabled = true;

  try {
    e.preventDefault();

    const formData = new FormData(commentReplyForm);
    const { comment } = Object.fromEntries(formData.entries());

    const { status } = await fetchAPI(
      `/api/comments/${commentId}/reply`,
      "POST",
      {
        postId,
        comment,
      },
    );

    if (status !== 201) throw new Error("Failed to reply to the comment");

    commentReplyForm.reset();

    isCommentRepliedByUser = !isCommentRepliedByUser;
    commentReplyFormContainer.classList.add("d-none");

    // Fetch the constructed comment HTML
    const { status: renderStatus, html } = await fetchAPI(
      `/api/comments/${commentId}/construct-comment`,
      "PUT",
      { commentLevel: commentContainer.dataset.commentLevel },
    );

    if (renderStatus !== 200)
      throw new Error("Failed to construct the comment");

    // Create a temporary div to hold the new reply HTML
    const tempDiv = document.createElement("div");
    const newCommentGroupContainer = `
        <div class="flex flex-col comment-group-container">
          ${html}
        </div>
      `;

    tempDiv.innerHTML = newCommentGroupContainer;

    // Find the new reply element inside the temporary div
    const newReplyGroupContainer = tempDiv.querySelector(
      ".comment-group-container",
    ).lastElementChild;

    // Append the new reply element to the current comment container's replies
    let currentElement = commentContainer;

    while (
      currentElement.nextElementSibling &&
      currentElement.nextElementSibling.classList.contains(
        "comment-group-container",
      )
    ) {
      currentElement = currentElement.nextElementSibling;
    }

    currentElement.insertAdjacentElement("afterend", newReplyGroupContainer);

    // Initialize the CommentHandler for the new reply
    commentReplyButton.classList.remove("d-none");
    commentReplyButton
      .closest(".comment-info")
      .querySelector(".comment-like")
      .classList.remove("d-none");

    const newReplyCommentContainer =
      newReplyGroupContainer.querySelector(".comment-container");

    new CommentHandler(newReplyCommentContainer);
    setConnectionLine();

    return newReplyCommentContainer;
  } catch (error) {
    console.error("Error from commentReplyHandler:", error);
  } finally {
    isSubmitting = false;
    commentReplyForm.disabled = false;
  }
};

const initializeReplyEventListeners = (commentContainer) => {
  const postId = commentContainer.closest(".post-card").dataset.postId;
  const postCard = commentContainer.closest(".post-card");
  const commentId = commentContainer.id.split("-").slice(1).join("-");
  const commentInfoContainer = commentContainer.querySelector(".comment-info");
  const commentReplyButton =
    commentInfoContainer.querySelector(".comment-reply");
  const isCommentRepliedByUser =
    commentReplyButton.dataset.isCommentRepliedByUser.toLowerCase() === "true";

  let commentReplyFormContainer = commentReplyButton
    ?.closest(".comment-container")
    ?.querySelector(".reserve-elements + .reserve-element.comment-form");

  // If the comment reply form container does not exist, create a new one
  if (!commentReplyFormContainer) {
    commentReplyFormContainer = commentReplyButton
      ?.closest(".comment-container")
      ?.querySelector(".reserve-elements .reserve-element.comment-form")
      .cloneNode(true);

    commentContainer.appendChild(commentReplyFormContainer);
    autoResizeCommentInput();
  }

  const commentReplyFormCancelButton =
    commentReplyFormContainer.querySelector(".cancel-button");
  const commentReplyForm = commentReplyFormContainer.querySelector("form");

  commentReplyFormContainer.style.marginLeft = "2.5rem";
  commentReplyFormContainer.classList.add("d-none");

  const handleReplyButtonClick = () => {
    commentReplyFormContainer.classList.remove("d-none");
    commentReplyForm.querySelector("textarea").focus();

    [...commentInfoContainer.querySelectorAll("button")]
      .filter(
        (button) => !button.classList.contains("edit-comment__save-button"),
      )
      .forEach((button) => button.classList.add("d-none"));
  };

  const handleReplyCancelButtonClick = () => {
    commentReplyForm.reset();
    commentReplyFormContainer.classList.add("d-none");

    [...commentInfoContainer.querySelectorAll("button")]
      .filter(
        (button) => !button.classList.contains("edit-comment__save-button"),
      )
      .forEach((button) => button.classList.remove("d-none"));
  };

  let isSubmitting = false;

  const createReplyHandlerObj = {
    postId,
    commentId,
    isCommentRepliedByUser,
    commentContainer,
    commentReplyFormContainer,
    commentReplyForm,
    commentReplyButton,
    isSubmitting,
  };

  const handleReplyFormSubmit = async (e) => {
    try {
      e.preventDefault();
      const newReply = await onCreateReplyHandlerSubmit(
        e,
        createReplyHandlerObj,
      );

      if (!newReply) throw new Error("Failed to create a reply");

      commentInfoContainer
        .querySelector(".comment-delete")
        ?.classList.add("d-none");
      commentInfoContainer
        .querySelector(".comment-edit")
        ?.classList.add("d-none");

      // update the reply count
      const replyCount = commentContainer.querySelector(
        `#reply-count-${commentId}`,
      );

      if (replyCount.textContent === "0") {
        replyCount.parentNode.classList.remove("d-none");
        replyCount.textContent = 1;
      } else {
        replyCount.textContent = parseInt(replyCount.textContent) + 1;
      }

      replyCount.nextElementSibling.textContent =
        replyCount.textContent === "1" ? " reply" : " replies";

      replyCount.parentNode.classList.add("text-active");
      replyCount.classList.add("text-active");
      commentReplyButton.classList.add("text-active");

      // update the comment counts of the postcard
      const commentCount = postCard.querySelector(`#comment-count-${postId}`);

      commentCount.textContent =
        commentCount.textContent === "0"
          ? 1
          : parseInt(commentCount.textContent) + 1;

      commentCount.nextElementSibling.textContent =
        commentCount.textContent === "1" ? " comment" : " comments";

      commentCount.parentNode.classList.add("text-active");

      // Initialize event listeners for the new reply only
      initializeReplyEventListeners(newReply);
    } catch (error) {
      console.error("Error from commentReplyHandler:", error);
    }
  };

  // Remove existing event listeners
  commentReplyButton.removeEventListener("click", handleReplyButtonClick);
  commentReplyFormCancelButton.removeEventListener(
    "click",
    handleReplyCancelButtonClick,
  );
  commentReplyForm.removeEventListener("submit", handleReplyFormSubmit);

  // Add event listeners
  commentReplyButton.addEventListener("click", handleReplyButtonClick);
  commentReplyFormCancelButton.addEventListener(
    "click",
    handleReplyCancelButtonClick,
  );
  commentReplyForm.addEventListener("submit", handleReplyFormSubmit);
};

const onCommentReplyHandler = () => {
  const commentContainers = document.querySelectorAll(
    ".comment-container[id]:not([id=''])",
  );
  commentContainers.forEach(initializeReplyEventListeners);
};

["DOMContentLoaded", "postCardsPaginationLoaded"].forEach((e) => {
  document.addEventListener(e, () => {
    onLoadCreateCommentHandler();
    onLoadCommentHandler();

    onCommentReplyHandler();
  });
});
