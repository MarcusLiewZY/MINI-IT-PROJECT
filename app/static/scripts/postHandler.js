import { autoResizeTextarea, fetchAPI } from "./utils.js";

class MultiSelectDropdownMenu {
  constructor(postForm) {
    this.postTagContainer = postForm.querySelector(
      ".post-tag-container.post-tag-dropdown",
    );
    this.isDropdownOpen = false;
    this.dropdownButton = postForm.querySelector("#postTagDropDownButton");
    this.dropdownMenu = postForm.querySelector(".dropdown-content");
    this.badgeContainer = postForm.querySelector("#postTagBadgeContainer");
    this.dropdownSearch = postForm.querySelector("#postTagDropDownSearch");
    this.dropdownList = postForm.querySelector("#postTagDropDownList");

    this.selectedItemsOrder = []; // Store the order of selected items
    this.eventListeners = {}; // Store references to added event listeners

    this.init();
  }

  init = () => {
    this.dropdownSearch.addEventListener("keyup", this.filterItems);
    this.dropdownButton.addEventListener("click", this.toggleDropdown);
    document.addEventListener("click", this.closeDropdown);
    this.dropdownList.querySelectorAll("li").forEach((li) => {
      li.addEventListener("click", this.toggleItem);
    });

    // Add event listeners and store their references
    this.addEventListeners([
      {
        element: this.dropdownSearch,
        event: "keyup",
        handler: this.filterItems,
      },
      {
        element: this.dropdownButton,
        event: "click",
        handler: this.toggleDropdown,
      },
      { element: document, event: "click", handler: this.closeDropdown },
    ]);

    this.updateStateFromLoadedItems();
  };

  addEventListeners = (listeners) => {
    listeners.forEach(({ element, event, handler }) => {
      element.addEventListener(event, handler);
      this.eventListeners[event] = this.eventListeners[event] || [];
      this.eventListeners[event].push({ element, handler });
    });
  };

  removeEventListeners = () => {
    Object.entries(this.eventListeners).forEach(([event, listeners]) => {
      listeners.forEach(({ element, handler }) => {
        element.removeEventListener(event, handler);
      });
    });
    this.eventListeners = {};
  };

  updateStateFromLoadedItems = () => {
    const loadedItems = this.badgeContainer.querySelectorAll(".post-tag__edit");

    loadedItems.forEach((badge) => {
      const checkboxId = badge.id.replace("post-tag-badge-", "");
      const checkbox = document.getElementById(checkboxId);

      // update the selected items order array
      if (checkbox) {
        checkbox.checked = true;
        this.selectedItemsOrder.push(checkbox.id);
        checkbox.closest("li").classList.add("selected");
      }

      // add the click event listener to the badge
      badge.addEventListener("click", () => {
        checkbox.checked = false;
        this.removeBadge(checkboxId);
        console.log(checkbox.closest("li"));
        checkbox.closest("li").classList.remove("selected");
      });

      // Update the visibility of the toggle button
      this.updateToggleButtonVisibility();
    });
  };

  filterItems = (event) => {
    const filter = event.target.value.toUpperCase();
    const dropdownItems = this.dropdownList.querySelectorAll("li");

    dropdownItems.forEach((item) => {
      const label = item.querySelector("label").innerText;
      item.style.display =
        label.toUpperCase().indexOf(filter) > -1 ? "" : "none";
    });
  };

  toggleDropdown = (event) => {
    event.stopPropagation();

    this.isDropdownOpen = !this.isDropdownOpen;

    this.toggleWindowScroll();

    if (!this.isDropdownOpen) {
      this.updateBadges();
    }

    document
      .querySelector("#dropdownOverlay")
      .classList.toggle("d-none", !this.isDropdownOpen);

    this.dropdownMenu.classList.toggle("show", this.isDropdownOpen);
  };

  closeDropdown = (event) => {
    if (
      this.isDropdownOpen &&
      !event.target.closest("#postTagBadgeContainer")
    ) {
      this.updateBadges();
    }
  };

  toggleItem = (event) => {
    event.stopPropagation();
    const checkbox = event.currentTarget.querySelector(
      'input[type="checkbox"]',
    );
    checkbox.checked = !checkbox.checked;

    if (checkbox.checked) {
      event.currentTarget.classList.add("selected");
      this.selectedItemsOrder.push(checkbox.id);
    } else {
      event.currentTarget.classList.remove("selected");
      this.selectedItemsOrder = this.selectedItemsOrder.filter(
        (id) => id !== checkbox.id,
      );
    }
  };

