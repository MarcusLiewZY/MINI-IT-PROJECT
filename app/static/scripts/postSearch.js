import { fetchAPI } from "./utils.js";

class postAdvancedSearchModal {
  constructor() {
    this.postAdvancedSearchModal = document.getElementById(
      "postAdvancedSearchModal",
    );
    this.postAdvancedSearchForm = this.postAdvancedSearchModal.getElementById(
      "postAdvancedSearchForm",
    );
  }
}

class PostSimpleSearchBar {
  constructor() {
    this.postSearchForm = document.getElementById("postSearchForm");
    this.postSearchSubmitButton = this.postSearchForm.getElementById(
      "postSearchSubmitButton",
    );
    this.postSearchInput =
      this.postSearchForm.getElementById("postSearchInput");
    this.toggleAdvancedSearchButton = this.postSearchForm.getElementById(
      "togglePostAdvancedSearchButton",
    );

    console.log(
      this.postSearchForm,
      this.postSearchSubmitButton,
      this.postSearchInput,
      this.toggleAdvancedSearchButton,
    );

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.onPostSimpleSearchSubmit = this.onPostSimpleSearchSubmit.bind(this);
    this.onToggleAdvancedSearchModal =
      this.onToggleAdvancedSearchModal.bind(this);
    this.enableForm = this.enableForm.bind(this);
    this.disableForm = this.disableForm.bind(this);
  }

  init() {
    this.postSearchForm.addEventListener(
      "submit",
      this.onPostSimpleSearchSubmit,
    );
    this.toggleAdvancedSearchButton.addEventListener(
      "click",
      this.onToggleAdvancedSearchModal,
    );

    // call the toggle advanced search modal when the user press ctrl + k
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.key === "k") this.onToggleAdvancedSearchModal;
    });
  }

  async onPostSimpleSearchSubmit() {}

  onToggleAdvancedSearchModal() {
    const advancedSearchModal = document.getElementById(
      "postAdvancedSearchModal",
    );

    if (!advancedSearchModal) return;

    advancedSearchModal.showModal();
  }

  enableForm() {}

  disableForm() {}
}

document.addEventListener("DOMContentLoaded", () => {
  new PostSimpleSearchBar();
});
