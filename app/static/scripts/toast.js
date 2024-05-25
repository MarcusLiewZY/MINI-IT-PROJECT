document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".flash");

  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.classList.add("fade-out");
      setTimeout(() => {
        toast.remove();
      }, 1000);
    }, 3000);
  });
});