  updateBadges = () => {
    // clear existing badges
    this.badgeContainer
      .querySelectorAll(".post-tag__edit")
      .forEach((badge) => badge.remove());

    // get the checkbox in the order of user selection
    const selectedCheckboxes = this.selectedItemsOrder
      .map((id) => document.getElementById(id))
      .filter((checkbox) => checkbox.checked);

    // Add badges for selected items, up to 5
    selectedCheckboxes.slice(0, 5).forEach((checkbox) => {
      if (!document.getElementById(`post-tag-badge-${checkbox.id}`)) {
        this.addBadge(checkbox.value, checkbox.id, checkbox.dataset.color);
        checkbox.closest("li").classList.add("selected");
      }
    });

    // Deselect any remaining checkboxes beyond the first 5 selected
    selectedCheckboxes.slice(5).forEach((checkbox) => {
      checkbox.checked = false;
      checkbox.closest("li").classList.remove("selected");
      this.selectedItemsOrder = this.selectedItemsOrder.filter(
        (id) => id !== checkbox.id,
      );
    });

    // Clear the search field
    this.dropdownSearch.value = "";

    // Reset the filter to show all items
    this.filterItems({ target: { value: "" } });

    this.isDropdownOpen = false;
    this.dropdownMenu.classList.remove("show");
    document
      .querySelector("#dropdownOverlay")
      .classList.toggle("d-none", !this.isDropdownOpen);
    this.toggleWindowScroll();
  };

  addBadge = (value, id, tagColor) => {
    const tempDiv = document.createElement("div");

    const badgeHtml = `
      <div class="text-label-sm post-tag post-tag__edit" id="post-tag-badge-${id}"
      style="background-color: ${tagColor}"
      >
        ${value}
      </div>`;

    tempDiv.innerHTML = badgeHtml;

    // Use tempDiv.children[0] to get the first child element, ignoring text nodes
    const badge = tempDiv.children[0];

    // this.badgeContainer.appendChild(badge);
    this.dropdownButton.insertAdjacentElement("beforebegin", badge);

    badge.addEventListener("click", () => {
      const checkbox = document.getElementById(id);
      checkbox.checked = false;
      this.removeBadge(id);
      checkbox.closest("li").classList.remove("selected");
    });

    // Update the visibility of the toggle button
    this.updateToggleButtonVisibility();
  };

  removeBadge = (id) => {
    const badge = document.querySelector(`#post-tag-badge-${id}`);
    if (badge) {
      badge.remove();
    }

    this.selectedItemsOrder = this.selectedItemsOrder.filter(
      (selectedId) => selectedId !== id,
    );

    // Update the visibility of the toggle button
    this.updateToggleButtonVisibility();
  };

  updateToggleButtonVisibility = () => {
    const selectedItemsCount = this.getSelectedItems().length;

    this.dropdownButton.style.display =
      selectedItemsCount >= 5 ? "none" : "block";
  };

  toggleWindowScroll = () => {
    // get the width of the dropdown button to prevent the window slide to right when the overflow style is set to hidden

    if (this.isDropdownOpen) {
      const scrollbarWidth =
        window.innerWidth - document.documentElement.clientWidth;

      document.body.style.paddingRight = `${scrollbarWidth}px`;
      document.body.style.overflow = "hidden";

      document.querySelector(".navbar").style.paddingRight =
        `${scrollbarWidth}px`;
    } else {
      document.body.style.paddingRight = "0px";
      document.body.style.overflow = "";

      document.querySelector(".navbar").style.paddingRight = "0px";
    }
  };

  destroy = () => {
    this.removeEventListeners();
  };

  getSelectedItems = () => {
    const checkboxes = this.postTagContainer.querySelectorAll(
      '#postTagDropDownList input[type="checkbox"]',
    );

    const selectedItems = Array.from(checkboxes)
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value);

    return JSON.parse(JSON.stringify(selectedItems));
  };
}

