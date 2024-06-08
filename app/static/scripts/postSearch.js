import { fetchAPI } from "./utils.js";

class postAdvancedSearchModal {
  constructor() {
    this.postAdvancedSearchModal = document.querySelector(
      "#postAdvancedSearchModal",
    );
    this.postAdvancedSearchForm = this.postAdvancedSearchModal.querySelector(
      "#postAdvancedSearchForm",
    );

    // footer buttons
    this.postAdvancedSearchResetFilterButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchReestFilterButton",
      );

    this.postAdvancedSearchCancelButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchModalCloseButton",
      );

    this.postAdvancedSearchSubmitButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchModalSubmitButton",
      );

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.onPostAdvancedSearchSubmit =
      this.onPostAdvancedSearchSubmit.bind(this);
    this.onClosePostAdvancedSearchModalClick =
      this.onClosePostAdvancedSearchModalClick.bind(this);
    this.enableForm = this.enableForm.bind(this);
    this.disableForm = this.enableForm.bind(this);
  }

  init() {
    this.postAdvancedSearchForm.addEventListener(
      "submit",
      this.onPostAdvancedSearchSubmit,
    );
    this.postAdvancedSearchCancelButton.addEventListener(
      "click",
      this.onClosePostAdvancedSearchModalClick,
    );

    // shortcut key to close the modal
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        this.onClosePostAdvancedSearchModalClick();
      }
    });

    // clear the form
    this.postAdvancedSearchForm.reset();
  }

  async onPostAdvancedSearchSubmit() {}

  onClosePostAdvancedSearchModalClick() {
    this.postAdvancedSearchModal.close();
  }

  enableForm() {
    this.postAdvancedSearchModal
      .querySelectorAll("input, button")
      .forEach((el) => (el.disabled = false));
  }

  disableForm() {
    this.postAdvancedSearchModal
      .querySelectorAll("input, button")
      .forEach((el) => (el.disabled = true));
  }
}

class PostSimpleSearchBar {
  constructor() {
    this.postSearchForm = document.querySelector("#postSearchForm");

    this.postSearchSubmitButton = this.postSearchForm.querySelector(
      "#postSearchSubmitButton",
    );

    this.postSearchInput =
      this.postSearchForm.querySelector("#postSearchInput");
    this.toggleAdvancedSearchButton = this.postSearchForm.querySelector(
      "#togglePostAdvancedSearchButton",
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
      if (e.ctrlKey && e.key === "k") {
        e.preventDefault();
        this.onToggleAdvancedSearchModal();
      }
    });

    // clear the form
    this.postSearchForm.reset();
  }

  onPostSimpleSearchSubmit(e) {
    e.preventDefault();
    const searchText = this.postSearchInput.value;
    this.disableForm();

    try {
      // construct the search query
      const queryParamObj = {
        search_text: searchText,
        type_filter: "all",
        sort_by: "relevance",
      };

      const queryParams = new URLSearchParams(queryParamObj).toString();

      window.location.href = `results?${queryParams}`;
    } catch (error) {
      console.error("Error from onPostSimpleSearchSubmit", error);
    }
  }

  onToggleAdvancedSearchModal() {
    const advancedSearchModal = document.querySelector(
      "#postAdvancedSearchModal",
    );

    if (!advancedSearchModal) return;

    new postAdvancedSearchModal();
    advancedSearchModal.showModal();
  }

  enableForm() {
    this.postSearchForm
      .querySelectorAll("input, button")
      .forEach((el) => (el.disabled = false));
  }

  disableForm() {
    this.postSearchForm
      .querySelectorAll("input, button")
      .forEach((el) => (el.disabled = true));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new PostSimpleSearchBar();
});
