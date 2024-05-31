export const insertLineBreaks = (text) => {
  return text.replace(/\n/g, "<br>");
};

export const fetchAPI = async (url, methods, body = null) => {
  try {
    const response = await fetch(url, {
      method: methods,
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(body),
    });

    return await response.json();
  } catch (error) {
    console.error("Error from fetchAPI:", error);
  }
};

export const autoResizeTextarea = (textArea, maxHeight) => {
  textArea?.addEventListener("input", () => {
    textArea.style.height = "auto";
    textArea.style.maxHeight = `${maxHeight || 280}px`;
    textArea.style.height = `${textArea.scrollHeight}px`;
  });
};

export const scrollToTopElement = (element = window, offsetY = 0) => {
  const scrollToTopButton = document.querySelector("#scrollToTop");
  let fadeOutTimeout = null;
  let hideTimeout = null;

  const handleClick = () => {
    clearTimeout(fadeOutTimeout);
    clearTimeout(hideTimeout);

    window.scrollTo({
      top: element.offsetTop - offsetY,
      behavior: "smooth",
    });

    scrollToTopButton.classList.add("d-none");
  };

  scrollToTopButton.classList.remove("d-none", "fade-out");

  scrollToTopButton.removeEventListener("click", handleClick);

  scrollToTopButton.addEventListener("click", handleClick);

  clearTimeout(fadeOutTimeout);
  clearTimeout(hideTimeout);

  fadeOutTimeout = setTimeout(() => {
    scrollToTopButton.classList.add("fade-out");
  }, 3000);

  hideTimeout = setTimeout(() => {
    scrollToTopButton.classList.add("d-none");
  }, 3300); // 3000ms + 300ms (assume fade-out duration is 300ms)
};