class CreatePostFormHandler {
  constructor(postForm) {
    this.postForm = postForm;

    // Post title element
    this.postTitle = postForm.querySelector("#postTitle");

    // Post tag element
    this.postTags = new MultiSelectDropdownMenu(postForm);

    // Post content element
    this.postContent = postForm.querySelector("#postContent");

    // Image upload elements
    this.imageUpload = postForm.querySelector("#createPostUploadImageInput");
    this.imagePreviewContainer = postForm.querySelector(
      "#createPostPreviewImageContainer",
    );
    this.imagePreview = this.imagePreviewContainer.querySelector("img");
    this.removeImageButton = postForm.querySelector(
      "#createPostRemoveImageButton",
    );
    this.customUploadButton = postForm.querySelector(
      "#createPostUploadImageButton",
    );

    // Error message element
    this.errorMessage = postForm.querySelector("#createPostErrorMessage");

    // Submit button
    this.submitButton = postForm.querySelector("#createPostSubmitButton");

    // Cancel button
    this.cancelButton = postForm.querySelector("#createPostCancelButton");

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.focusOnPostTitle = this.focusOnPostTitle.bind(this);
    this.onCreatePostSubmit = this.onCreatePostSubmit.bind(this);
    this.onCallCreatePostAPI = this.onCallCreatePostAPI.bind(this);
    this.handleImageUpload = this.handleImageUpload.bind(this);
    this.removeImage = this.removeImage.bind(this);
    this.triggerImageUpload = this.triggerImageUpload.bind(this);
    this.showErrorMessage = this.showErrorMessage.bind(this);
    this.clearErrorMessage = this.clearErrorMessage.bind(this);
    this.disableForm = this.disableForm.bind(this);
    this.enableForm = this.enableForm.bind(this);
    this.returnToPreviousPage = this.returnToPreviousPage.bind(this);
    this.destroy = this.destroy.bind(this);
  }

  init() {
    this.postForm.addEventListener("submit", this.onCreatePostSubmit);

    // image upload handlers
    this.imageUpload.addEventListener("change", this.handleImageUpload);
    this.removeImageButton.addEventListener("click", this.removeImage);
    this.customUploadButton.addEventListener("click", this.triggerImageUpload);
    this.cancelButton.addEventListener("click", this.returnToPreviousPage);

    this.focusOnPostTitle();

    autoResizeTextarea(this.postContent, 1000);
  }

  async onCallCreatePostAPI() {
    const postData = new FormData(this.postForm);
    this.disableForm();

    try {
      let tags = this.postTags.getSelectedItems();
      postData.append("tags", JSON.stringify(tags));

      // append image url for compatibility with the API
      postData.append("image_url", "");

      const {
        status,
        errors,
        post_id: postId,
      } = await fetchAPI("/api/posts", "POST", postData);

      if (status === 400 && errors) {
        this.showErrorMessage(errors[0]);
        return;
      }

      this.postForm.reset();

      return postId;
    } catch (error) {
      throw new Error("Error creating post handler", error);
    }
  }

  async onCreatePostSubmit(e) {
    e.preventDefault();
    this.clearErrorMessage();

    try {
      const postId = await this.onCallCreatePostAPI();

      if (!postId) {
        throw new Error("Post ID is missing");
      }

      sessionStorage.setItem("isLoadAllPostStatus", true);

      window.location.href = `/notifications?filter=post-status#${postId}`;
    } catch (error) {
      throw new Error("Error creating post", error);
    } finally {
      this.enableForm();
    }
  }

  focusOnPostTitle() {
    this.postTitle.focus();

    // Place the cursor at the end of the text
    const titleLength = this.postTitle.value.length;
    this.postTitle.setSelectionRange(titleLength, titleLength);
  }

