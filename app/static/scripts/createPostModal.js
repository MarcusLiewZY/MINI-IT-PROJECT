// post modal
const createPostModal = document.querySelector("#createPostModal");
const openModalButton = document.querySelector("#createPostModalOpenButton");
const closeModalButton = document.querySelector("#createPostModalCloseButton");
const createPostModalErrorMessage = document.querySelector(
  "#createPostModalErrorMessage",
);

openModalButton?.addEventListener("click", () => {
  createPostModal.showModal();
});

closeModalButton?.addEventListener("click", () => {
  createPostModal.close();
});

// keep modal open on error
if (createPostModalErrorMessage) {
  window.onload = () => {
    const createPostModal = document.getElementById("createPostModal");

    createPostModal.showModal();
  };
}

// content field auto resize
const contentField = document.querySelector("#contentField");

contentField?.addEventListener("input", () => {
  contentField.style.height = "auto";

  contentField.style.maxHeight = "280px";
  contentField.style.height = `${contentField.scrollHeight}px`;
});

// upload image
const uploadImageIcon = document.querySelector("#uploadImageIcon");
const imageInput = document.querySelector("#image");
const selectImageMessage = document.querySelector(".select-image-message");
const removeImageButton = document.querySelector(".remove-image");

uploadImageIcon?.addEventListener("click", () => {
  imageInput.click();
});

removeImageButton?.addEventListener("click", () => {
  imageInput.value = "";
  selectImageMessage.textContent = "";
  removeImageButton.classList.add("d-none");
});

imageInput?.addEventListener("change", () => {
  if (imageInput.files.length > 0) {
    const filename = imageInput.files[0].name;
    const truncatedFilename =
      filename.length > 25 ? filename.slice(0, 25) + "..." : filename;
    selectImageMessage.textContent = `${truncatedFilename} is selected`;

    removeImageButton.classList.remove("d-none");
  }
});
