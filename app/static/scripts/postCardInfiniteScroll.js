import { setConnectionLine } from "./connectionLine.js";
import { postCardHandler } from "./postCardHandler.js";
import { fetchAPI } from "./utils.js";

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
  "/results": {
    postContainerId: "searchPostCardContainer",
    apiPaginateUrl: `${baseUrl}/search-post-list`,
  },
};

const getExtraParams = () => {
  const extraParams = new URLSearchParams(window.location.search);

  // convert the extraParams to object
  let extraParamsObj = {};
  for (const [key, value] of extraParams) {
    if (key === "page" || key === "per_page") return;
    extraParamsObj[key] = value;
  }

  return extraParamsObj;
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
    const params = new URLSearchParams();

    params.append("page", state.page);
    params.append("per_page", state.perPage);

    const extraParamsObj = getExtraParams();

    Object.entries(extraParamsObj).forEach(([key, value]) => {
      params.append(key, value);
    });

    const queryString = params.toString();

    const { status, html, has_next } = await fetchAPI(
      `${apiPaginateUrl}?${queryString}`,
      "GET",
      null,
    );

    if (status === 200) {
      // if there is no result for the first page
      if (!state.has_next && state.page === 1) {
        const notResourceHandlerContainer = postContainer.querySelector(
          ".no-resource-handler-container",
        );
        if (notResourceHandlerContainer) {
          notResourceHandlerContainer.classList.remove("d-none");
        }
      }

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

  // set the search text to the search input
  const postSearchFormInput = document.querySelector("#postSearchInput");

  if (postSearchFormInput) {
    postSearchFormInput.value = new URLSearchParams(window.location.search).get(
      "search_text",
    );
  }
});
