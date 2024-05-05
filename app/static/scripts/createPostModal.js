// post modal
const createPostModal = document.querySelector("#createPostModal");
const openModalButton = document.querySelector("#openButton");
const closeModalButton = document.querySelector("#closeButton");
const errorMessage = document.querySelector("#errorMessage");

openModalButton.addEventListener("click", () => {
  createPostModal.showModal();
});

closeModalButton.addEventListener("click", () => {
  createPostModal.close();
});

// keep modal open on error
if (errorMessage) {
  window.onload = () => {
    const createPostModal = document.getElementById("createPostModal");

    createPostModal.showModal();
  };
}

// content field auto resize
const contentField = document.querySelector("#contentField");

contentField.addEventListener("input", () => {
  contentField.style.height = "auto";

  contentField.style.maxHeight = "280px";
  contentField.style.height = `${contentField.scrollHeight}px`;
});

// upload image
const uploadImageIcon = document.querySelector("#uploadImageIcon");
const imageInput = document.querySelector("#image");
const selectImageMessage = document.querySelector(".select-image-message");

uploadImageIcon.addEventListener("click", () => {
  imageInput.click();
});

imageInput.addEventListener("change", () => {
  if (imageInput.files.length > 0) {
    selectImageMessage.textContent = `${imageInput.files[0].name} is selected`;
  }
});
