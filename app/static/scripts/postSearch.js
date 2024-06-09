import { fetchAPI } from "./utils.js";

class PostAdvancedSearchModal {
  constructor() {
    this.postAdvancedSearchModal = document.querySelector(
      "#postAdvancedSearchModal",
    );
    this.postAdvancedSearchForm = this.postAdvancedSearchModal.querySelector(
      "#postAdvancedSearchForm",
    );

    // search input
    this.postAdvancedSearchInput = this.postAdvancedSearchModal.querySelector(
      "#postAdvancedSearchModalSearchField",
    );

    // upload date filter
    this.postUpdatedDateFilterContainer =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchUpdatedDate",
      );

    // post type filter
    this.postTypeFilterContainer = this.postAdvancedSearchModal.querySelector(
      "#postAdvancedSearchType",
    );

    // post tags
    this.postTagsSection =
      this.postAdvancedSearchModal.querySelector("#postTagsCol");
    this.postTagTitle = this.postTagsSection.querySelector("#postTagTitle");
    this.postTagsContainer = this.postTagsSection.querySelector(
      "#postAdvancedSearchTags",
    );
    this.postTagSearchInput = this.postTagsSection.querySelector(
      "#postTagSearchField",
    );
    this.postTagSearchButton = this.postTagsSection.querySelector(
      "#postTagSearchButton",
    );
    this.postTagCancelButton = this.postTagsSection.querySelector(
      "#postTagSearchCancelButton",
    );

    // sort by
    this.postSortbyContainer = this.postAdvancedSearchModal.querySelector(
      "#postAdvancedSearchSortBy",
    );

