import { fetchAPI } from "./utils.js";

class PostCardHandler {
  constructor(userId) {
    this.userId = userId;

    this.likeButtonHandler = this.likeButtonHandler.bind(this);
    this.bookmarkButtonHandler = this.bookmarkButtonHandler.bind(this);
    this.editButtonHandler = this.editButtonHandler.bind(this);
    this.deleteButtonHandler = this.deleteButtonHandler.bind(this);
  }

  likeButtonHandler(postId) {
    return async (button) => {
      let isPostLikedByUser =
        button.dataset.isPostLikedByUser.toLowerCase() === "true";
      const postCard = document.querySelector(
        `.post-card[data-post-id="${postId}"]`,
      );

      try {
        const { status } = await fetchAPI(
          `/api/posts/${postId}/interactions?isLike=${!isPostLikedByUser}`,
          "POST",
          null,
        );

        if (status !== 200) throw new Error("Liking post failed");

        isPostLikedByUser = !isPostLikedByUser;
        button.dataset.isPostLikedByUser = isPostLikedByUser.toString();

        const likeButton = postCard.querySelector(".like-button");
        const likeButtonIcon = likeButton.querySelector("svg");
        const likeButtonCount = postCard.querySelector(`#like-count-${postId}`);

        if (isPostLikedByUser) {
          likeButtonIcon.classList.add("liked");
          likeButtonCount.textContent =
            parseInt(likeButtonCount.textContent) + 1;

          likeButtonCount.parentNode.classList.add("text-active");
        } else {
          likeButtonIcon.classList.remove("liked");
          likeButtonCount.textContent = Math.max(
            0,
            parseInt(likeButtonCount.textContent) - 1,
          );
          likeButtonCount.parentNode.classList.remove("text-active");
        }

        likeButtonCount.nextElementSibling.textContent =
          likeButtonCount.textContent === "1" ? " like" : " likes";
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    };
  }

  bookmarkButtonHandler(postId) {
    return async (button) => {
      let isPostBookmarkedByUser =
        button.dataset.isPostBookmarkedByUser.toLowerCase() === "true";
      const postCard = document.querySelector(
        `.post-card[data-post-id="${postId}"]`,
      );

      try {
        const { status } = await fetchAPI(
          `/api/posts/${postId}/interactions?isBookmark=${!isPostBookmarkedByUser}`,
          "POST",
          null,
        );

        if (status !== 200) throw new Error("Bookmarking post failed");

        isPostBookmarkedByUser = !isPostBookmarkedByUser;
        button.dataset.isPostBookmarkedByUser =
          isPostBookmarkedByUser.toString();

        const bookmarkButton = postCard.querySelector(".bookmark-button");
        const bookmarkButtonIcon = bookmarkButton.querySelector("svg");

        if (isPostBookmarkedByUser) {
          bookmarkButtonIcon.classList.add("bookmarked");
        } else {
          bookmarkButtonIcon.classList.remove("bookmarked");
        }
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    };
  }

  editButtonHandler(postId) {
    return () => {
      // redirect user to edit post page
      window.location.href = `/posts/${postId}/edit-post`;
    };
  }

  deleteButtonHandler(postId) {
    return async () => {
      try {
        const data = await fetchAPI(`/api/posts/${postId}`, "DELETE", {
          isSoftDelete: true,
        });

        if (data.status === 200) {
          const postCard = document.querySelector(
            `.post-card[data-post-id="${postId}"]`,
          );

          if (postCard) {
            postCard.remove();
          }

          window.location.href = "/";
        }
      } catch (error) {
        console.error("Error from deleteButtonHandler: ", error);
      }
    };
  }

  // Setup button events
  setupButtonEvents(button, callbackFunction) {
    if (!button) return;

    // clone and replace to effectively remove multiple event listeners of the same node
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);

    newButton.addEventListener("click", async () => {
      try {
        await callbackFunction(newButton);
      } catch (error) {
        console.error("Error from Post Card buttons:", error);
      }
    });
  }

  // Post card setup
  setupPostCard(postCard) {
    const postId = postCard.dataset.postId;
    const reactContainer = postCard.querySelector(".react-container");

    const buttonsInfo = [
      {
        buttonSelector: ".like-button",
        onClickFunction: this.likeButtonHandler,
      },
      {
        buttonSelector: ".bookmark-button",
        onClickFunction: this.bookmarkButtonHandler,
      },
      {
        buttonSelector: ".edit-button",
        onClickFunction: this.editButtonHandler,
      },
      {
        buttonSelector: ".delete-button",
        onClickFunction: this.deleteButtonHandler,
      },
    ];

    buttonsInfo.forEach(({ buttonSelector, onClickFunction }) => {
      if (!reactContainer) return;
      const button = reactContainer.querySelector(buttonSelector);
      const callBackFunction = onClickFunction(postId);
      this.setupButtonEvents(button, callBackFunction);
    });
  }
}

export const autoResizeCommentInput = () => {
  const addCommentContainers = document.querySelectorAll(
    ".post-card__add-comment-container",
  );
  addCommentContainers.forEach((addCommentContainer) => {
    var commentInput = addCommentContainer.querySelector(".comment-input");
    const commentForm = addCommentContainer.querySelector("form");
    var submitButton = addCommentContainer.querySelector(
      ".submit-comment-button svg",
    );

    ["input", "focus"].forEach((e) => {
      commentInput.addEventListener(e, () => {
        commentInput.style.height = "auto";
        commentInput.style.maxHeight = "200px";
        commentInput.style.height = commentInput.scrollHeight + "px";
      });
    });

    commentForm.addEventListener("submit", () => {
      commentInput.style.height = "auto";
    });

    // var defaultImagePath = "/static/svg/send-gray.svg";
    // var activeImagePath = "/static/svg/send-blue.svg";

    ["focus", "input"].forEach((event) => {
      commentInput.addEventListener(event, () => {
        submitButton.classList.toggle("sent", commentInput.value.length > 0);
      });
    });

    commentInput.addEventListener("blur", () => {
      submitButton.classList.remove("sent");
    });
  });
};

export const postCardHandler = () => {
  const userId = document.querySelector(".current-user-id")?.dataset.userId;

  // if (!userId) return;

  const postCardHandler = new PostCardHandler(userId);
  const postCards = document.querySelectorAll(".post-card");

  postCards.forEach((postCard) => postCardHandler.setupPostCard(postCard));

  autoResizeCommentInput();
};

document.addEventListener("DOMContentLoaded", () => {
  postCardHandler();
});
