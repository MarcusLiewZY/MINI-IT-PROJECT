class PostCardHandler {
  constructor(userId) {
    this.userId = userId;

    this.likeButtonHandler = this.likeButtonHandler.bind(this);
    this.bookmarkButtonHandler = this.bookmarkButtonHandler.bind(this);
    this.editButtonHandler = this.editButtonHandler.bind(this);
    this.deleteButtonHandler = this.deleteButtonHandler.bind(this);
  }

  async fetchAPI(url, method, body = null) {
    try {
      const response = await fetch(url, {
        method: method,
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      return data;
    } catch (error) {
      console.error("Error from fetchAPI: ", error);
    }
  }

  likeButtonHandler(postId) {
    return async (button) => {
      let isPostLikedByUser =
        button.dataset.isPostLikedByUser.toLowerCase() === "true";
      const postCard = document.querySelector(
        `.post-card[data-post-id="${postId}"]`,
      );

      try {
        const data = await this.fetchAPI(
          `/api/posts/${postId}/interactions?isLike=${!isPostLikedByUser}`,
          "POST",
          null,
        );

        if (data[0].status === 200) {
          const likeButton = postCard.querySelector(".like-button");
          const likeButtonImg = likeButton.querySelector("img");
          const likeButtonCount = postCard.querySelector(
            `#like-count-${postId}`,
          );

          if (isPostLikedByUser) {
            likeButtonImg.src = "/static/svg/like.svg";
            likeButtonCount.textContent = Math.max(
              0,
              parseInt(likeButtonCount.textContent) - 1,
            );
          } else {
            likeButtonImg.src = "/static/svg/like-blue.svg";
            likeButtonCount.textContent =
              parseInt(likeButtonCount.textContent) + 1;
          }

          isPostLikedByUser = !isPostLikedByUser;
          button.dataset.isPostLikedByUser = isPostLikedByUser.toString();
        }
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
        const data = await this.fetchAPI(
          `/api/posts/${postId}/interactions?isBookmark=${!isPostBookmarkedByUser}`,
          "POST",
          null,
        );

        if (data[0].status === 200) {
          const bookmarkButton = postCard.querySelector(".bookmark-button");
          const bookmarkButtonImg = bookmarkButton.querySelector("img");

          if (isPostBookmarkedByUser) {
            bookmarkButtonImg.src = "/static/svg/bookmark-gray.svg";
          } else {
            bookmarkButtonImg.src = "/static/svg/bookmark-brown.svg";
          }

          isPostBookmarkedByUser = !isPostBookmarkedByUser;
          button.dataset.isPostBookmarkedByUser =
            isPostBookmarkedByUser.toString();
        }
      } catch (error) {
        console.error("Error from likeButtonHandler:", error);
      }
    };
  }

  editButtonHandler(postId) {
    return () => {
      // redirect user to edit post page: /posts/:postId
      const path = `/posts/${postId}`;
      const editPostModal = document.querySelector("#editPostModal");

      if (window.location.pathname === path) {
        editPostModal.showModal();
      } else {
        window.location.href = `${path}?isEdit=true`;
      }
    };
  }

  deleteButtonHandler(postId) {
    return async () => {
      try {
        const data = await this.fetchAPI(`/api/posts/${postId}`, "DELETE", {
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
  setupButtonEvents(
    button,
    defaultImagePath,
    hoverImagePath,
    callbackFunction,
  ) {
    if (!button) return;

    // clone and replace to effectively remove multiple event listeners of the same node
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);

    const buttonImg = newButton.querySelector("img");

    newButton.addEventListener("mouseover", () => {
      buttonImg.src = hoverImagePath;
    });

    newButton.addEventListener("mouseout", () => {
      const isPostLikedByUser =
        newButton.dataset?.isPostLikedByUser?.toLowerCase() === "true";
      const isPostBookmarkedByUser =
        newButton.dataset?.isPostBookmarkedByUser?.toLowerCase() === "true";

      if (isPostLikedByUser && newButton.classList.contains("like-button")) {
        buttonImg.src = hoverImagePath;
      } else if (
        isPostBookmarkedByUser &&
        newButton.classList.contains("bookmark-button")
      ) {
        buttonImg.src = hoverImagePath;
      } else {
        buttonImg.src = defaultImagePath;
      }
    });

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
        defaultImagePath: "/static/svg/like.svg",
        hoverImagePath: "/static/svg/like-blue.svg",
        onClickFunction: this.likeButtonHandler,
      },
      {
        buttonSelector: ".bookmark-button",
        defaultImagePath: "/static/svg/bookmark-gray.svg",
        hoverImagePath: "/static/svg/bookmark-brown.svg",
        onClickFunction: this.bookmarkButtonHandler,
      },
      {
        buttonSelector: ".edit-button",
        defaultImagePath: "/static/svg/edit-gray.svg",
        hoverImagePath: "/static/svg/edit-blue.svg",
        onClickFunction: this.editButtonHandler,
      },
      {
        buttonSelector: ".delete-button",
        defaultImagePath: "/static/svg/bin-gray.svg",
        hoverImagePath: "/static/svg/bin-red.svg",
        onClickFunction: this.deleteButtonHandler,
      },
    ];

    buttonsInfo.forEach(
      ({
        buttonSelector,
        defaultImagePath,
        hoverImagePath,
        onClickFunction,
      }) => {
        const button = reactContainer.querySelector(buttonSelector);
        const callBackFunction = onClickFunction(postId);
        this.setupButtonEvents(
          button,
          defaultImagePath,
          hoverImagePath,
          callBackFunction,
        );
      },
    );
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
      ".submit-comment-button img",
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

    var defaultImagePath = "/static/svg/send-gray.svg";
    var activeImagePath = "/static/svg/send-blue.svg";

    ["focus", "input"].forEach((event) => {
      commentInput.addEventListener(event, () => {
        submitButton.src = commentInput.value
          ? activeImagePath
          : defaultImagePath;
      });
    });

    commentInput.addEventListener("blur", () => {
      submitButton.src = defaultImagePath;
    });
  });
};

export const postCardHandler = () => {
  const userId = document.querySelector(".current-user-id").dataset.userId;

  const postCardHandler = new PostCardHandler(userId);
  const postCards = document.querySelectorAll(".post-card");

  postCards.forEach((postCard) => postCardHandler.setupPostCard(postCard));

  autoResizeCommentInput();
};

document.addEventListener("DOMContentLoaded", () => {
  postCardHandler();
});
