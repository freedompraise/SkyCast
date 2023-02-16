function toggleDarkMode() {
    var body = document.querySelector("body");
    var button = document.querySelector("#dark-mode-toggle");
    var icon = document.querySelector("#dark-mode-icon");
    var label = document.querySelector("#dark-mode-label");
    
    if (body.classList.contains("dark-mode")) {
      body.classList.remove("dark-mode");
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
      label.textContent = "Dark Mode";
    } else {
      body.classList.add("dark-mode");
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
      label.textContent = "Light Mode";
    }
  }