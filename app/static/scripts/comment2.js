import { setConnectionLine } from "./connectionLine.js";
import { autoResizeCommentInput } from "./postCardHandler.js";
import { fetchAPI, scrollToTopElement } from "./utils.js";

export class CommentHandler {
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
    try {
      const { status } = await fetchAPI(
        `/api/comments/${this.commentId}`,
        "DELETE",
      );

      if (status !== 200) throw new Error("Failed to delete the comment");

      this.deleteCommentButton
        .closest(".comment-container")
        .classList.add("d-none");

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

    // if the current page is not the post detail page, return
    if (!(window.location.pathname === `/posts/${postId}`)) return;

    // navigate to the newly created comment
    newComment.scrollIntoView({ behavior: "smooth" });

    scrollToTopElement(createCommentFormContainer, 20);

    return newComment;
  } catch (error) {
    console.error("Error from createCommentHandler:", error);
  } finally {
    isSubmitting = false;
    createCommentForm.disabled = false;
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

        // initialize the comment handler for the new comment
        new CommentHandler(newComment);
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
  const commentId = commentContainer.id.split("-").slice(1).join("-");
  const commentInfoContainer = commentContainer.querySelector(".comment-info");
  const commentReplyButton =
    commentInfoContainer.querySelector(".comment-reply");
  const isCommentRepliedByUser =
    commentReplyButton.dataset.isCommentRepliedByUser.toLowerCase() === "true";

  let commentReplyFormContainer = commentReplyButton
    ?.closest(".comment-container")
    ?.querySelector(".reserve-elements + .reserve-element.comment-form");

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
    commentReplyButton.classList.add("d-none");
  };

  const handleReplyCancelButtonClick = () => {
    commentReplyForm.reset();
    commentReplyFormContainer.classList.add("d-none");
    commentReplyButton.classList.remove("d-none");
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

    // todo: test for second pages
    onCommentReplyHandler();
  });
});
