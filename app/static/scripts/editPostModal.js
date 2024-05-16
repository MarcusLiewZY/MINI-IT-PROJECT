document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const isEdit = urlParams.get("isEdit");

  if (isEdit === "true") {
    const editPostModal = document.querySelector("#editPostModal");
    if (editPostModal) {
      editPostModal.showModal();

      urlParams.delete("isEdit");
      history.replaceState({}, "", "?" + urlParams.toString());
    }
  }

  const closeButton = document.querySelector("#editPostModalCloseButton");
  const removeImageButton = document.querySelector(".remove-image");
  const imageInput = document.querySelector("#image");
  const showImageLinkButton = document.querySelector(".select-image-message");
  const showImageLink = document.querySelector("#showImageLink");

  // if (imageInput.value) {
  //   removeImageButton.classList.remove("d-none");
  //   showImageLink.href = URL.createObjectURL(imageInput.files[0]);
  //   showImageLink.classList.remove("d-none");
  // }

  removeImageButton?.addEventListener("click", () => {
    imageInput.value = "";
    removeImageButton.classList.add("d-none");
    showImageLink.href = "";
    showImageLink.classList.add("d-none");
  });

  closeButton?.addEventListener("click", () => {
    editPostModal.close();
  });

  imageInput?.addEventListener("change", () => {
    console.log(imageInput.files[0].name);
    if (imageInput.files.length > 0) {
      showImageLinkButton.classList.remove("d-none");
      removeImageButton.classList.remove("d-none");
      showImageLink.href = URL.createObjectURL(imageInput.files[0]);
    }
  });

  const editPostModalErrorMessage = document.querySelector(
    "#editPostModalErrorMessage",
  );

  if (editPostModalErrorMessage) {
    editPostModal.showModal();
  }
});
