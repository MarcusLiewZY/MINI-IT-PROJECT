import { autoResizeTextarea } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const createPostPageButton = document.querySelector("#createPostPageButton");

  createPostPageButton?.addEventListener("click", () => {
    window.location.href = "/posts/new-post";
  });

  const postContent = document.querySelector("#postContent");

  autoResizeTextarea(postContent, 1000);
});
