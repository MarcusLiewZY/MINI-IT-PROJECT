export const setConnectionLine = () => {
  var commentContainers = document.querySelectorAll(".comment-container");

  // set margin left of the comment container based on the comment level
  // if the comment level is 1, margin left is 0rem
  // else margin left is 2.5rem * (comment level - 1)
  commentContainers.forEach((commentContainer) => {
    var commentLevel = commentContainer.dataset.commentLevel;

    if (commentLevel > 0 && commentLevel <= 4) {
      let marginLeft = 2.5 * (commentLevel - 1);
      commentContainer.style.marginLeft = `${marginLeft}rem`;
    } else if (commentLevel > 4) {
      let marginLeft = 2.5 * 3.5;
      commentContainer.style.marginLeft = `${marginLeft}rem`;
      const avatar = commentContainer.querySelector(".avatar");
      avatar.style.scale = "0.8";
    }
  });

  commentContainers.forEach((commentContainer) => {
    var commentLevel = commentContainer.dataset.commentLevel;

    if (commentLevel <= 1 || commentLevel > 4) return;

    var avatarContainer = commentContainer.querySelector(".avatar-container");

    var previousCommentContainerHeight =
      commentContainer.previousElementSibling?.offsetHeight ||
      commentContainer.parentNode.previousElementSibling?.offsetHeight ||
      0;

    var avatarHeight = avatarContainer.querySelector(".avatar").offsetHeight;

    avatarContainer.classList.add("reply-avatar-container");

    var paddingBottomOfCommentContainer = 20;

    var connectLineLength = previousCommentContainerHeight - avatarHeight / 2;

    var offsetHeight = 8;

    var connectLineTopPosition =
      previousCommentContainerHeight -
      avatarHeight +
      paddingBottomOfCommentContainer +
      offsetHeight;

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
  });
};

// // comment connection line and avatar position
Array("resize", "load", "DOMContentLoaded").forEach((e) => {
  window.addEventListener(e, () => {
    setConnectionLine();
  });
});

// Create a new observer instance
let observer = new MutationObserver((mutations) => {
  // For each mutation
  mutations.forEach((mutation) => {
    // If the mutation is an addition of nodes
    if (mutation.type === "childList") {
      if (mutation.addedNodes.length > 0) {
        // Nodes added
        setConnectionLine();
      }

      if (mutation.removedNodes.length > 0) {
        // Nodes removed
        setConnectionLine();
      }
    }
  });
});

// Configuration of the observer
// childList: look for changes in the child elements of the target node
// subtree: look for changes in the target node and its descendants, not just direct children
let config = {
  childList: true,
  subtree: true,
};

// Pass in the target node (in this case, the whole document) and the observer options
let postCommentContainers = document.querySelectorAll(
  ".post-card__post-comment-container",
);

postCommentContainers.forEach((node) => {
  observer.observe(node, config);
});
