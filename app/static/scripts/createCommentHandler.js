import { insertLineBreaks } from "./utils.js";
import { autoResizeCommentInput } from "./postCardHandler.js";

const createCommentHandler = async (formData, postId) => {
  const userId = document.querySelector(".current-user-id").dataset.userId;
  try {
    const { comment } = Object.fromEntries(formData.entries());

    const response = await fetch("/api/comments", {
      method: "POST",
      body: JSON.stringify({ comment, postId }),
      headers: {
        "Content-type": "application/json",
      },
    });

    const { status, comment_id, content } = await response.json();

    if (status === 201) {
      const postCard = document.querySelector(
        `.post-card[data-post-id="${postId}"]`,
      );

      const newComment = postCard
        .querySelector(".reserve-elements .comment-group-container")
        .cloneNode(true);
      newComment.id = `comment-${comment_id}`;
      newComment.dataset.currentUserId = userId;
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

      postCard
        .querySelector(".comment-group-container")
        .appendChild(newComment);

      return newComment;
    }
  } catch (error) {
    console.error("Error from createCommentHandler:", error);
    return null;
  }
};

const commentLikeHandler = (commentId) => async (button) => {
  let isCommentLikedByUser =
    button.dataset.isCommentLikedByUser.toLowerCase() === "true";
  const userId = document.querySelector(".current-user-id").dataset.userId;

  try {
    const response = await fetch(
      `/api/comments/${commentId}?isLike=${!isCommentLikedByUser}`,
      {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
      },
    );

    const data = await response.json();

    if (data[0].status === 200) {
      const likeCommentCount = document.querySelector(
        `#like-count-${commentId}`,
      );
      if (isCommentLikedByUser) {
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

      isCommentLikedByUser = !isCommentLikedByUser;
      button.dataset.isCommentLikedByUser = isCommentLikedByUser.toString();
    }
  } catch (error) {
    console.error("Error from likeButtonHandler:", error);
  }
};

var commentReplyHandler = (commentId) => () => {
  console.log(commentId);
};

// Setup button events
const setupCommentInteractionEvents = (interactionButton, callbackFunction) => {
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
};

// Post card setup
const setupCommentContainer = (commentContainer) => {
  const commentId = commentContainer
    .getAttribute("id")
    .split("-")
    .slice(1)
    .join("-");
  const commentInfoContainer = commentContainer.querySelector(".comment-info");

  const buttonsInfo = [
    {
      interactionSelector: ".comment-like",
      onClickFunction: commentLikeHandler,
    },
    {
      interactionSelector: ".comment-reply",
      onClickFunction: commentReplyHandler,
    },
  ];

  buttonsInfo.forEach(({ interactionSelector, onClickFunction }) => {
    const interactionButton =
      commentInfoContainer.querySelector(interactionSelector);
    const callBackFunction = onClickFunction(commentId);
    setupCommentInteractionEvents(interactionButton, callBackFunction);
  });
};

export const onLoadCreateCommentHandler = () => {
  const createCommentFormContainers = document.querySelectorAll(
    ".post-card__add-comment-container",
  );

  autoResizeCommentInput();

  createCommentFormContainers.forEach((createCommentFormContainer) => {
    const postId =
      createCommentFormContainer.closest(".post-card").dataset.postId;

    const createCommentForm = createCommentFormContainer.querySelector(
      `#comment-form-${postId}`,
    );

    createCommentForm.addEventListener("submit", async (e) => {
      try {
        e.preventDefault();
        const formData = new FormData(createCommentForm);
        const newCommentContainer = await createCommentHandler(
          formData,
          postId,
        );

        if (newCommentContainer) {
          createCommentForm.querySelector("textarea[name='comment']").value =
            "";
          // const newComment = newCommentContainer.querySelector(".comment-container");
          setupCommentContainer(newCommentContainer);
        }
      } catch (error) {
        console.error("Error from createCommentHandler:", error);
      }
    });
  });
};

document.addEventListener("DOMContentLoaded", () => {
  onLoadCreateCommentHandler();
});
