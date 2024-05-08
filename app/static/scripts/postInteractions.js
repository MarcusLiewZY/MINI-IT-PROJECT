// Get all post boxes
const postBoxes = document.querySelectorAll(".post-box");

// Iterate through each post box
postBoxes.forEach((postBox) => {
  // Like button within the post box
  const likeButton = postBox.querySelector('button[id^="post"]');
  // Span displaying the number of likes
  const likeCount = postBox.querySelector("span");
  // Event handler for clicking the like button
  likeButton.addEventListener("click", () => {
    // If the button hasn't been clicked before
    if (!likeButton.classList.contains("liked")) {
      // Update the like count and display it
      let currentLikes = parseInt(likeCount.textContent);
      currentLikes++;
      likeCount.textContent = currentLikes;
      // Add the 'liked' class to indicate that the button has been clicked
      likeButton.classList.add("liked");
      // Change the button color to red
      likeButton.style.color = "red";
      // Disable the button to prevent multiple clicks
      likeButton.disabled = true;
    }
  });
});

function toggleAnswer(element) {
  element.classList.toggle("active");
}
