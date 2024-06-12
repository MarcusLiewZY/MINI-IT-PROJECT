document.addEventListener("DOMContentLoaded", () => {
  const userProfileModal = document.querySelector("#userProfileModal");
  const userProfileModalOpenButton = document.querySelector(".open-button");

  if (!userProfileModal || !userProfileModalOpenButton) return;

  userProfileModalOpenButton.addEventListener("click", () => {
    userProfileModal.showModal();
  });

  userProfileModal.addEventListener("click", (e) => {
    if (e.target === userProfileModal) {
      userProfileModal.close();
    }
  });
});
