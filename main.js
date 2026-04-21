(() => {
  function popupBuilder(burger) {
    const burgerName = document.createElement("h1");
    burgerName.classList.add("burger");
    burgerName.innerText = burger["burger"];

    const burgerPrice = document.createElement("div");
    burgerPrice.classList.add("price");
    burgerPrice.innerText = burger["price"];

    const restaurantName = document.createElement("div");
    restaurantName.classList.add("restaurant");
    restaurantName.innerText = burger["restaurant"];

    const address = document.createElement("address");
    address.innerHTML = burger["address"];

    const wrapper = document.createElement("div");
    wrapper.classList.add("burger-popup");
    wrapper.appendChild(burgerName);
    wrapper.appendChild(burgerPrice);
    wrapper.appendChild(restaurantName);
    wrapper.appendChild(address);

    return wrapper;
  }

  // Initialize map
  const map = L.map("map", {
    center: [44.6638, -63.5851],
    zoom: 10,
  });

  // Add base OSM tile layer
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Load the burger data
  fetch("../data/burger-bash-2026.json")
    .then((res) => res.json())
    .then((data) => {
      data.forEach((burger) => {
        // Add burger marker to the map
        let marker = L.marker([burger["latitude"], burger["longitude"]]).addTo(
          map,
        );
        // Bind popup message
        marker.bindPopup(popupBuilder(burger));
      });
    });
})();
