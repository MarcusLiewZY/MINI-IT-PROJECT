const tagListContainer = document.querySelector(
  ".admin-section .tag-list-container",
);

const adminPageTagListToggleButton = tagListContainer.querySelector(
  "#adminPageTagListToggleButton",
);

const adminPageTagToggleList = tagListContainer.querySelector(
  "#adminPageTagToggleList",
);

const adminPageCreateTagModalButton = tagListContainer.querySelector(
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
    this.fetchAPI = this.fetchAPI.bind(this);
    this.createTag = this.createTag.bind(this);
  }

  attachEventListeners() {
    this.onOpenCreateTagModalClick();
    this.onCloseCreateTagModalClick();
    this.onColorPickerChange();
    this.autoResizeTextarea();
    this.createTag();
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

  async createTag() {
    this.createTagForm.addEventListener("submit", async (e) => {
      try {
        e.preventDefault();

        if (!this.validateForm()) return;

        const tagData = new FormData(this.createTagForm);

        const tagDataObj = Object.fromEntries(tagData.entries());

        const { status } = await this.fetchAPI("POST", "/api/tags", tagDataObj);

        if (status !== 201) throw new Error("Failed to create tag.");

        this.createTagModal.close();
        this.createTagForm.reset();
        window.location.reload();
      } catch (error) {
        console.error("Error from createTag:", error);
      }
    });
  }
}

class EditTagModalHandler {
  constructor(tagId) {
    this.tagId = tagId;
    this.editTagModal = document.querySelector("#editTagModal");
    this.openEditTagModalButton = document.querySelector(
      `.admin-section [id="${tagId}"]`,
    );
    this.closeEditTagModalButton = this.editTagModal?.querySelector(
      "#editTagModalCloseButton",
    );
    this.deleteTagButton = this.editTagModal?.querySelector(
      "#editTagModalDeleteButton",
    );
    this.errorMessage = this.editTagModal?.querySelector(
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
    this.fetchAPI = this.fetchAPI.bind(this);
    this.getTag = this.getTag.bind(this);
    this.editTag = this.editTag.bind(this);
    this.deleteTag = this.deleteTag.bind(this);
  }

  attachEventListeners() {
    this.onOpenEditTagModalClick();
    this.onCloseEditTagModalClick();
    this.onColorPickerChange();
    this.autoResizeTextarea();
    this.editTag();
    this.deleteTag();
  }

  async onOpenEditTagModalClick() {
    await this.getTag();
    this.editTagModal.showModal();
  }

  onCloseEditTagModalClick() {
    this.closeEditTagModalButton.addEventListener("click", () => {
      this.editTagModal.close();
    });
  }

  onColorPickerChange() {
    const tagColorPreview =
      this.editTagModal?.querySelector("#tagColorPreview");

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
      const {
        status,
        tag: { name, color, description },
      } = await this.fetchAPI("GET", `/api/tags/${this.tagId}`, null);

      if (status !== 200) throw new Error("Failed to get tag.");

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
      this.errorMessage.textContent = "Please fill out all required fields.";
      this.errorMessage.classList.remove("d-none");
      return false;
    } else return true;
  }

  async editTag() {
    this.editTagForm.addEventListener("submit", async (e) => {
      try {
        e.preventDefault();

        if (!this.validateForm()) return;

        const tagData = new FormData(this.editTagForm);

        const tagDataObj = Object.fromEntries(tagData.entries());

        const { status } = await this.fetchAPI(
          "PUT",
          `/api/tags/${this.tagId}`,
          tagDataObj,
        );

        if (status !== 200) throw new Error("Failed to edit tag.");

        this.editTagModal.close();
        this.editTagForm.reset();
        window.location.reload();
      } catch (error) {
        console.error("Error from editTag:", error);
      }
    });
  }

  async deleteTag() {
    this.deleteTagButton.addEventListener("click", async () => {
      try {
        const { status } = await this.fetchAPI(
          "DELETE",
          `/api/tags/${this.tagId}`,
          null,
        );

        if (status !== 200) throw new Error("Failed to delete tag.");

        this.editTagModal.close();
        this.editTagForm.reset();
        window.location.reload();
      } catch (error) {
        console.error("Error from deleteTag: ", error);
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // toggle tag list
  adminPageTagListToggleButton.addEventListener("click", onToggleTagList);

  // create tag handlers
  const createTagModalHandler = new CreateTagModalHandler();
  createTagModalHandler.attachEventListeners();

  const tagListContentContainer =
    adminPageTagToggleList?.querySelector(".tag-list-content");

  // edit tag handlers
  [...tagListContentContainer.children].forEach((tag) => {
    tag.addEventListener("click", () => {
      const tagId = tag.id;
      const editTagModalHandler = new EditTagModalHandler(tagId);
      editTagModalHandler?.attachEventListeners();
    });
  });
});

onToggleTagList();
