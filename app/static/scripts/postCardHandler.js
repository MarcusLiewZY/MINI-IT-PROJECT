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

// react buttons hover effect
var reactContainers = document.querySelectorAll(".react-container");

reactContainers.forEach((reactContainer) => {
  var buttonsInfo = [
    {
      buttonSelector: ".like-button",
      defaultImagePath: "static/svg/like.svg",
      hoverImagePath: "static/svg/like-blue.svg",
    },
    {
      buttonSelector: ".bookmark-button",
      defaultImagePath: "static/svg/bookmark-gray.svg",
      hoverImagePath: "static/svg/bookmark-brown.svg",
    },
    {
      buttonSelector: ".edit-button",
      defaultImagePath: "static/svg/edit-gray.svg",
      hoverImagePath: "static/svg/edit-blue.svg",
    },
    {
      buttonSelector: ".delete-button",
      defaultImagePath: "static/svg/bin-gray.svg",
      hoverImagePath: "static/svg/bin-red.svg",
    },
  ];

  var setupButtonEvents = (
    buttonSelector,
    defaultImagePath,
    hoverImagePath,
  ) => {
    var button = reactContainer.querySelector(buttonSelector);
    var buttonImg = reactContainer.querySelector(`${buttonSelector} img`);

    button.addEventListener("mouseover", () => {
      buttonImg.src = hoverImagePath;
    });

    button.addEventListener("mouseout", () => {
      buttonImg.src = defaultImagePath;
    });
  };

  buttonsInfo.forEach(
    ({ buttonSelector, defaultImagePath, hoverImagePath }) => {
      setupButtonEvents(buttonSelector, defaultImagePath, hoverImagePath);
    },
  );
});
