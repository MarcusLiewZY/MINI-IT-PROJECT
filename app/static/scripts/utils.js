export const insertLineBreaks = (text) => {
  return text.replace(/\n/g, "<br>");
};

export const fetchAPI = async (url, method, body = null) => {
  try {
    const options = {
      method,
      headers: {
        Accept: "application/json",
      },
    };

    if (method !== "GET" && method !== "HEAD") {
      if (body instanceof FormData) {
        options.body = body;
      } else {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
      }
    }
    const response = await fetch(url, options);

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

export const scrollToTopElement = (
  element = window,
  offsetY = 0,
  animationTime = 3000,
) => {
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
  }, animationTime);

  hideTimeout = setTimeout(() => {
    scrollToTopButton.classList.add("d-none");
  }, animationTime); // 3000ms + 300ms (assume fade-out duration is 300ms)
};
