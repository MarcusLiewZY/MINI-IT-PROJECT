import { scrollToTopElement } from "./utils.js";

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

    const { status, html, has_next, page } = await response.json();

    if (status === 200) {
      // if there is no notification
      if (!has_next && page === 1 && html === "") {
        const notResourceHandlerContainer = notificationContainer.querySelector(
          ".no-resource-handler-container",
        );
        if (notResourceHandlerContainer) {
          notResourceHandlerContainer.classList.remove("d-none");
        }
      }

      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = html;

      while (tempDiv.firstChild) {
        notificationContainer.insertBefore(
          tempDiv.firstChild,
          loadingContainer,
        );
      }

      state.hasNextPage = has_next;

      // create custom event to notify that the pagination is loaded
      const notificationPaginationLoadedEvent = new Event(
        "notificationPaginationLoaded",
      );
      document.dispatchEvent(notificationPaginationLoadedEvent);
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

  const baseUrl = "api/paginate";
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

  const isLoadAllPostStatus = sessionStorage.getItem("isLoadAllPostStatus");

  const onLoadAllPostStatus = async () => {
    try {
      await notificationOnLoadInfiniteScroll(
        notificationContainer,
        "post-status",
        notificationBaseUrl,
        {
          page: 1,
          perPage: 10000,
          isLoading: false,
          hasNextPage: true,
        },
      );

      sessionStorage.removeItem("isLoadAllPostStatus");

      // get the post id from the url and scroll to that post
      const postId = window.location.hash.split("#")[1];

      if (!postId) return;

      const postElement = document.getElementById(postId);

      if (!postElement) return;

      if (notificationContainer.offsetHeight <= window.innerHeight) return;

      postElement.scrollIntoView({ behavior: "smooth" });
      scrollToTopElement(document, 0, 8000);
    } catch (error) {
      console.error("Error from onLoadAllPostStatus: ", error);
    }
  };

  if (isLoadAllPostStatus) {
    onLoadAllPostStatus();
    return;
  }

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
