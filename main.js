const abc = document.querySelector("#createPostModal");
const openModal = document.querySelector(".buttonopen");
const closeModal = document.querySelector(".buttonclose");

openModal.addEventListener("click", () => {
  abc.showModal();
});

closeModal.addEventListener("click", () => {
  abc.close();
});
