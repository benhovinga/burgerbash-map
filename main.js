(() => {
  function popupBuilder(burger) {
    const burgerName = document.createElement("div");
    burgerName.classList.add("burger");
    burgerName.innerText = burger["burger"];

    const burgerPrice = document.createElement("div");
    burgerPrice.classList.add("price");
    burgerPrice.innerText = burger["price"];

    const image = document.createElement("img");
    image.loading = "lazy";
    image.src = burger["image"];

    const moreInfo = document.createElement("div");
    moreInfo.classList.add("more-info");
    moreInfo.innerHTML = `<a target="_blank" href="${burger["href"]}">More information</a>`;

    const restaurantName = document.createElement("div");
    restaurantName.classList.add("restaurant");
    restaurantName.innerText = burger["restaurant"];

    const address = document.createElement("div");
    address.classList.add("address");
    address.innerText = burger["address"];

    const directions = document.createElement("div");
    directions.classList.add("directions");
    directions.innerHTML = `<a target="_blank" href="https://www.google.com/maps/dir/?api=1&destination=${burger["latitude"]},${burger["longitude"]}">Get Directions</a>`;

    const wrapper = document.createElement("div");
    wrapper.classList.add("burger-popup");
    wrapper.appendChild(burgerName);
    wrapper.appendChild(burgerPrice);
    wrapper.appendChild(image);
    wrapper.appendChild(moreInfo);
    wrapper.appendChild(restaurantName);
    wrapper.appendChild(address);
    wrapper.appendChild(directions);

    return wrapper;
  }

  const burgerIcon = L.icon({
    iconUrl: "img/burger-bash-icon.webp",
    iconSize: [32, 50],
  });

  // Initialize map
  const map = L.map("map", {
    center: [44.6638, -63.5851],
    zoom: 11,
  });

  // Add base OSM tile layer
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Load the burger data
  fetch("data/burger-bash-2026.json")
    .then((res) => res.json())
    .then((data) => {
      data.forEach((burger) => {
        // Add burger marker to the map
        let marker = L.marker([burger["latitude"], burger["longitude"]], {
          alt: burger["restaurant "],
          icon: burgerIcon,
        }).addTo(map);
        // Bind popup message
        marker.bindPopup(popupBuilder(burger));
      });
    });

  // Zoom to user location (requires location services)
  map.locate({ setView: true, maxZoom: 14 });
})();
