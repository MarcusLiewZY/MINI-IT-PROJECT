const tagListContainer = document.querySelector(
  ".admin-section .tag-list-container",
);

const adminPageTagListToggleButton = tagListContainer?.querySelector(
  "#adminPageTagListToggleButton",
);

const adminPageTagToggleList = tagListContainer?.querySelector(
  "#adminPageTagToggleList",
);

const tagListContentContainer =
  adminPageTagToggleList?.querySelector(".tag-list-content");

const adminPageCreateTagModalButton = tagListContainer?.querySelector(
  "#adminPageCreateTagModalButton",
);

const flashMessageContainer = document.querySelector("#flashMessage");

const onToggleTagList = () => {
  adminPageTagToggleList.classList.toggle("show");

  const tagListToggleButtonImg =
    adminPageTagListToggleButton.querySelector("img");

  if (adminPageTagToggleList.classList.contains("show")) {
    tagListToggleButtonImg.classList.add("rotate-down-90");
  } else {
    tagListToggleButtonImg.classList.remove("rotate-down-90");
  }
};

class CreateTagModalHandler {
  constructor() {
    this.createTagModal = document.querySelector("#createTagModal");
    this.openCreateTagModalButton = document.querySelector(
      ".admin-section #adminPageCreateTagModalButton",
    );
    this.closeCreateTagModalButton = this.createTagModal?.querySelector(
      "#createTagModalCloseButton",
    );
    this.errorMessage = this.createTagModal?.querySelector(
      "#createTagModalErrorMessage",
    );

    // form
    this.createTagForm = this.createTagModal?.querySelector("#createTagForm");

    // form inputs
    this.tagNameInput = this.createTagModal?.querySelector("#tagName");
    this.tagColorInput = this.createTagModal?.querySelector("#tagColor");
    this.tagDescriptionInput =
      this.createTagModal?.querySelector("#tagDescription");

    // bind the context of the class methods
    this.onColorPickerChange = this.onColorPickerChange.bind(this);
    this.onOpenCreateTagModalClick = this.onOpenCreateTagModalClick.bind(this);
    this.onCloseCreateTagModalClick =
      this.onCloseCreateTagModalClick.bind(this);
    this.autoResizeTextarea = this.autoResizeTextarea.bind(this);
    this.validateForm = this.validateForm.bind(this);
    this.onCreateTagClick = this.onCreateTagClick.bind(this);

    // utility methods
    this.fetchAPI = this.fetchAPI.bind(this);
    this.flashMessage = this.flashMessage.bind(this);
    this.showErrorMessage = this.showErrorMessage.bind(this);
    this.clearErrorMessage = this.clearErrorMessage.bind(this);
  }

  attachEventListeners() {
    this.onOpenCreateTagModalClick();
    this.onCloseCreateTagModalClick();
    this.onColorPickerChange();
    this.autoResizeTextarea();
    this.onCreateTagClick();
  }

  onOpenCreateTagModalClick() {
    this.openCreateTagModalButton.addEventListener("click", () => {
      this.createTagModal.showModal();
    });
  }

  onCloseCreateTagModalClick() {
    this.closeCreateTagModalButton.addEventListener("click", () => {
      this.createTagModal.close();
    });
  }

  onColorPickerChange() {
    const tagColorPreview =
      this.createTagModal?.querySelector("#tagColorPreview");

    tagColorPreview
      .closest(".color-swatch-container")
      .addEventListener("click", () => {
        this.tagColorInput.click();
      });

    this.tagColorInput.addEventListener("change", () => {
      tagColorPreview.style.backgroundColor = this.tagColorInput.value;

      if (this.tagColorInput.value === "#ffffff") {
        tagColorPreview.style.border = "1px solid #000000";
      } else {
        tagColorPreview.style.border = "none";
      }
    });
  }

  autoResizeTextarea() {
    this.tagDescriptionInput?.addEventListener("input", () => {
      this.tagDescriptionInput.style.height = "auto";

      this.tagDescriptionInput.style.maxHeight = "280px";
      this.tagDescriptionInput.style.height = `${this.tagDescriptionInput.scrollHeight}px`;
    });
  }

  validateForm() {
    if (
      !this.tagNameInput.value ||
      !this.tagColorInput.value ||
      !this.tagDescriptionInput.value
    ) {
      this.errorMessage.textContent = "Please fill out all required fields.";
      this.errorMessage.classList.remove("d-none");
      return false;
    } else return true;
  }

  async fetchAPI(method, url, data = null) {
    try {
      const response = await fetch(url, {
        method,
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(data),
      });

      return await response.json();
    } catch (error) {
      console.error("Error from fetchAPI:", error);
    }
  }

