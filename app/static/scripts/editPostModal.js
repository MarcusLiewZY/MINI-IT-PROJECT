// document.addEventListener("DOMContentLoaded", () => {
//   const urlParams = new URLSearchParams(window.location.search);
//   const isEdit = urlParams.get("isEdit");
//   const editPostModal = document.querySelector("#editPostModal");

//   if (isEdit === "true") {
//     if (editPostModal) {
//       editPostModal.showModal();

//       urlParams.delete("isEdit");
//       history.replaceState({}, "", "?" + urlParams.toString());
//     }
//   }

//   const uploadImageIcon = editPostModal?.querySelector("#uploadImageIcon");
//   const closeButton = editPostModal?.querySelector("#editPostModalCloseButton");
//   const removeImageButton = editPostModal?.querySelector(".remove-image");
//   const imageInput = editPostModal?.querySelector("#image");
//   const showImageLinkButton = editPostModal?.querySelector(".show-image-url");
//   const showImageLink = editPostModal?.querySelector("#showImageLink");

//   removeImageButton?.addEventListener("click", () => {
//     imageInput.value = "";
//     showImageLink.href = "";
//     showImageLinkButton.classList.add("d-none");
//     removeImageButton.classList.add("d-none");
//   });

//   uploadImageIcon?.addEventListener("click", () => {
//     imageInput.click();
//   });

//   closeButton?.addEventListener("click", () => {
//     editPostModal.close();
//   });

//   imageInput?.addEventListener("change", () => {
//     if (imageInput.files.length > 0) {
//       showImageLinkButton.classList.remove("d-none");
//       removeImageButton.classList.remove("d-none");
//       showImageLink.href = URL.createObjectURL(imageInput.files[0]);
//     }
//   });

//   const editPostModalErrorMessage = editPostModal?.querySelector(
//     "#editPostModalErrorMessage",
//   );

//   if (editPostModalErrorMessage) {
//     editPostModal.showModal();
//   }
// });
