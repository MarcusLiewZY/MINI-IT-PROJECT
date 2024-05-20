// navigation and filter for notification page

const adminNotificationsMapping = [
  {
    id: "adminPageAllFilter",
    param: "all",
    supportedNotificationType: ["ApprovingPost", "ReportingComment"],
    counterId: "adminPageAllCount",
  },
  {
    id: "adminPageApprovingPostsFilter",
    param: "approving-posts",
    supportedNotificationType: ["ApprovingPost"],
    counterId: "adminPageApprovingCount",
  },
  {
    id: "adminPageReportingCommentsFilter",
    param: "reporting-comments",
    supportedNotificationType: ["ReportingComment"],
    counterId: "adminPageReportingCommentsCount",
  },
];

const adminNotificationFilterContainer = document.querySelector(
  ".admin-section .filter-container",
);

const adminNotificationFilter = () => {
  adminNotificationsMapping.forEach((item) => {
    const filterButton = adminNotificationFilterContainer?.querySelector(
      `#${item.id}`,
    );

    filterButton?.addEventListener("click", () => {
      window.location.href = `/admin?filter=${item.param}`;
    });
  });
};

document.addEventListener("DOMContentLoaded", () => {
  adminNotificationFilter();
});

// update notification status
// const notificationContentContainer = document.querySelector(
//   ".notification-section #notificationPageNotificationContentContainer",
// );

// const updateNotificationStatus = async (notificationId, notificationType) => {
//   try {
//     const response = await fetch(`/api/notifications/${notificationId}`, {
//       method: "PUT",
//       body: JSON.stringify({ type: notificationType }),
//       headers: {
//         "Content-Type": "application/json",
//       },
//     });

//     const { status, post_detail_url, post_status } = await response.json();

//     if (status === 200) {
//       window.open(post_detail_url, "_blank");
//     } else {
//       throw new Error("Error updating notification status");
//     }

//     return {
//       status,
//       post_detail_url,
//       postStatus: post_status || null,
//     };
//   } catch (error) {
//     console.error("Error updating notification status", error);
//   }
// };

// todo: reporting and approval features

class ReportingCommentHandler {
  constructor(userId) {
    this.userId = userId;

    this.allowReportedComment = this.allowReportedComment.bind(this);
    this.deleteReportedComment = this.deleteReportedComment.bind(this);
  }

  allowReportedComment(commentId) {
    return async () => {
      try {
        const response = await fetch(
          `/api/comments/${commentId}/reporting?isReport=false`,
          {
            method: "PUT",
            body: JSON.stringify({ userId: this.userId }),
            headers: {
              "Content-Type": "application/json",
            },
          },
        );

        const data = await response.json();

        return data.status === 200;
      } catch (error) {
        console.error("Error allowing reported comment", error);
      }
    };
  }

  deleteReportedComment(commentId) {
    return async () => {
      try {
        const response = await fetch(`/api/comments/${commentId}`, {
          method: "DELETE",
          body: JSON.stringify({ userId: this.userId }),
          headers: {
            "Content-Type": "application/json",
          },
        });

        return response.status === 204;
      } catch (error) {
        console.error("Error deleting reported comment", error);
      }
    };
  }

  setupReportingCommentHandler(reportingCommentContainer) {
    const reportingCommentId = reportingCommentContainer.getAttribute("id");

    const actionButtonContainer = reportingCommentContainer.querySelector(
      ".action-button-container",
    );

    const actionButton = [
      {
        interactionSelector: "#reportingCommentAllowButton",
        handler: this.allowReportedComment,
      },
      {
        interactionSelector: "#reportingCommentDeleteButton",
        handler: this.deleteReportedComment,
      },
    ];

    actionButton.forEach(({ interactionSelector, handler }) => {
      const button = actionButtonContainer?.querySelector(interactionSelector);

      if (!button) return;

      const buttonHandler = handler(reportingCommentId);

      button.addEventListener("click", async () => {
        try {
          button.disable = true;
          const isSuccess = await buttonHandler();

          if (isSuccess) {
            reportingCommentContainer.remove();
          } else {
            throw new Error("Error handling reporting comment");
          }
        } catch (error) {
          console.error("Error handling reporting comment", error);
        } finally {
          button.disable = false;
        }
      });
    });
  }
}