  onCreateTagClick() {
    this.createTagForm.addEventListener("submit", async (e) => {
      try {
        e.preventDefault();

        if (!this.validateForm()) return;

        const tagData = new FormData(this.createTagForm);

        const tagDataObj = Object.fromEntries(tagData.entries());

        const { status, tag } = await this.fetchAPI(
          "POST",
          "/api/tags",
          tagDataObj,
        );

        if (status === 409) {
          this.showErrorMessage("Tag name already exists.");
          return;
        }

        if (status !== 201) throw new Error("Failed to create tag.");

        const { id, name, color } = tag;

        this.createTagModal.close();
        this.createTagForm.reset();

        // construct the tag node element
        const newTagString = `<li
          class="post-tag post-tag-lg"
          id="${id}"
          style="background-color: ${color};">
          ${name}
        </li>`;

        tagListContentContainer.insertAdjacentHTML("beforeend", newTagString);

        const newTag = document.querySelector(`.admin-section [id="${id}"]`);

        newTag.addEventListener("click", () => {
          editTagModalHandler.onOpenEditTagModalClick(id);
        });

        this.flashMessage("Tag created successfully.", "success", 3000);
        this.clearErrorMessage();
      } catch (error) {
        console.error("Error from onCreateTagClick:", error);
      }
    });
  }

  flashMessage(message, type, duration = 3000) {
    const flashMessage = `<span class="flash flash-${type}">${message}</span>`;

    flashMessageContainer.innerHTML = flashMessage;
    flashMessageContainer.classList.remove("d-none");

    setTimeout(() => {
      flashMessageContainer.innerHTML = "";
      flashMessageContainer.classList.add("d-none");
    }, duration);
  }

  showErrorMessage(message) {
    this.errorMessage.textContent = message;
    this.errorMessage.classList.remove("d-none");
  }

  clearErrorMessage() {
    this.errorMessage.textContent = "";
    this.errorMessage.classList.add("d-none");
  }
}
class EditTagModalHandler {
  constructor() {
    this.isEventListenersAttached = false;
    this.editTagModal = document.querySelector("#editTagModal");
    this.closeEditTagModalButton = this.editTagModal.querySelector(
      "#editTagModalCloseButton",
    );
    this.deleteTagButton = this.editTagModal.querySelector(
      "#editTagModalDeleteButton",
    );
    this.errorMessage = this.editTagModal.querySelector(
      "#editTagModalErrorMessage",
    );

    // form
    this.editTagForm = this.editTagModal?.querySelector("#editTagForm");

    // form inputs
    this.tagNameInput = this.editTagModal?.querySelector("#tagName");
    this.tagColorInput = this.editTagModal?.querySelector("#tagColor");
    this.tagDescriptionInput =
      this.editTagModal?.querySelector("#tagDescription");

    // bind the context of the class methods
    this.onColorPickerChange = this.onColorPickerChange.bind(this);
    this.onOpenEditTagModalClick = this.onOpenEditTagModalClick.bind(this);
    this.onCloseEditTagModalClick = this.onCloseEditTagModalClick.bind(this);
    this.autoResizeTextarea = this.autoResizeTextarea.bind(this);
    this.validateForm = this.validateForm.bind(this);
    this.getTag = this.getTag.bind(this);
    this.onEditTagFormSubmit = this.onEditTagFormSubmit.bind(this);
    this.onDeleteTagClick = this.onDeleteTagClick.bind(this);

    // utility
    this.fetchAPI = this.fetchAPI.bind(this);
    this.flashMessage = this.flashMessage.bind(this);
    this.clearErrorMessage = this.clearErrorMessage.bind(this);
    this.showErrorMessage = this.showErrorMessage.bind(this);

    // Attach initial event listeners
    this.attachEventListeners();
  }

  attachEventListeners() {
    // Check if event listeners have already been attached
    if (this.isEventListenersAttached) return;

    this.closeEditTagModalButton.addEventListener(
      "click",
      this.onCloseEditTagModalClick,
    );
    this.deleteTagButton.addEventListener("click", this.onDeleteTagClick);
    this.editTagForm?.addEventListener("submit", this.onEditTagFormSubmit);

    this.onColorPickerChange();
    this.autoResizeTextarea();

    // Update isEventListenersAttached
    this.isEventListenersAttached = true;
  }

  async onOpenEditTagModalClick(tagId) {
    this.tagId = tagId; // Update tagId when opening the modal
    await this.getTag();
    this.editTagModal.showModal();
  }

  onCloseEditTagModalClick() {
    this.editTagModal.close();
  }

  onColorPickerChange() {
    const tagColorPreview =
      this.editTagModal?.querySelector("#tagColorPreview");

    tagColorPreview
      ?.closest(".color-swatch-container")
      .addEventListener("click", () => {
        this.tagColorInput.click();
      });

    this.tagColorInput?.addEventListener("change", () => {
      tagColorPreview.style.backgroundColor = this.tagColorInput.value;

      if (this.tagColorInput.value === "#ffffff") {
        tagColorPreview.style.border = "1px solid #000000";
      } else {
        tagColorPreview.style.border = "none";
      }
    });
  }

