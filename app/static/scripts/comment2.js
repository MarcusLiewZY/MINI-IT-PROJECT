import { setConnectionLine } from "./connectionLine.js";
import { insertLineBreaks } from "./utils.js";
import { autoResizeCommentInput } from "./postCardHandler.js";

class CommentReplyForm {
  constructor(commentReplyButton) {
    this.commentReplyButton = commentReplyButton;
    this.commentReplyForm = this.commentReplyButton
      .closest(".comment-group-container")
      .querySelector(".reserve-elements .reserve-element.comment-form")
      .cloneNode(true);
    this.commentReplyFormCancelButton =
      this.commentReplyForm.querySelector(".cancel-button");
  }
}

class CommentHandler {
  constructor(commentContainer) {
    this.commentContainer = commentContainer;
    this.userId = document.querySelector(".current-user-id").dataset.userId;
    this.postId = this.commentContainer.closest(".post-card").dataset.postId;
    this.commentId = this.commentContainer.id.split("-").slice(1).join("-");

    this.commentInfoContainer =
      this.commentContainer.querySelector(".comment-info");

    // like elements
    this.commentLikeButton =
      this.commentInfoContainer.querySelector(".comment-like");

    // reply elements
    this.commentReplyButton =
      this.commentInfoContainer.querySelector(".comment-reply");
    // this.commentReplyForm = this.commentReplyButton
    //   .closest(".comment-group-container")
    //   .querySelector(".reserve-elements .reserve-element.comment-form")
    //   .cloneNode(true);
    // this.commentReplyFormCancelButton =
    //   this.commentReplyForm.querySelector(".cancel-button");
    this.commentReplyForm = null;

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
    this.isCommentRepliedByUser =
      this.commentReplyButton.dataset.isCommentRepliedByUser.toLowerCase() ===
      "true";
    this.isReported = false;

    // bind the context of the class methods
    this.onCommentLikeClick = this.onCommentLikeClick.bind(this);
    this.onCommentReplyClick = this.onCommentReplyClick.bind(this);
    this.onCommentEditClick = this.onCommentEditClick.bind(this);
    this.onCommentSaveButtonClick = this.onCommentSaveButtonClick.bind(this);
    this.onCommentCancelButtonClick =
      this.onCommentCancelButtonClick.bind(this);
    this.onCommentDeleteClick = this.onCommentDeleteClick.bind(this);
    this.onCommentReportClick = this.onCommentReportClick.bind(this);
    this.fetchAPI = this.fetchAPI.bind(this);

    this.isEventListenersAttached = false;

    if (this.commentContainer) {
      this.attachEventListeners();
    }
  }

  attachEventListeners() {
    if (this.isEventListenersAttached) return;

    this.commentLikeButton?.addEventListener("click", this.onCommentLikeClick);
    this.commentReplyButton?.addEventListener(
      "click",
      this.onCommentReplyClick,
    );
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

  // utility functions
  async fetchAPI(url, method, body = null) {
    try {
      const response = await fetch(url, {
        method: method,
        body: JSON.stringify(body),
        headers: {
          "Content-type": "application/json",
        },
      });

      return await response.json();
    } catch (error) {
      console.error("Error from fetchAPI:", error);
    }
  }

  async onCommentLikeClick() {
    try {
      const { status } = await this.fetchAPI(
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
    }
  }

  async onCommentReplyClick() {
    this.commentReplyForm.style.marginLeft = "2.5rem";

    commentContainer.appendChild(newCommentReplyForm);
    autoResizeCommentInput();

    this.commentReplyButton.classList.add("d-none");

    this.commentReplyFormCancelButton.addEventListener("click", () => {
      newCommentReplyForm.remove();
      this.commentReplyButton.classList.remove("d-none");
    });

    this.commentReplyForm.addEventListener("submit", async (e) => {
      try {
        e.preventDefault();

        const replyForm = this.commentReplyForm.querySelector("form");

        const formData = new FormData(replyForm);
        const { comment } = Object.fromEntries(formData.entries());

        const { status } = await this.fetchAPI(
          `/api/comments/${this.commentId}/reply`,
          "POST",
          {
            postId: this.postId,
            comment,
          },
        );

        if (status !== 201) throw new Error("Failed to reply to the comment");

        this.isCommentRepliedByUser = !this.isCommentRepliedByUser;
        this.commentContainer.removeChild(newCommentReplyForm);

        console.log("Comment replied successfully");

        setTimeout(() => {
          window.location.href = `/posts/${this.postId}#comment-${this.commentId}`;
        }, 3000);

        // todo: call another api to construct the reply comment and append it to the comment container

        // const newComment = this.constructCommentReply(
        //   postId,
        //   commentContainer,
        //   data,
        // );

        // const replyCommentCount = commentContainer.querySelector(
        //   `#reply-count-${commentId}`,
        // );

        // if (replyCommentCount.textContent === "0") {
        //   replyCommentCount.parentNode.classList.remove("d-none");
        //   replyCommentCount.textContent = 1;
        // } else {
        //   replyCommentCount.textContent =
        //     parseInt(replyCommentCount.textContent) + 1;
        // }

        // replyCommentCount.nextElementSibling.textContent =
        //   replyCommentCount.textContent === "1" ? " reply" : " replies";

        // replyCommentCount.parentNode.classList.add("text-active");
        // button.classList.remove("hidden");
        // button.classList.add("text-active");

        // this.setupCommentContainer(newComment);
      } catch (error) {
        console.error("Error from commentReplyHandler:", error);
      }
    });
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

      // update the comment info element
      [...this.commentInfoContainer.children].forEach((commentInfo) => {
        commentInfo.classList.remove("d-none");
      });

      this.editCommentCancelButton.classList.add("d-none");
      this.editCommentSaveButton.classList.add("d-none");
      comment.classList.remove("editing");

      this.editCommentButton.textContent = "Edited";
      this.editCommentButton.classList.add("text-active");

      this.commentInfoContainer.querySelector(".date").textContent = "just now";
    });
  }

  async onCommentSaveButtonClick(commentContent) {
    try {
      const { comment: commentObj, status } = await this.fetchAPI(
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
    try {
      const { status } = await this.fetchAPI(
        `/api/comments/${this.commentId}`,
        "DELETE",
      );

      if (status !== 200) throw new Error("Failed to delete the comment");

      this.deleteCommentButton.closest(".comment-container").remove();

      const commentCount = document.querySelector(
        `#comment-count-${this.postId}`,
      );

      if (commentCount.textContent === "1") {
        commentCount.parentNode.classList.add("d-none");
        commentCount.textContent = 0;
      } else {
        commentCount.textContent = parseInt(commentCount.textContent - 1);
      }

      const commentTextMap = {
        1: " comment",
        0: "",
      };

      commentCount.nextElementSibling.textContent =
        commentTextMap[commentCount.textContent] || " comments";
    } catch (error) {
      console.error("Error from onCommentDeleteClick:", error);
    }
  }

  async onCommentReportClick() {
    this.isReported =
      this.reportCommentButton.dataset.isReported.toLowerCase() === "true";

    if (this.isReported === true) return;

    try {
      const { status } = await this.fetchAPI(
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
    }
  }
}

export const onLoadCommentHandler = () => {
  const commentContainers = document.querySelectorAll(".comment-container");

  commentContainers.forEach((commentContainer) => {
    const commentHandler = new CommentHandler(commentContainer);
  });
};

document.addEventListener("DOMContentLoaded", () => {
  onLoadCommentHandler();
});
