const navigateMapping = [
  {
    id: "notificationPageAllNotificationsFilter",
    param: "all",
  },
  {
    id: "notificationPagePostNotificationsFilter",
    param: "posts",
  },
  {
    id: "notificationPageCommentNotificationsFilter",
    param: "comments",
  },
  {
    id: "notificationPagePostStatusFilter",
    param: "post-status",
  },
];

const notificationFilterContainer = document.querySelector(
  ".notification-section .filter-container",
);

const notificationFilter = () => {
  navigateMapping.forEach((item) => {
    const filterButton = notificationFilterContainer?.querySelector(
      `#${item.id}`,
    );

    filterButton?.addEventListener("click", () => {
      window.location.href = `/notifications?filter=${item.param}`;
    });
  });
};

document.addEventListener("DOMContentLoaded", () => {
  notificationFilter();
});
