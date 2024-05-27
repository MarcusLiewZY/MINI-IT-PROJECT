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

    const newComment = document.createElement("div");
    newComment.innerHTML = newCommentHTML;

    outermostCommentGroupContainer.appendChild(newComment);

    // if the current page is not the post detail page, return
    if (!(window.location.pathname === `/posts/${postId}`)) return;

    // navigate to the newly created comment
    newComment.scrollIntoView({ behavior: "smooth" });

    scrollToTopElement(createCommentFormContainer, 20);
  } catch (error) {
    console.error("Error from createCommentHandler:", error);
  } finally {
    isSubmitting = false;
    createCommentForm.disabled = false;
  }
};

export const onLoadCreateCommentHandler = () => {
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
        await onCreateCommentHandlerSubmit(e, createCommentFormObj);
      } catch (error) {
        console.error("Error from createCommentHandler:", error);
      }
    });
  });
};

["DOMContentLoaded", "postCardsPaginationLoaded"].forEach((e) => {
  document.addEventListener(e, () => {
    onLoadCreateCommentHandler();
  });
});
