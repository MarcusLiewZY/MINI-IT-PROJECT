// post modal
const createPostModal = document.querySelector("#createPostModal");
const openModalButton = document.querySelector("#openButton");
const closeModalButton = document.querySelector("#closeButton");

openModalButton.addEventListener("click", () => {
  createPostModal.showModal();
});

closeModalButton.addEventListener("click", () => {
  createPostModal.close();
});

// upload image
const uploadImageIcon = document.querySelector("#uploadImageIcon");
const imageInput = document.querySelector("#image");

uploadImageIcon.addEventListener("click", () => {
  imageInput.click();
});

// console.log the the target filename
// console.log the file url that will be submitted to the server
imageInput.addEventListener("change", () => {
  console.log(imageInput.files[0].name);
  console.log(URL.createObjectURL(imageInput.files[0]));
});

// todo: use this method to get the tag color
// const user_info = JSON.parse(
//   document.querySelector("#userInfo").dataset.userInfo,
// );

// for (const key in user_info) {
//   console.log(`${key}: ${user_info[key]}`);
// }
