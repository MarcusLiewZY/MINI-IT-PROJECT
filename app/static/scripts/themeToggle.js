console.log("themeToggle.js loaded");

const themeStorageKey = "theme-preference";

const getColorPreference = () => {
  // check the local storage first, then the system preference
  if (localStorage.getItem(themeStorageKey)) {
    return localStorage.getItem(themeStorageKey);
  } else {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }
};

const theme = {
  value: getColorPreference(),
};

const reflectPreference = () => {
  document.firstElementChild.setAttribute("data-theme", theme.value);

  console.log(document.querySelector("#theme-toggle"));

  document
    .querySelector("#theme-toggle")
    ?.setAttribute("aria-label", theme.value);
};

const setThemePreference = () => {
  localStorage.setItem(themeStorageKey, theme.value);
  reflectPreference();
};

const onThemeToggleClick = () => {
  console.log("theme-toggle clicked");
  theme.value = theme.value === "light" ? "dark" : "light";

  setThemePreference();
};

// set the initial theme
reflectPreference();

window.onload = () => {
  // set on load so that the theme is set before the page is displayed
  reflectPreference();

  document
    .querySelector("#theme-toggle")
    .addEventListener("click", onThemeToggleClick);
};

// sync with system preference changes
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", ({ matches: isDark }) => {
    theme.value = isDark ? "dark" : "light";
    setThemePreference();
  });
