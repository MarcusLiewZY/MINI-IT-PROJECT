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
    counterId: "adminPageApprovingPagesCount",
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

class ReportingCommentHandler {
  constructor(userId, notificationType) {
    this.userId = userId;
    this.notificationType = notificationType;

    this.allowReportedComment = this.allowReportedComment.bind(this);
    this.deleteReportedComment = this.deleteReportedComment.bind(this);
    this.setupHandler = this.setupHandler.bind(this);
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

  setupHandler(reportingCommentContainer) {
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
            updateAdminNotificationCounter(this.notificationType);
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
  constructor(userId, notificationType) {
    this.userId = userId;
    this.notificationType = notificationType;

    this.approvePost = this.approvePost.bind(this);
    this.rejectPost = this.rejectPost.bind(this);
    this.setupHandler = this.setupHandler.bind(this);
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

  setupHandler(approvingPostContainer) {
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

          if (isSuccess) {
            approvingPostContainer.remove();
            updateAdminNotificationCounter(this.notificationType);
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

document.addEventListener("adminNotificationPaginationLoaded", () => {
  const adminNotificationContentContainer = document.querySelector(
    ".admin-section #adminPageAdminContentContainer",
  );

  const userId = document.querySelector(".current-user-id").dataset.userId;

  const notificationHandlers = {
    ReportingComment: ReportingCommentHandler,
    ApprovingPost: ApprovingPostHandler,
  };

  [...adminNotificationContentContainer?.children].forEach(
    async (notification) => {
      try {
        const notificationType = notification.getAttribute(
          "data-admin-notification-type",
        );

        const Handler = notificationHandlers[notificationType];

        if (!Handler) return;

        const handler = new Handler(userId, notificationType);
        const isSuccess = await handler.setupHandler(notification);

        if (!isSuccess) return;

        updateAdminNotificationCounter(notificationType);
      } catch (error) {
        console.error("Error updating notification status", error);
      }
    },
  );
});
