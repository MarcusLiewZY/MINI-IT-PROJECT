import { setConnectionLine } from "./connectionLine.js";
import { postCardHandler } from "./postCardHandler.js";
// import { onLoadCreateCommentHandler } from "./createCommentHandler.js";
// import { onLoadCommentHandler } from "./comment2.js";

const baseUrl = "/api/paginate";
const meBaseUrl = `${baseUrl}/me`;

const pageMapping = {
  "/": {
    postContainerId: "mainPagePostCardContainer",
    apiPaginateUrl: `${baseUrl}/post-list`,
  },
  "/me/posts": {
    postContainerId: "myPageCreatedPostCardContainer",
    apiPaginateUrl: `${meBaseUrl}/created-post-list`,
  },
  "/me/likes": {
    postContainerId: "myPageLikedPostCardContainer",
    apiPaginateUrl: `${meBaseUrl}/liked-post-list`,
  },
  "/me/replies": {
    postContainerId: "myPageRepliesPostCardContainer",
    apiPaginateUrl: `${meBaseUrl}/replies-post-list`,
  },
  "/me/bookmarks": {
    postContainerId: "myPageBookmarkedPostCardContainer",
    apiPaginateUrl: `${meBaseUrl}/bookmarked-post-list`,
  },
  "/me/rejected-posts": {
    postContainerId: "myPageRejectedPostCardContainer",
    apiPaginateUrl: `${meBaseUrl}/rejected-post-list`,
  },
};

const fetchPosts = async (
  postContainer,
  loadingContainer,
  apiPaginateUrl,
  state,
) => {
  if (state.isLoading || !state.hasNextPage) return;

  loadingContainer.classList.remove("d-none");
  state.isLoading = true;

  try {
    const response = await fetch(
      `${apiPaginateUrl}?page=${state.page}&per_page=${state.perPage}`,
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
        postContainer.insertBefore(tempDiv.firstChild, loadingContainer);
      }

      state.hasNextPage = has_next;
    }

    // create custom event to notify that the pagination is loaded
    const postCardsPaginationLoaded = new Event("postCardsPaginationLoaded");
    document.dispatchEvent(postCardsPaginationLoaded);
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
    perPage: 5,
    isLoading: false,
    hasNextPage: true,
  };

  const pageData = pageMapping[window.location.pathname] || {};
  const { postContainerId, apiPaginateUrl } = pageData;

  if (!postContainerId || !apiPaginateUrl) {
    return;
  }

  const onLoadInfiniteScroll = async (
    postContainerId,
    apiPaginateUrl,
    state,
  ) => {
    const postContainer = document.querySelector(`#${postContainerId}`);
    const loadingContainer = postContainer?.querySelector(".loading-container");

    try {
      await fetchPosts(postContainer, loadingContainer, apiPaginateUrl, state);
      postCardHandler();
      // onLoadCreateCommentHandler();
      // onLoadCommentHandler();
      setConnectionLine();
    } catch (error) {
      console.error("Error from onLoadInfiniteScroll: ", error);
    }
  };

  const handleScroll = (postContainerId, apiPaginateUrl, state) => {
    if (
      !state.isLoading &&
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
    ) {
      state.page++;
      onLoadInfiniteScroll(postContainerId, apiPaginateUrl, state);
    }
  };

  window.addEventListener("scroll", () => {
    handleScroll(postContainerId, apiPaginateUrl, state);
  });

  onLoadInfiniteScroll(postContainerId, apiPaginateUrl, state);
});