  handleImageUpload(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview.src = e.target.result;
        this.imagePreview.classList.remove("d-none");
        this.removeImageButton.classList.remove("d-none");
      };
      reader.readAsDataURL(file);
      this.customUploadButton.parentNode.classList.add("d-none");
    }
  }

  removeImage() {
    this.imagePreview.src = "";
    this.imagePreview.classList.add("d-none");
    this.removeImageButton.classList.add("d-none");
    this.imageUpload.value = "";
    this.customUploadButton.parentNode.classList.remove("d-none");
  }

  triggerImageUpload() {
    this.imageUpload.click();
  }

  showErrorMessage(message) {
    this.errorMessage.textContent = message;
    this.errorMessage.classList.remove("d-none");
  }

  clearErrorMessage() {
    this.errorMessage.textContent = "";
    this.errorMessage.classList.add("d-none");
  }

  disableForm() {
    const allInteractiveElements = [];
    const targetElements = ["input", "textarea", "button"];

    targetElements.forEach((targetElement) => {
      allInteractiveElements.push(
        ...this.postForm.querySelectorAll(targetElement),
      );
    });

    allInteractiveElements.forEach((el) => {
      el.disabled = true;
    });
  }

  enableForm() {
    const allInteractiveElements = [];
    const targetElements = ["input", "textarea", "button"];

    targetElements.forEach((targetElement) => {
      allInteractiveElements.push(
        ...this.postForm.querySelectorAll(targetElement),
      );
    });

    allInteractiveElements.forEach((el) => {
      el.disabled = false;
    });
  }

  returnToPreviousPage() {
    window.history.back();
  }

  destroy() {
    this.removeEventListeners();
    this.postTags.destroy();
  }
}

class EditPostFormHandler {
  constructor(postForm) {
    this.postForm = postForm;

    // Post title element
    this.postTitle = postForm.querySelector("#postTitle");

    // Post tag element
    this.postTags = new MultiSelectDropdownMenu(postForm);

    // Post content element
    this.postContent = postForm.querySelector("#postContent");

    // Image upload elements
    this.imageUpload = postForm.querySelector("#editPostUploadImageInput");
    this.imagePreviewContainer = postForm.querySelector(
      "#editPostPreviewImageContainer",
    );
    this.imagePreview = this.imagePreviewContainer.querySelector("img");
    this.removeImageButton = postForm.querySelector(
      "#editPostRemoveImageButton",
    );
    this.customUploadButton = postForm.querySelector(
      "#editPostUploadImageButton",
    );

    // Error message element
    this.errorMessage = postForm.querySelector("#editPostErrorMessage");

    // Submit button
    this.submitButton = postForm.querySelector("#editPostSubmitButton");

    // Cancel button
    this.cancelButton = postForm.querySelector("#editPostCancelButton");

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.disableSubmitButtonOnLoad = this.disableSubmitButtonOnLoad.bind(this);
    this.focusOnPostTitle = this.focusOnPostTitle.bind(this);
    this.onEditPostSubmit = this.onEditPostSubmit.bind(this);
    this.onCallCreatePostAPI = this.onCallCreatePostAPI.bind(this);
    this.onCallDeletePostAPI = this.onCallDeletePostAPI.bind(this);
    this.handleImageUpload = this.handleImageUpload.bind(this);
    this.removeImage = this.removeImage.bind(this);
    this.triggerImageUpload = this.triggerImageUpload.bind(this);
    this.showErrorMessage = this.showErrorMessage.bind(this);
    this.clearErrorMessage = this.clearErrorMessage.bind(this);
    this.disableForm = this.disableForm.bind(this);
    this.enableForm = this.enableForm.bind(this);
    this.returnToPreviousPage = this.returnToPreviousPage.bind(this);
    this.destroy = this.destroy.bind(this);
  }

  init() {
    this.postForm.addEventListener("submit", this.onEditPostSubmit);

    // image upload handlers
    this.imageUpload.addEventListener("change", this.handleImageUpload);
    this.removeImageButton.addEventListener("click", this.removeImage);
    this.customUploadButton.addEventListener("click", this.triggerImageUpload);
    this.cancelButton.addEventListener("click", this.returnToPreviousPage);

    this.disableSubmitButtonOnLoad();
    this.focusOnPostTitle();
    this.setPostContentLineBreaks();

    autoResizeTextarea(this.postContent, 1000);
  }

  async onCallCreatePostAPI() {
    const postData = new FormData(this.postForm);
    this.disableForm();

    try {
      let tags = this.postTags.getSelectedItems();
      postData.append("tags", JSON.stringify(tags));

      // append image url if the image is the previous image
      // also need to add the condition src not equal to window.location.href, because the imagePreview.src is set to window.location.href when the image is removed
      if (
        this.imagePreview.src &&
        this.imagePreview.src !== window.location.href &&
        !this.imageUpload.files.length
      ) {
        postData.append("image_url", this.imagePreview.src);
      } else {
        postData.append("image_url", "");
      }

      const {
        status,
        errors,
        post_id: postId,
      } = await fetchAPI(`/api/posts`, "POST", postData);

      if (status === 400 && errors) {
        this.showErrorMessage(errors[0]);
        return;
      }

      return postId;
    } catch (error) {
      throw new Error("Error editing post handler", error);
    }
  }

