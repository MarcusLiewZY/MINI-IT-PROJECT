const notificationFilterMapping = {
  all: "all",
  posts: "posts",
  comments: "comments",
  "post-status": "post-status",
};

const fetchNotifications = async (
  notificationContainer,
  loadingContainer,
  param,
  notificationBaseUrl,
  state,
) => {
  if (state.isLoading || !state.hasNextPage) return;

  loadingContainer.classList.remove("d-none");
  state.isLoading = true;

  try {
    const response = await fetch(
      `${notificationBaseUrl}?filter=${param}&page=${state.page}&per_page=${state.perPage}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

    const { status, html, has_next } = await response.json();

    if (status === 200) {
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = html;

      while (tempDiv.firstChild) {
        notificationContainer.insertBefore(
          tempDiv.firstChild,
          loadingContainer,
        );
      }

      state.hasNextPage = has_next;
    }
  } catch (error) {
    console.error(error);
  } finally {
    state.isLoading = false;
    loadingContainer.classList.add("d-none");
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const state = {
    page: 1,
    perPage: 10,
    isLoading: false,
    hasNextPage: true,
  };

  const notificationFilterContainer = document.querySelector(
    ".notification-container",
  );
  const notificationContainer = notificationFilterContainer?.querySelector(
    "#notificationPageNotificationContentContainer",
  );

  const param =
    notificationFilterMapping[window.location.search.split("filter=")[1]] || "";

  const baseUrl = "/api/paginate";
  const notificationBaseUrl = `${baseUrl}/notification`;

  if (!notificationContainer || !param) {
    return;
  }

  const notificationOnLoadInfiniteScroll = async (
    notificationContainer,
    param,
    notificationBaseUrl,
    state,
  ) => {
    const loadingContainer =
      notificationContainer?.querySelector(".loading-container");

    try {
      await fetchNotifications(
        notificationContainer,
        loadingContainer,
        param,
        notificationBaseUrl,
        state,
      );
    } catch (error) {
      console.error("Error from notificationOnLoadInfiniteScroll: ", error);
    }
  };

  const notificationHandleScroll = (
    notificationContainer,
    param,
    notificationBaseUrl,
    state,
  ) => {
    if (
      !state.isLoading &&
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
    ) {
      state.page++;
      notificationOnLoadInfiniteScroll(
        notificationContainer,
        param,
        notificationBaseUrl,
        state,
      );
    }
  };

  window.addEventListener("scroll", () => {
    notificationHandleScroll(
      notificationContainer,
      param,
      notificationBaseUrl,
      state,
    );
  });

  notificationOnLoadInfiniteScroll(
    notificationContainer,
    param,
    notificationBaseUrl,
    state,
  );
});
