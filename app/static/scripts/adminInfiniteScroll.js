const adminNotificationFilterMapping = {
  all: "all",
  "reporting-comments": "reporting-comments",
  "approving-posts": "approving-posts",
};

const fetchAdminNotification = async (
  adminNotificationContainer,
  loadingContainer,
  param,
  adminNotificationBaseUrl,
  state,
) => {
  if (state.isLoading || !state.hasNextPage) return;

  loadingContainer.classList.remove("d-none");
  state.isLoading = true;

  try {
    const response = await fetch(
      `${adminNotificationBaseUrl}?filter=${param}&page=${state.page}&per_page=${state.perPage}`,
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
        adminNotificationContainer.insertBefore(
          tempDiv.firstChild,
          loadingContainer,
        );
      }

      state.hasNextPage = has_next;

      // create custom event to notify that the pagination is loaded
      const adminNotificationPaginationLoadedEvent = new Event(
        "adminNotificationPaginationLoaded",
      );
      document.dispatchEvent(adminNotificationPaginationLoadedEvent);
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

  const adminNotificationFilterContainer =
    document.querySelector(".admin-container");
  const adminNotificationContainer =
    adminNotificationFilterContainer?.querySelector(
      "#adminPageAdminContentContainer",
    );

  const param =
    adminNotificationFilterMapping[
      window.location.search.split("filter=")[1]
    ] || "";

  const baseUrl = "/api/paginate";
  const adminNotificationBaseUrl = `${baseUrl}/admin-notification`;

  if (!adminNotificationContainer || !param) {
    return;
  }

  const adminNotificationOnLoadInfiniteScroll = async (
    adminNotificationContainer,
    param,
    adminNotificationBaseUrl,
    state,
  ) => {
    const loadingContainer =
      adminNotificationContainer?.querySelector(".loading-container");

    try {
      await fetchAdminNotification(
        adminNotificationContainer,
        loadingContainer,
        param,
        adminNotificationBaseUrl,
        state,
      );
    } catch (error) {
      console.error(
        "Error from adminNotificationOnLoadInfiniteScroll: ",
        error,
      );
    }
  };

  const adminNotificationHandleScroll = (
    adminNotificationContainer,
    param,
    adminNotificationBaseUrl,
    state,
  ) => {
    if (
      !state.isLoading &&
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
    ) {
      state.page++;
      adminNotificationOnLoadInfiniteScroll(
        adminNotificationContainer,
        param,
        adminNotificationBaseUrl,
        state,
      );
    }
  };

  window.addEventListener("scroll", () => {
    adminNotificationHandleScroll(
      adminNotificationContainer,
      param,
      adminNotificationBaseUrl,
      state,
    );
  });

  adminNotificationOnLoadInfiniteScroll(
    adminNotificationContainer,
    param,
    adminNotificationBaseUrl,
    state,
  );
});
