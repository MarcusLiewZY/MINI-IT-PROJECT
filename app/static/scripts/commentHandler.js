import { setConnectionLine } from "./connectionLine.js";
import { insertLineBreaks } from "./utils.js";
import { autoResizeCommentInput } from "./postCardHandler.js";
class CommentHandler {
  constructor(userId) {
    this.userId = userId;
    this.isCommentLikedByUser = false;
    this.isCommentRepliedByUser = false;
    this.isReported = false;

    this.commentLikeHandler = this.commentLikeHandler.bind(this);
    this.commentReplyHandler = this.commentReplyHandler.bind(this);
    this.commentDeleteHandler = this.commentDeleteHandler.bind(this);
    this.commentEditHandler = this.commentEditHandler.bind(this);
    this.commentReportHandler = this.commentReportHandler.bind(this);
  }

  async fetchAPI(url, method, body = null) {
    try {
      const response = await fetch(url, {
        method: method,
        body: JSON.stringify(body),
        headers: {
          "Content-type": "application/json",
        },
      });

      const data = await response.json();

      return data;
    } catch (error) {
      console.error("Error from fetchAPI: ", error);
    }
  }

  commentLikeHandler(commentId) {
    return async (button) => {
      this.isCommentLikedByUser =
        button.dataset.isCommentLikedByUser.toLowerCase() === "true";

      try {
        const data = await this.fetchAPI(
          `/api/comments/${commentId}?isLike=${!this.isCommentLikedByUser}`,
          "POST",
          null,
        );

        if (data[0].status === 200) {
          const likeCommentCount = document.querySelector(
            `#like-count-${commentId}`,
          );
          if (this.isCommentLikedByUser) {
            if (likeCommentCount.textContent === "1") {
              likeCommentCount.parentNode.classList.add("d-none");
              likeCommentCount.textContent = 0;
            } else {
              (likeCommentCount.textContent =
                parseInt(likeCommentCount.textContent) - 1),
                likeCommentCount.parentNode.classList.remove("text-active");
            }

            button.classList.remove("text-active");
          } else {
            if (likeCommentCount.textContent === "0") {
              likeCommentCount.parentNode.classList.remove("d-none");
              likeCommentCount.textContent = 1;
            } else {
              likeCommentCount.textContent =
                parseInt(likeCommentCount.textContent) + 1;
            }

            likeCommentCount.parentNode.classList.add("text-active");
            button.classList.add("text-active");
          }

          likeCommentCount.nextElementSibling.textContent =
            likeCommentCount.textContent === "1" ? "like" : "likes";

          this.isCommentLikedByUser = !this.isCommentLikedByUser;
          button.dataset.isCommentLikedByUser =
            this.isCommentLikedByUser.toString();
        }
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    };
  }

  // utility function - reply comment handler
  constructCommentReply(postId, commentContainer, data) {
    const postCard = document.querySelector(
      `.post-card[data-post-id="${postId}"]`,
    );

    const {
      comment_id,
      content,
      replied_comment_id,
      comment_user_anon_no,
      replied_comment_user_anon_no,
    } = data;

    const newComment = postCard
      .querySelector(".reserve-elements .comment-group-container")
      .cloneNode(true);
    newComment.id = `comment-${comment_id}`;
    newComment.dataset.currentUserId = this.userId;
    newComment.querySelector(".reply").innerHTML = insertLineBreaks(content);

    Array("comment-edit", "comment-delete", "comment-reply").forEach(
      (className) => {
        newComment.querySelector(`.${className}`).classList.add("hidden");
      },
    );

    const likeCount = newComment.querySelector("#like-count-");
    likeCount.id = `like-count-${comment_id}`;
    likeCount.textContent = 0;
    likeCount.parentNode.classList.add("d-none");
    const replyCount = newComment.querySelector("#reply-count-");
    replyCount.id = `reply-count-${comment_id}`;
    replyCount.textContent = 0;
    replyCount.parentNode.classList.add("d-none");
    newComment.querySelector(".user-interaction-container").innerHTML = `
            Anonymous_${comment_user_anon_no}
              <a
                href="/posts/${postId}#comment-${replied_comment_id}"
                class="link user-interaction-container__reply"
              >
                reply to
                <span class="replied-user"
                  >Anonymous_${replied_comment_user_anon_no}</span
                ></a
              >
    `;

    newComment.style.marginLeft = "2.5rem";
    commentContainer.appendChild(newComment);
    setConnectionLine();

    return newComment;
  }

  // reply commend handler
  commentReplyHandler(commentId) {
    return async (button) => {
      this.isCommentRepliedByUser =
        button.dataset.isCommentRepliedByUser.toLowerCase() === "true";

      // create the comment reply form
      const newCommentReplyForm = button
        .closest(".comment-group-container")
        .querySelector(".reserve-elements .reserve-element.comment-form")
        .cloneNode(true);

      newCommentReplyForm.style.marginLeft = "2.5rem";

      const commentContainer = button.closest(".comment-container");

      commentContainer.appendChild(newCommentReplyForm);
      autoResizeCommentInput();

      button.classList.add("d-none");

      const cancelReplyFormButton =
        newCommentReplyForm.querySelector(".cancel-button");

      cancelReplyFormButton.addEventListener("click", () => {
        newCommentReplyForm.remove();
        button.classList.remove("d-none");
      });

      newCommentReplyForm.addEventListener("submit", async (e) => {
        try {
          e.preventDefault();

          const replyForm = newCommentReplyForm.querySelector("form");

          const formData = new FormData(replyForm);
          const { comment } = Object.fromEntries(formData.entries());

          const postId = button.closest(".post-card").dataset.postId;

          const data = await this.fetchAPI(
            `/api/comments/${commentId}/reply`,
            "POST",
            {
              postId,
              comment,
            },
          );

          if (data.status === 201) {
            this.isCommentRepliedByUser = !this.isCommentRepliedByUser;
            commentContainer.removeChild(newCommentReplyForm);

            const newComment = this.constructCommentReply(
              postId,
              commentContainer,
              data,
            );

            const replyCommentCount = commentContainer.querySelector(
              `#reply-count-${commentId}`,
            );

            if (replyCommentCount.textContent === "0") {
              replyCommentCount.parentNode.classList.remove("d-none");
              replyCommentCount.textContent = 1;
            } else {
              replyCommentCount.textContent =
                parseInt(replyCommentCount.textContent) + 1;
            }

            replyCommentCount.nextElementSibling.textContent =
              replyCommentCount.textContent === "1" ? " reply" : " replies";

            replyCommentCount.parentNode.classList.add("text-active");
            button.classList.remove("hidden");
            button.classList.add("text-active");

            this.setupCommentContainer(newComment);
          }
        } catch (error) {
          console.error("Error from commentReplyHandler:", error);
        }
      });
    };
  }

  // delete comment handler
  commentDeleteHandler(commentId) {
    return async (button) => {
      try {
        const data = await this.fetchAPI(
          `/api/comments/${commentId}`,
          "DELETE",
        );

        if (data.status === 200) {
          const postId = button.closest(".post-card").dataset.postId;

          button.closest(".comment-container").remove();

          const commentCount = document.querySelector(
            `#comment-count-${postId}`,
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
        }
      } catch (error) {
        console.error("Error from commentDeleteHandler: ", error);
      }
    };
  }

  // edit comment handler
  commentEditHandler(commentId) {
    return async (button) => {
      const commentContainer = button.closest(".comment-container");
      const commentInfoContainer =
        commentContainer.querySelector(".comment-info");

      const editCommentCancelButton = commentInfoContainer.querySelector(
        ".edit-comment__cancel-button",
      );
      const editCommentSaveButton = commentInfoContainer.querySelector(
        ".edit-comment__save-button",
      );

      const comment = commentContainer.querySelector(".comment");
      const commentContent = comment.querySelector(".reply");

      [...commentInfoContainer.children].forEach((commentInfo) => {
        commentInfo.classList.add("d-none");
      });

      const oldCommentContent = commentContent.textContent;

      comment.classList.add("editing");
      editCommentCancelButton.classList.remove("d-none");
      editCommentSaveButton.classList.remove("d-none");

      editCommentCancelButton.addEventListener("click", () => {
        commentContent.contentEditable = false;
        commentContent.textContent = oldCommentContent;
        [...commentInfoContainer.children].forEach((commentInfo) => {
          commentInfo.classList.remove("d-none");
        });

        comment.classList.remove("editing");
        editCommentCancelButton.classList.add("d-none");
        editCommentSaveButton.classList.add("d-none");
      });

      commentContent.contentEditable = true;
      commentContent.focus();

      // Place cursor at the end of the text content
      const range = document.createRange();
      const selection = window.getSelection();
      range.selectNodeContents(commentContent);
      range.collapse(false); // Collapse the range to the end point
      selection.removeAllRanges();
      selection.addRange(range);

      const postId = button.closest(".post-card").dataset.postId;

      editCommentSaveButton.addEventListener("click", async () => {
        try {
          const { content, status } = await this.fetchAPI(
            `/api/comments/${commentId}`,
            "PUT",
            {
              postId,
              comment: commentContent.textContent,
            },
          );

          if (status === 200) {
            commentContent.contentEditable = false;
            commentContent.textContent = content;
            [...commentInfoContainer.children].forEach((commentInfo) => {
              commentInfo.classList.remove("d-none");
            });

            editCommentCancelButton.classList.add("d-none");
            editCommentSaveButton.classList.add("d-none");
            comment.classList.remove("editing");

            const editCommentButton =
              commentInfoContainer.querySelector(".comment-edit");

            editCommentButton.textContent = "Edited";
            editCommentButton.classList.add("text-active");

            commentInfoContainer.querySelector(".date").textContent =
              "just now";
          }
        } catch (error) {
          console.error("Error from commentEditHandler: ", error);
        }
      });
    };
  }

  // report comment handler
  commentReportHandler(commentId) {
    return async (button) => {
      this.isReported = button.dataset.isReported.toLowerCase() === "true";

      if (this.isReported === true) return;

      try {
        const data = await this.fetchAPI(
          `/api/comments/${commentId}/reporting?isReport=${!this.isReported}`,
          "PUT",
        );

        if (data.status === 200) {
          this.isReported = !this.isReported;

          button.classList.add("text-error");

          button.textContent = "Reported";

          button.dataset.isReported = this.isReported.toString();
        }
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    };
  }

  // Setup button events
  setupCommentInteractionEvents(interactionButton, callbackFunction) {
    if (!interactionButton) return;

    // clone and replace to effectively remove multiple event listeners of the same node
    const newButton = interactionButton.cloneNode(true);
    interactionButton.parentNode.replaceChild(newButton, interactionButton);

    newButton.addEventListener("click", async () => {
      try {
        await callbackFunction(newButton);
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    });
  }

  // Post card setup
  setupCommentContainer(commentContainer) {
    const commentId = commentContainer
      .getAttribute("id")
      .split("-")
      .slice(1)
      .join("-");
    const commentInfoContainer =
      commentContainer.querySelector(".comment-info");

    const buttonsInfo = [
      {
        interactionSelector: ".comment-like",
        onClickFunction: this.commentLikeHandler,
      },
      {
        interactionSelector: ".comment-reply",
        onClickFunction: this.commentReplyHandler,
      },
      {
        interactionSelector: ".comment-delete",
        onClickFunction: this.commentDeleteHandler,
      },
      {
        interactionSelector: ".comment-edit",
        onClickFunction: this.commentEditHandler,
      },
      {
        interactionSelector: ".report-button",
        onClickFunction: this.commentReportHandler,
      },
    ];

    buttonsInfo.forEach(({ interactionSelector, onClickFunction }) => {
      let interactionButton;

      if (interactionSelector === ".report-button") {
        interactionButton = commentContainer.querySelector(interactionSelector);
      } else {
        interactionButton =
          commentInfoContainer.querySelector(interactionSelector);
      }

      const callBackFunction = onClickFunction(commentId);
      this.setupCommentInteractionEvents(interactionButton, callBackFunction);
    });
  }
}

export const onLoadCommentHandler = () => {
  const userId = document.querySelector(".current-user-id").dataset.userId;

  const commentHandler = new CommentHandler(userId);
  const commentContainers = document.querySelectorAll(".comment-container");

  commentContainers.forEach((commentContainer) =>
    commentHandler.setupCommentContainer(commentContainer),
  );
};

document.addEventListener("DOMContentLoaded", () => {
  onLoadCommentHandler();
});