class ApprovingPostHandler {
  constructor(userId) {
    this.userId = userId;

    this.approvePost = this.approvePost.bind(this);
    this.rejectPost = this.rejectPost.bind(this);
  }

  approvePost(postId) {
    return async () => {
      try {
        const response = await fetch(`/api/posts/${postId}/post-status`, {
          method: "PUT",
          body: JSON.stringify({
            userId: this.userId,
            postStatus: "unread_approved",
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        return data.status === 200;
      } catch (error) {
        console.error("Error allowing reported comment", error);
      }
    };
  }

  rejectPost(postId) {
    return async () => {
      try {
        const response = await fetch(`/api/posts/${postId}/post-status`, {
          method: "PUT",
          body: JSON.stringify({
            userId: this.userId,
            postStatus: "unread_rejected",
          }),
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        return data.status === 200;
      } catch (error) {
        console.error("Error deleting reported comment", error);
      }
    };
  }

  setupApprovingPostHandler(approvingPostContainer) {
    const approvingPostId = approvingPostContainer.getAttribute("id");

    const actionButtonContainer = approvingPostContainer.querySelector(
      ".action-button-container",
    );

    const actionButton = [
      {
        interactionSelector: "#approvingPostApproveButton",
        handler: this.approvePost,
      },
      {
        interactionSelector: "#approvingPostRejectButton",
        handler: this.rejectPost,
      },
    ];

    actionButton.forEach(({ interactionSelector, handler }) => {
      const button = actionButtonContainer?.querySelector(interactionSelector);

      if (!button) return;

      const buttonHandler = handler(approvingPostId);

      button.addEventListener("click", async () => {
        try {
          button.disable = true;
          const isSuccess = await buttonHandler();

          console.log("isSuccess", isSuccess);

          if (isSuccess) {
            approvingPostContainer.remove();
          } else {
            throw new Error("Error handling reporting comment");
          }
        } catch (error) {
          console.error("Error handling reporting comment", error);
        } finally {
          button.disable = false;
        }
      });
    });
  }
}

const updateAdminNotificationCounter = (notificationType) => {
  adminNotificationsMapping.forEach(
    ({ supportedNotificationType, counterId }) => {
      const notificationCounter =
        adminNotificationFilterContainer?.querySelector(`#${counterId}`);

      if (
        !supportedNotificationType.includes(notificationType) ||
        !notificationCounter
      )
        return;

      const currentCount = parseInt(notificationCounter.textContent);

      notificationCounter.textContent = currentCount - 1;
      const newCount = parseInt(notificationCounter.textContent);

      if (newCount === 0) {
        notificationCounter.classList.add("d-none");
      } else if (newCount > 0) {
        notificationCounter.classList.remove("d-none");

        if (newCount > 99) notificationCounter.textContent = "99+";
      }

      return;
    },
  );
};

document.addEventListener("adminNotificationPaginationLoaded", () => {
  const adminNotificationContentContainer = document.querySelector(
    ".admin-section #adminPageAdminContentContainer",
  );

  const userId = document.querySelector(".current-user-id").dataset.userId;

  [...adminNotificationContentContainer?.children].forEach((notification) => {
    const notificationType = notification.getAttribute(
      "data-admin-notification-type",
    );

    if (!notificationType) return;

    if (notificationType === "ReportingComment") {
      const reportingCommentHandler = new ReportingCommentHandler(userId);
      reportingCommentHandler.setupReportingCommentHandler(notification);
    } else if (notificationType === "ApprovingPost") {
      const approvingPostHandler = new ApprovingPostHandler(userId);
      approvingPostHandler.setupApprovingPostHandler(notification);
    }
  });
});