    // footer buttons
    this.postAdvancedSearchResetFilterButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchModalResetFilterButton",
      );

    this.postAdvancedSearchCancelButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchModalCloseButton",
      );

    this.postAdvancedSearchSubmitButton =
      this.postAdvancedSearchModal.querySelector(
        "#postAdvancedSearchModalSubmitButton",
      );

    this.defaultFilters = {};

    this.bindAll();
    this.init();
  }

  bindAll() {
    this.onPostAdvancedSearchSubmit =
      this.onPostAdvancedSearchSubmit.bind(this);
    this.onClosePostAdvancedSearchModalClick =
      this.onClosePostAdvancedSearchModalClick.bind(this);

    // setup methods
    this.getAllPostTags = this.getAllPostTags.bind(this);
    this.resetFilters = this.resetFilters.bind(this);
    this.setDefaultFilters = this.setDefaultFilters.bind(this);
    this.setupRadioButtonSelectItems =
      this.setupRadioButtonSelectItems.bind(this);
    this.setupCheckboxButtonSelectItems =
      this.setupCheckboxButtonSelectItems.bind(this);
    this.setInputAndFiltersOnUrl = this.setInputAndFiltersOnUrl.bind(this);

    // post tags methods
    this.onPostTagSearchButtonClick =
      this.onPostTagSearchButtonClick.bind(this);
    this.onPostTagFilterKeyUp = this.onPostTagFilterKeyUp.bind(this);
    this.onPostTagCancelClick = this.onPostTagCancelClick.bind(this);

    // utility methods
    this.enableForm = this.enableForm.bind(this);
    this.disableForm = this.enableForm.bind(this);
  }

  async init() {
    await this.getAllPostTags();
    this.setupRadioButtonSelectItems();

    // post tags
    this.postTagSearchButton.addEventListener(
      "click",
      this.onPostTagSearchButtonClick,
    );
    this.postTagSearchInput.addEventListener(
      "keyup",
      this.onPostTagFilterKeyUp,
    );
    this.postTagCancelButton.addEventListener(
      "click",
      this.onPostTagCancelClick,
    );

    // footer buttons
    this.postAdvancedSearchResetFilterButton.addEventListener("click", (e) => {
      e.preventDefault();
      this.resetFilters();
      this.postAdvancedSearchInput.focus();
    });
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
    this.setDefaultFilters();

    const searchParams = new URLSearchParams(window.location.search);

    if (searchParams && searchParams.has("search_text"))
      this.setInputAndFiltersOnUrl();
    else this.resetFilters();
  }

  onPostAdvancedSearchSubmit(e) {
    e.preventDefault();
    this.disableForm();

    try {
      const searchObj = {};

      const searchText = this.postAdvancedSearchInput.value;

      searchObj.search_text = searchText;

      const filters = [
        this.postUpdatedDateFilterContainer,
        this.postTypeFilterContainer,
        this.postSortbyContainer,
      ];

      filters.forEach((filter) => {
        const selectedFilter = [
          ...filter.querySelectorAll('input[type="radio"]'),
        ].filter((radio) => radio.checked)[0];

        if (!selectedFilter) return;

        searchObj[selectedFilter.name] = selectedFilter.value.toLowerCase();
      });

      const selectedTags = [
        ...this.postTagsContainer.querySelectorAll('input[type="checkbox"]'),
      ]
        .filter((checkbox) => checkbox.checked)
        .map((checkbox) => checkbox.value);

      if (selectedTags.length > 0) {
        const tagFilterName = this.postTagsContainer.querySelector(
          'input[type="checkbox"]',
        ).name;

        searchObj[tagFilterName] = selectedTags;
      }

      const queryParams = new URLSearchParams(searchObj).toString();

      this.enableForm();
      window.location.href = `/results?${queryParams}`;
    } catch (error) {
      console.error("Error from onPosAdvancedSearchSubmit", error);
    }
  }

  onClosePostAdvancedSearchModalClick() {
    this.postAdvancedSearchModal.close();

    postSimpleSearchBar.enableForm();
  }

  async getAllPostTags() {
    try {
      const { status, tags } = await fetchAPI("/api/tags", "GET", null);
      if (status !== 200) {
        throw new Error("Failed to fetch tags from the server");
      }

      // construct the tags element and append it to the postTagsContainer

      Object.keys(tags).forEach((tag) => {
        const tagElementText = `
        <li>
          <input type="checkbox" id="${tag}" name="tag_filter" value="${tag}" />
          <label for="${tag}" class="text-label-lg">${tag}</label>
        </li>
        `;

        const tagElement = document.createElement("div");
        tagElement.innerHTML = tagElementText;

        this.postTagsContainer.appendChild(tagElement.firstElementChild);
      });

      this.setupCheckboxButtonSelectItems();
    } catch (error) {
      console.error("Error from getAllPostTags", error);
    }
  }

  setupRadioButtonSelectItems() {
    const filterContainers = [
      this.postUpdatedDateFilterContainer,
      this.postTypeFilterContainer,
      this.postSortbyContainer,
    ];

    filterContainers.forEach((container) => {
      const radioButtons = container.querySelectorAll("input[type='radio']");

      radioButtons.forEach((radioButton) => {
        radioButton.addEventListener("change", () => {
          const label = radioButton.parentNode.querySelector("label");

          container.querySelectorAll("label").forEach((label) => {
            label.classList.remove("selected");
          });

          if (radioButton.checked) {
            label.classList.add("selected");
          }
        });
      });
    });
  }

  setupCheckboxButtonSelectItems() {
    const checkboxButtonsContainers =
      this.postTagsContainer.querySelectorAll("li");

    checkboxButtonsContainers.forEach((checkboxButtonContainer) => {
      checkboxButtonContainer.addEventListener("click", () => {
        const checkboxButton = checkboxButtonContainer.querySelector(
          'input[type="checkbox"]',
        );

        checkboxButton.checked = !checkboxButton.checked;

        if (checkboxButton.checked) {
          checkboxButtonContainer.classList.add("selected");
        } else {
          checkboxButtonContainer.classList.remove("selected");
        }

        this.postTagSearchInput.focus();
      });
    });
  }

  setDefaultFilters() {
    const defaultUpdatedTime =
      this.postUpdatedDateFilterContainer.querySelector("#allTime");
    const defaultPostType =
      this.postTypeFilterContainer.querySelector("#postTitle");
    const defaultSortBy = this.postSortbyContainer.querySelector("#relevance");

    const defaultFilters = [defaultUpdatedTime, defaultPostType, defaultSortBy];

    defaultFilters.forEach((filter) => {
      this.defaultFilters[filter.name] = filter.value;
    });

    this.defaultFilters.tag_filter = "None";
  }

  resetFilters() {
    const allRadioButtonFilters = this.postAdvancedSearchForm.querySelectorAll(
      'input[type="radio"]',
    );

    const allCheckboxFilters = this.postAdvancedSearchForm.querySelectorAll(
      'input[type="checkbox"]',
    );

    allRadioButtonFilters.forEach((filter) => {
      filter.checked = false;
      filter.parentNode.querySelector("label").classList.remove("selected");
    });

    allCheckboxFilters.forEach((filter) => {
      filter.checked = false;
      filter.parentNode.classList.remove("selected");
    });

    const defaultFilters = Object.entries(this.defaultFilters);

    defaultFilters.forEach(([filterName, filterValue]) => {
      const filterToCheck = this.postAdvancedSearchForm.querySelector(
        `input[type="radio"][name="${filterName}"][value="${filterValue}"]`,
      );

      if (filterToCheck) {
        filterToCheck.checked = true;
        filterToCheck.parentNode
          .querySelector("label")
          .classList.add("selected");
      }
    });

    // manually set the post tag default filter
    const defaultTagFilter = this.postTagsContainer.querySelector(
      `input[type='checkbox'][value=${this.defaultFilters.tag_filter}]`,
    );

    if (defaultTagFilter) {
      defaultTagFilter.checked = true;
      defaultTagFilter.parentNode.classList.add("selected");
    }
  }

  setInputAndFiltersOnUrl() {
    const searchParams = new URLSearchParams(window.location.search);

    // set the search text
    this.postAdvancedSearchInput.value = searchParams.get("search_text");
    this.postAdvancedSearchInput.focus();

    const allFilter = Object.fromEntries(searchParams.entries());

    const FilterContainers = [
      this.postUpdatedDateFilterContainer,
      this.postTypeFilterContainer,
      this.postSortbyContainer,
    ];

    for (const filterContainer of FilterContainers) {
      const radio = filterContainer.querySelector('input[type="radio"]');

      const filterName = radio.name;

      if (!filterName) continue;

      const filterValue = allFilter[filterName];

      if (!filterValue) continue;

      let radioToCheck = filterContainer.querySelector(
        `input[type="radio"][value="${filterValue}"]`,
      );

      if (!radioToCheck) {
        radioToCheck = filterContainer.querySelector(
          `input[type="radio"][name="${filterName}"][value="${this.defaultFilters[filterName]}"]`,
        );
      }

      radioToCheck.checked = true;
      radioToCheck.parentNode.querySelector("label").classList.add("selected");
    }

    // check the tags
    const tags = allFilter.tag_filter.split(",");

    tags.forEach((tag) => {
      const checkbox = this.postTagsContainer.querySelector(
        `input[type="checkbox"][value="${tag}"]`,
      );

      if (checkbox) {
        checkbox.checked = true;
        checkbox.parentNode.classList.add("selected");
      }
    });

    // if the tags are invalid, use the default tag
    const selectedTags = [
      ...this.postTagsContainer.querySelectorAll('input[type="checkbox"]'),
    ].filter((checkbox) => checkbox.value !== "None" && checkbox.checked);

    if (selectedTags.length < 1) {
      const defaultPostTag = this.postTagsContainer.querySelector(
        `input[type="checkbox"][value="${this.defaultFilters.tag_filter}"]`,
      );

      defaultPostTag.checked = true;
      defaultPostTag.parentNode.classList.add("selected");
    }
  }

  onPostTagSearchButtonClick() {
    this.postTagSearchInput.classList.remove("d-none");
    this.postTagSearchInput.focus();

    this.postTagTitle.classList.add("d-none");

    this.postTagCancelButton.classList.remove("d-none");

    this.postTagSearchButton.classList.add("d-none");
  }

  onPostTagCancelClick() {
    this.postTagSearchInput.value = "";
    this.postTagSearchInput.classList.add("d-none");

    this.postTagTitle.classList.remove("d-none");

    this.postTagSearchButton.classList.remove("d-none");
    this.postTagCancelButton.classList.add("d-none");

    // show all tags
    const tags = this.postTagsContainer.querySelectorAll("li");

    tags.forEach((tag) => {
      tag.classList.remove("d-none");
    });
  }

  onPostTagFilterKeyUp(e) {
    const searchText = e.target.value.toUpperCase();
    const tags = this.postTagsContainer.querySelectorAll("li");

    tags.forEach((tag) => {
      const label = tag.querySelector("label");
      const tagText = label.textContent.toUpperCase();

      if (tagText.includes(searchText)) {
        tag.classList.remove("d-none");
      } else {
        tag.classList.add("d-none");
      }
    });
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
        updated_time_filter: "all time",
        type_filter: "post title",
        tag_filter: "None",
        sort_by: "relevance",
      };

      const queryParams = new URLSearchParams(queryParamObj).toString();

      this.enableForm();
      window.location.href = `/results?${queryParams}`;
    } catch (error) {
      console.error("Error from onPostSimpleSearchSubmit", error);
    }
  }

  onToggleAdvancedSearchModal() {
    const advancedSearchModal = document.querySelector(
      "#postAdvancedSearchModal",
    );

    if (!advancedSearchModal) return;

    advancedSearchModal.showModal();

    // disable all the form elements
    this.disableForm();
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

const postSimpleSearchBar = new PostSimpleSearchBar();
const postAdvancedSearchModal = new PostAdvancedSearchModal();

// document.addEventListener("DOMContentLoaded", () => {});