  async onCallDeletePostAPI() {
    try {
      // get the post id from the url
      const oldPostId = window.location.pathname.split("/").at(-2);

      const { status } = await fetchAPI(
        `/api/posts/${oldPostId}?isSoftDelete=true`,
        "DELETE",
        {
          isSoftDelete: true,
        },
      );

      return status === 200;
    } catch (error) {
      throw new Error("Error deleting post", error);
    }
  }

  async onEditPostSubmit(e) {
    e.preventDefault();
    this.clearErrorMessage();

    try {
      const postId = await this.onCallCreatePostAPI();

      if (!postId) {
        throw new Error("Post ID is missing");
      }
      const isOldPostSoftDeleted = await this.onCallDeletePostAPI();

      if (!isOldPostSoftDeleted) {
        throw new Error("Old post is not deleted");
      }

      sessionStorage.setItem("isLoadAllPostStatus", true);

      window.location.href = `/notifications?filter=post-status#${postId}`;
    } catch (error) {
      throw new Error("Error editing post", error);
    } finally {
      this.enableForm();
    }
  }

  disableSubmitButtonOnLoad() {
    this.submitButton.disabled = true;

    this.postForm.addEventListener("input", () => {
      this.submitButton.disabled = false;
    });
  }

  focusOnPostTitle() {
    this.postTitle.focus();

    // Place the cursor at the end of the text
    const titleLength = this.postTitle.value.length;
    this.postTitle.setSelectionRange(titleLength, titleLength);
  }

  setPostContentLineBreaks() {
    this.postContent.rows = this.postContent.value.split("\n").length;

    // once the post content is changed, set the row to 1
    this.postContent.addEventListener("input", () => {
      this.postContent.rows = 1;
    });
  }

  handleImageUpload(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview.src = e.target.result;
        this.imagePreview.classList.remove("d-none");
        this.removeImageButton.classList.remove("d-none");
      };

      // open and read the file, once the file is read, the onload event is triggered for further processing
      reader.readAsDataURL(file);
      this.customUploadButton.parentNode.classList.add("d-none");
    }
  }

  removeImage() {
    this.imagePreview.src = "";
    this.imagePreview.classList.add("d-none");
    this.removeImageButton.classList.add("d-none");
    this.imageUpload.value = "";
    this.customUploadButton.parentNode.classList.remove("d-none");
  }

  triggerImageUpload() {
    this.imageUpload.click();
  }

  showErrorMessage(message) {
    this.errorMessage.textContent = message;
    this.errorMessage.classList.remove("d-none");
  }

  clearErrorMessage() {
    this.errorMessage.textContent = "";
    this.errorMessage.classList.add("d-none");
  }

  disableForm() {
    const allInteractiveElements = [];
    const targetElements = ["input", "textarea", "button"];

    targetElements.forEach((targetElement) => {
      allInteractiveElements.push(
        ...this.postForm.querySelectorAll(targetElement),
      );
    });

    allInteractiveElements.forEach((el) => {
      el.disabled = true;
    });
  }

  enableForm() {
    const allInteractiveElements = [];
    const targetElements = ["input", "textarea", "button"];

    targetElements.forEach((targetElement) => {
      allInteractiveElements.push(
        ...this.postForm.querySelectorAll(targetElement),
      );
    });

    allInteractiveElements.forEach((el) => {
      el.disabled = false;
    });
  }

  returnToPreviousPage() {
    window.history.back();
  }

  destroy() {
    this.removeEventListeners();
    this.postTags.destroy();
  }
}

const onCreatePostPageButtonNavigate = () => {
  const createPostPageButton = document.querySelector("#createPostPageButton");

  createPostPageButton?.addEventListener("click", () => {
    window.location.href = "/posts/new-post";
  });
};

document.addEventListener("DOMContentLoaded", () => {
  onCreatePostPageButtonNavigate();

  const createPostForm = document.querySelector("#createPostForm");
  if (createPostForm) {
    new CreatePostFormHandler(createPostForm);
  }

  const editPostForm = document.querySelector("#editPostForm");

  if (editPostForm) {
    new EditPostFormHandler(editPostForm);
  }
});
