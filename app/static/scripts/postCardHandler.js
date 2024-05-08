// comment input auto resize
var addCommentContainers = document.querySelectorAll(
  ".post-card__add-comment-container",
);
addCommentContainers.forEach((addCommentContainer) => {
  var commentInput = addCommentContainer.querySelector(".comment-input");
  var submitButton = addCommentContainer.querySelector(
    ".submit-comment-button img",
  );

  commentInput.addEventListener("input", () => {
    commentInput.style.height = "auto";
    commentInput.style.maxHeight = "200px";
    commentInput.style.height = commentInput.scrollHeight + "px";
  });

  var defaultImagePath = "static/svg/send-gray.svg";
  var activeImagePath = "static/svg/send-blue.svg";

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

// todo: add the comments for the following code
// comment connection line and avatar position
Array("resize", "load").forEach((e) => {
  window.addEventListener(e, () => {
    var commentContainers = document.querySelectorAll(".comment-container");

    // set margin left of the comment container based on the comment level
    // if the comment level is 1, margin left is 0rem
    // else margin left is 2.5rem * (comment level - 1)
    commentContainers.forEach((commentContainer) => {
      var commentLevel = commentContainer.getAttribute("data-commentLevel");

      if (commentLevel > 0 && commentLevel <= 3) {
        let marginLeft = 2.5 * (commentLevel - 1);
        commentContainer.style.marginLeft = `${marginLeft}rem`;
      }
    });

    commentContainers.forEach((commentContainer) => {
      var commentLevel = commentContainer.getAttribute("data-commentLevel");

      if (commentLevel > 1) {
        var avatarContainer =
          commentContainer.querySelector(".avatar-container");

        var previousCommentContainerHeight =
          commentContainer.previousElementSibling?.offsetHeight || 0;

        var avatarHeight =
          avatarContainer.querySelector(".avatar").offsetHeight;

        avatarContainer.classList.add("reply-avatar-container");

        var paddingBottomOfCommentContainer = 20;

        var connectLineLength =
          previousCommentContainerHeight - avatarHeight / 2;

        var offsetHeight = 8;

        var connectLineTopPosition =
          previousCommentContainerHeight -
          avatarHeight +
          paddingBottomOfCommentContainer +
          offsetHeight;

        avatarContainer.style.setProperty(
          "--before-height",
          `${connectLineLength + paddingBottomOfCommentContainer + offsetHeight}px`,
        );

        avatarContainer.style.setProperty(
          "--before-top",
          `-${connectLineTopPosition}px`,
        );
      }
    });
  });
});

// react buttons handler
// Event handler
var reactButtonHandler = (postId) => () =>
  console.log(`button clicked on post ${postId}`);

// Setup button events
var setupButtonEvents = (
  button,
  defaultImagePath,
  hoverImagePath,
  callbackFunction,
) => {
  if (!button) return;

  // clone and replace to effectively remove multiple event listeners of the same node
  const newButton = button.cloneNode(true);
  button.parentNode.replaceChild(newButton, button);

  const buttonImg = newButton.querySelector("img");

  newButton.addEventListener("click", callbackFunction);
  newButton.addEventListener("mouseover", () => {
    buttonImg.src = hoverImagePath;
  });
  newButton.addEventListener("mouseout", () => {
    buttonImg.src = defaultImagePath;
  });
};

// Post card setup
var setupPostCard = (postCard) => {
  const postId = postCard.dataset.postId;
  const reactContainer = postCard.querySelector(".react-container");

  const buttonsInfo = [
    {
      buttonSelector: ".like-button",
      defaultImagePath: "/static/svg/like.svg",
      hoverImagePath: "/static/svg/like-blue.svg",
    },
    {
      buttonSelector: ".bookmark-button",
      defaultImagePath: "/static/svg/bookmark-gray.svg",
      hoverImagePath: "/static/svg/bookmark-brown.svg",
    },
    {
      buttonSelector: ".edit-button",
      defaultImagePath: "/static/svg/edit-gray.svg",
      hoverImagePath: "/static/svg/edit-blue.svg",
    },
    {
      buttonSelector: ".delete-button",
      defaultImagePath: "/static/svg/bin-gray.svg",
      hoverImagePath: "/static/svg/bin-red.svg",
    },
  ];

  buttonsInfo.forEach(
    ({ buttonSelector, defaultImagePath, hoverImagePath }) => {
      const button = reactContainer.querySelector(buttonSelector);
      const callbackFunction = reactButtonHandler(postId);
      setupButtonEvents(
        button,
        defaultImagePath,
        hoverImagePath,
        callbackFunction,
      );
    },
  );
};

document.addEventListener("DOMContentLoaded", () => {
  const postCards = document.querySelectorAll(".post-card");
  postCards.forEach(setupPostCard);
});
