function fetchSuggestions(query) {
  const suggestionsBox = document.getElementById("suggestions-box");
  if (query.length < 2) {
    suggestionsBox.innerHTML = ""; // Clear suggestions if input is too short
    return;
  }

  fetch(`/fetch-city-suggestions/?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      suggestionsBox.innerHTML = "";
      if (data.suggestions && data.suggestions.length > 0) {
        data.suggestions.forEach((city) => {
          const div = document.createElement("div");
          div.classList.add("suggestion-item");
          div.textContent = `${city.name}, ${
            city.state ? city.state + ", " : ""
          }${city.country}`;
          div.onclick = () => {
            document.getElementById("search-input").value = city.name;
            suggestionsBox.innerHTML = ""; // Clear suggestions after selection
          };
          suggestionsBox.appendChild(div);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching city suggestions:", error);
    });
}
