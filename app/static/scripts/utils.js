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

export const scrollToTopElement = (element = window, offsetY = 0) => {
  const scrollToTopButton = document.querySelector("#scrollToTop");

  scrollToTopButton.classList.remove("d-none");

  scrollToTopButton.addEventListener("click", () => {
    window.scrollTo({
      top: element.offsetTop - offsetY,
      behavior: "smooth",
    });

    scrollToTopButton.classList.add("d-none");
  });
};
