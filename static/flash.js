document.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((msg) => {
    setTimeout(() => {
      msg.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      msg.style.opacity = "0";
      msg.style.transform = "translateX(-20px)";
      setTimeout(() => msg.remove(), 600);
    }, 6000);
  });
});
