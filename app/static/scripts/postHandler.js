import { autoResizeTextarea } from "./utils.js";

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
    document.querySelectorAll("#dropdownList li").forEach((li) => {
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
    const li = this.dropdownList.querySelectorAll("#dropdownList li");

    li.forEach((item) => {
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
    if (this.isDropdownOpen && !event.target.closest(".post-tag-dropdown")) {
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

    // Update badges for all selected/deselected items
    checkboxes.forEach((checkbox) => {
      if (
        checkbox.checked &&
        !this.postTagContainer.getElementById(checkbox.id)
      ) {
        console.log(checkbox.value, checkbox.id);
        this.addBadge(checkbox.value, checkbox.id, checkbox.dataset.color);
      } else if (
        !checkbox.checked &&
        this.postTagContainer.getElementById(checkbox.id)
      ) {
        this.removeBadge(checkbox.id);
      }
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
    <div class="text-label-sm post-tag" id="${id}"
    style="background-color: ${tagColor}"
    >
      ${value}
      <span class="remove-badge" data-id="${id}">&times;</span>
    </div>`;

    tempDiv.innerHTML = badgeHtml;

    // Use tempDiv.children[0] to get the first child element, ignoring text nodes
    const badge = tempDiv.children[0];

    console.log(tempDiv);
    console.log(badge);

    this.badgeContainer.insertAdjacentHTML("afterbegin", badge);

    badge.querySelector(".remove-badge").addEventListener("click", () => {
      console.log("remove badge clicked");
      console.log(id);
      const checkbox = document.getElementById(id);
      checkbox.checked = false;
      this.removeBadge(id);
      checkbox.closest("li").classList.remove("selected");
    });
  };

  removeBadge = (id) => {
    const badge = document.querySelector(`#post-tag-badge-${id}`);
    if (badge) {
      badge.remove();
    }
  };

  // this method is not used, it will pass the selected items to the formhandler class
  handleSubmit = (event) => {
    event.preventDefault();
    const checkboxes = document.querySelectorAll(
      '#dropdownList input[type="checkbox"]',
    );
    const selectedItems = Array.from(checkboxes)
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value);

    // const formData = new FormData(event.target);
    // formData.append("selectedItems", JSON.stringify(selectedItems));
    // const data = Object.fromEntries(formData.entries());
    // const parsedData = JSON.parse(data.selectedItems);
    // console.log(parsedData);
  };
}

class PostFormHandler {
  constructor(postForm) {
    this.postForm = postForm;
    this.imageUpload = document.getElementById("imageUpload");
    this.imagePreviewContainer = document.getElementById(
      "imagePreviewContainer",
    );
    this.imagePreview = document.getElementById("imagePreview");
    this.removeImageButton = document.getElementById("removeImageButton");
    this.customUploadButton = document.getElementById("customUploadButton");

    this.init();
  }

  init = () => {
    document
      .getElementById("dropdownForm")
      .addEventListener("submit", this.handleSubmit);
    this.imageUpload.addEventListener("change", this.handleImageUpload);
    this.removeImageButton.addEventListener("click", this.removeImage);
    this.customUploadButton.addEventListener("click", this.triggerImageUpload);

    // Add event listeners and store their references
    this.addEventListeners([
      {
        element: document.getElementById("dropdownForm"),
        event: "submit",
        handler: this.handleSubmit,
      },
      {
        element: this.imageUpload,
        event: "change",
        handler: this.handleImageUpload,
      },
      {
        element: this.removeImageButton,
        event: "click",
        handler: this.removeImage,
      },
      {
        element: this.customUploadButton,
        event: "click",
        handler: this.triggerImageUpload,
      },
    ]);
  };

  handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview.src = e.target.result;
        this.imagePreview.style.display = "block";
        this.removeImageButton.style.display = "block";
      };
      reader.readAsDataURL(file);
      this.customUploadButton.style.display = "none";
    }
  };

  removeImage = () => {
    this.imagePreview.src = "";
    this.imagePreview.style.display = "none";
    this.imageUpload.value = "";
    this.removeImageButton.style.display = "none";
    this.customUploadButton.style.display = "block";
  };

  triggerImageUpload = () => {
    this.imageUpload.click();
  };

  onSubmit = () => {};

  destroy = () => {
    // Cleanup logic
    this.removeEventListeners();
  };
}

class CreatePostFormHandler extends PostFormHandler {}

class EditPostFormHandler extends PostFormHandler {}

const onCreatePostPageButtonNavigate = () => {
  const createPostPageButton = document.querySelector("#createPostPageButton");

  createPostPageButton?.addEventListener("click", () => {
    window.location.href = "/posts/new-post";
  });
};

document.addEventListener("DOMContentLoaded", () => {
  onCreatePostPageButtonNavigate();

  const postContent = document.querySelector("#postContent");
  autoResizeTextarea(postContent, 1000);
  // todo: put into the form handler

  const postForm = document.querySelector("#createPostForm");
  const multiSelectDropdownMenu = new MultiSelectDropdownMenu(postForm);
});
