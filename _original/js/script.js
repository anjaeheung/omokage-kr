const menuToggle = document.getElementById("menuToggle");
const globalNav = document.getElementById("globalNav");

menuToggle.addEventListener("click", () => {
  globalNav.classList.toggle("open");
});
