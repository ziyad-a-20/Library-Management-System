function togglePassword() {
  const pwd = document.getElementById("password");
  const icon = document.querySelector(".toggle-password");
  const isHidden = pwd.type === "password";

  pwd.type = isHidden ? "text" : "password";
  icon.textContent = isHidden ? "visibility_off" : "visibility";
}
