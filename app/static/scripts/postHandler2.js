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
    if (!this.isDropdownOpen) {
      this.updateBadges(); // Call the function when closing the dropdown
    }

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
    } else {
      event.currentTarget.classList.remove("selected");
    }
  };

  updateBadges = () => {
    const checkboxes = this.postTagContainer.querySelectorAll(
      '#postTagDropDownList input[type="checkbox"]',
    );

    // get all selected items
    const selectedCheckboxes = Array.from(checkboxes).filter(
      (checkbox) => checkbox.checked,
    );

    // clear existing badges
    this.badgeContainer
      .querySelectorAll(".post-tag__edit")
      .forEach((badge) => badge.remove());

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
    });

    // Clear the search field
    this.dropdownSearch.value = "";

    // Reset the filter to show all items
    this.filterItems({ target: { value: "" } });

    this.dropdownMenu.classList.remove("show");
    this.isDropdownOpen = false;
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

    // Update the visibility of the toggle button
    this.updateToggleButtonVisibility();
  };

  updateToggleButtonVisibility = () => {
    const selectedItemsCount = this.getSelectedItems().length;

    this.dropdownButton.style.display =
      selectedItemsCount >= 5 ? "none" : "block";
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

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.onCreatePostSubmit = this.onCreatePostSubmit.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleImageUpload = this.handleImageUpload.bind(this);
    this.removeImage = this.removeImage.bind(this);
    this.triggerImageUpload = this.triggerImageUpload.bind(this);
    this.resetFileInput = this.resetFileInput.bind(this);
    this.showErrorMessage = this.showErrorMessage.bind(this);
    this.clearErrorMessage = this.clearErrorMessage.bind(this);
    this.disableForm = this.disableForm.bind(this);
    this.enableForm = this.enableForm.bind(this);
    this.destroy = this.destroy.bind(this);
  }

  init() {
    this.postForm.addEventListener("submit", this.onCreatePostSubmit);

    // image upload handlers
    this.imageUpload.addEventListener("change", this.handleImageUpload);
    this.removeImageButton.addEventListener("click", this.removeImage);
    this.customUploadButton.addEventListener("click", this.triggerImageUpload);

    autoResizeTextarea(this.postForm.querySelector("#postContent"), 1000);
  }

  async handleSubmit() {
    const postData = new FormData(this.postForm);
    this.disableForm();

    try {
      let tags = this.postTags.getSelectedItems();
      postData.append("tags", JSON.stringify(tags));

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
      const postId = await this.handleSubmit();

      if (!postId) {
        throw new Error("Post ID is missing");
      }

      // todo: create a new function to navigate to the notification page

      sessionStorage.setItem("newPostId", postId);

      window.location.href = `/notifications?filter=all`;
    } catch (error) {
      console.error("Error creating post", error);
    } finally {
      this.enableForm();
    }
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
    this.imageUpload.value = "";
    this.removeImageButton.classList.add("d-none");
    this.customUploadButton.parentNode.classList.remove("d-none");
  }

  triggerImageUpload() {
    this.imageUpload.click();
  }

  resetFileInput = (fileInput) => {
    const newInput = fileInput.cloneNode(true);
    fileInput.replaceWith(newInput);
    return newInput;
  };

  showErrorMessage(message) {
    this.errorMessage.textContent = message;
    this.errorMessage.classList.remove("d-none");
  }

  clearErrorMessage() {
    this.errorMessage.textContent = "";
    this.errorMessage.classList.add("d-none");
  }

  disableForm() {
    this.postForm
      .querySelectorAll("input", "textarea", "button")
      .forEach((el) => {
        el.disabled = true;
      });
  }

  enableForm() {
    this.postForm
      .querySelectorAll("input", "textarea", "button")
      .forEach((el) => {
        el.disabled = false;
      });
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

  const postForm = document.querySelector("#createPostForm");
  if (postForm) {
    new CreatePostFormHandler(postForm);
  }
});
