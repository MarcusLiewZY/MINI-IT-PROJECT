import { setConnectionLine } from "./connectionLine.js";
import { postCardHandler } from "./postCardHandler.js";
import { onLoadCreateCommentHandler } from "./createCommentHandler.js";
import { onLoadCommentHandler } from "./commentHandler.js";

document.addEventListener("DOMContentLoaded", () => {
  let page = 1;
  const perPage = 5;
  let isLoading = false;
  let hasNextPage = true;
  const postContainer = document.querySelector("#mainPagePostCardContainer");
  const loadingContainer = postContainer?.querySelector(".loading-container");

  const fetchPosts = async (page) => {
    if (isLoading || !hasNextPage) return;

    // console.log(isLoading);
    loadingContainer.classList.remove("d-none");
    isLoading = true;

    try {
      const response = await fetch(
        `/api/paginate/postList?page=${page}&per_page=${perPage}`,
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

        hasNextPage = has_next;
      }
    } catch (error) {
      console.error(error);
    } finally {
      isLoading = false;
      loadingContainer.classList.add("d-none");
    }
  };

  const onLoadInfiniteScroll = async (page) => {
    try {
      await fetchPosts(page);
      postCardHandler();
      onLoadCreateCommentHandler();
      onLoadCommentHandler();
      setConnectionLine();
    } catch (error) {
      console.error("Error from onLoadInfiniteScroll: ", error);
    }
  };

  const handleScroll = () => {
    if (
      !isLoading &&
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100
    ) {
      page++;
      onLoadInfiniteScroll(page);
    }
  };

  window.addEventListener("scroll", handleScroll);

  onLoadInfiniteScroll(page);
});
