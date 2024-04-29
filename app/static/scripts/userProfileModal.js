const modal = document.querySelector("#userProfileModal");
const openButton = document.querySelector(".open-button");

openButton.addEventListener("click", () => {
  modal.showModal();
});

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.close();
  }
});