  autoResizeTextarea() {
    this.tagDescriptionInput?.addEventListener("input", () => {
      this.tagDescriptionInput.style.height = "auto";
      this.tagDescriptionInput.style.maxHeight = "280px";
      this.tagDescriptionInput.style.height = `${this.tagDescriptionInput.scrollHeight}px`;
    });
  }

  flashMessage(message, type, duration = 3000) {
    const flashMessage = `<span class="flash flash-${type}">${message}</span>`;

    flashMessageContainer.innerHTML = flashMessage;
    flashMessageContainer.classList.remove("d-none");

    setTimeout(() => {
      flashMessageContainer.innerHTML = "";
      flashMessageContainer.classList.add("d-none");
    }, duration);
  }

  async fetchAPI(method, url, data = null) {
    try {
      const options = {
        method,
        headers: {
          "Content-type": "application/json",
        },
      };

      if (data !== null) options.body = JSON.stringify(data);

      const response = await fetch(url, options);
      return await response.json();
    } catch (error) {
      console.error("Error from fetchAPI:", error);
    }
  }

  async getTag() {
    try {
      const { status, tag } = await this.fetchAPI(
        "GET",
        `/api/tags/${this.tagId}`,
        null,
      );

      if (status !== 200) throw new Error("Failed to get tag.");

      const { name, color, description } = tag;

      this.tagNameInput.value = name;
      this.tagColorInput.value = color;
      this.tagDescriptionInput.value = description;

      const tagColorPreview =
        this.editTagModal?.querySelector("#tagColorPreview");
      tagColorPreview.style.backgroundColor = color;
    } catch (error) {
      console.error("Error from getTag:", error);
    }
  }

  validateForm() {
    if (
      !this.tagNameInput.value ||
      !this.tagColorInput.value ||
      !this.tagDescriptionInput.value
    ) {
      this.showErrorMessage("Please fill out all required fields.");
      return false;
    } else return true;
  }

  async onEditTagFormSubmit(e) {
    try {
      e.preventDefault();

      if (!this.validateForm()) return;

      const tagData = new FormData(this.editTagForm);
      const tagDataObj = Object.fromEntries(tagData.entries());

      const { status, tag } = await this.fetchAPI(
        "PUT",
        `/api/tags/${this.tagId}`,
        tagDataObj,
      );

      if (status === 409) {
        this.showErrorMessage("Tag name already exists.");
        return;
      }

      if (status !== 200) throw new Error("Failed to edit tag.");

      this.editTagModal.close();
      this.editTagForm.reset();

      // Update the tag in the tag list
      const { id, name, color } = tag;

      const updatedTag = document.querySelector(`.admin-section [id="${id}"]`);
      updatedTag.style.backgroundColor = color;
      updatedTag.textContent = name;

      // show flash message
      this.flashMessage("Tag updated successfully.", "success", 3000);
      this.clearErrorMessage();
    } catch (error) {
      console.error("Error from editTag:", error);
    }
  }

  async onDeleteTagClick() {
    try {
      const { status } = await this.fetchAPI(
        "DELETE",
        `/api/tags/${this.tagId}`,
        null,
      );

      if (status !== 200) throw new Error("Failed to delete tag.");

      this.editTagModal.close();
      this.editTagForm.reset();

      const tag = document.querySelector(`.admin-section [id="${this.tagId}"]`);
      tag.remove();

      this.flashMessage("Tag deleted successfully.", "success");
      this.clearErrorMessage();
    } catch (error) {
      console.error("Error from deleteTag: ", error);
    }
  }

  showErrorMessage(message) {
    this.errorMessage.textContent = message;
    this.errorMessage.classList.remove("d-none");
  }

  clearErrorMessage() {
    this.errorMessage.textContent = "";
    this.errorMessage.classList.add("d-none");
  }
}

// initialize the CreateTagModalHandler instance
const createTagModalHandler = new CreateTagModalHandler();

// Initialize the EditTagModalHandler instance
const editTagModalHandler = new EditTagModalHandler();

document.addEventListener("DOMContentLoaded", () => {
  // Toggle tag list
  adminPageTagListToggleButton.addEventListener("click", onToggleTagList);

  createTagModalHandler.attachEventListeners();

  // Attach click event listeners to each tag
  [...tagListContentContainer.children].forEach((tag) => {
    tag.addEventListener("click", () => {
      const tagId = tag.id;
      editTagModalHandler.onOpenEditTagModalClick(tagId);
    });
  });
});

onToggleTagList();
