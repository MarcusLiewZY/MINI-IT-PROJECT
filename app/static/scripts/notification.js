// JavaScript
document.addEventListener("DOMContentLoaded", function () {
  const numSpanList = document.querySelectorAll(".filters1 li span");
  const filtersList = document.querySelectorAll(".filters1 li");

  // Function to update unread message count
  function updateUnreadCount() {
    const unReadMessagesCount = document.querySelectorAll(".unread1").length;
    numSpanList.forEach((span) => {
      span.innerText = unReadMessagesCount;
    });
  }

  // Function to mark a message as read
  function markAsRead(message) {
    message.classList.remove("unread1");
    updateUnreadCount();
  }

  // Function to mark all messages as read
  function markAllAsRead() {
    const unReadMessages = document.querySelectorAll(".unread1");
    unReadMessages.forEach((message) => markAsRead(message));
  }

  // Event listeners for each filter
  filtersList.forEach((filter) => {
    filter.addEventListener("click", function () {
      filtersList.forEach((f) => f.classList.remove("active1"));
      filter.classList.add("active1");
      // Reset the color of all filters to black
      filtersList.forEach((f) => (f.style.color = "black"));
      // Change color of the clicked filter to blue
      filter.style.color = "#0056b3";
      // Mark all messages as read when a filter is clicked
      const unReadMessages = document.querySelectorAll(".unread1");
      unReadMessages.forEach((message) => markAsRead(message));
    });
  });

  // Event listener for marking all as read
  const markAll = document.getElementById("mark-as-read");
  markAll.addEventListener("click", function () {
    markAllAsRead();
    markAll.classList.add("clicked"); // Add the clicked class
  });

  // Update initial count
  updateUnreadCount();
});
