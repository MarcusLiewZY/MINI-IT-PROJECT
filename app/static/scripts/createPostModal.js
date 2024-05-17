// post modal

document.addEventListener("DOMContentLoaded", () => {
  console.log("createPostModal.js loaded");
  const createPostModal = document.querySelector("#createPostModal");
  const openModalButton = document.querySelector("#createPostModalOpenButton");

  console.log(openModalButton);
  const closeModalButton = createPostModal?.querySelector(
    "#createPostModalCloseButton",
  );
  const createPostModalErrorMessage = createPostModal?.querySelector(
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

      createPostModal?.showModal();
    };
  }

  // content field auto resize
  const contentField = createPostModal?.querySelector("#contentField");

  contentField?.addEventListener("input", () => {
    contentField.style.height = "auto";

    contentField.style.maxHeight = "280px";
    contentField.style.height = `${contentField.scrollHeight}px`;
  });

  // upload image
  const uploadImageIcon = createPostModal?.querySelector("#uploadImageIcon");
  const imageInput = createPostModal?.querySelector("#image");
  const showImageLinkButton = createPostModal?.querySelector(".show-image-url");
  const showImageLink = createPostModal?.querySelector(
    "#createPostModalShowImageLink",
  );
  const removeImageButton = createPostModal?.querySelector(".remove-image");

  uploadImageIcon?.addEventListener("click", () => {
    imageInput.click();
  });

  removeImageButton?.addEventListener("click", () => {
    imageInput.value = "";
    // selectImageMessage.textContent = "";
    showImageLink.href = "";
    showImageLinkButton.classList.add("d-none");
    removeImageButton.classList.add("d-none");
  });

  imageInput?.addEventListener("change", () => {
    if (imageInput.files.length > 0) {
      // const filename = imageInput.files[0].name;
      // const truncatedFilename =
      // filename.length > 25 ? filename.slice(0, 25) + "..." : filename;
      // selectImageMessage.textContent = `${truncatedFilename} is selected`;

      showImageLink.href = URL.createObjectURL(imageInput.files[0]);
      showImageLinkButton.classList.remove("d-none");
      removeImageButton.classList.remove("d-none");
    }
  });
});
