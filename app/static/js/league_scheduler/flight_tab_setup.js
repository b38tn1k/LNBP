function selectTab(flightId) {
    // Remove the 'active' class from all tabs
    const tabs = document.querySelectorAll(".flight-tab");
    tabs.forEach((tab) => {
        tab.classList.remove("active");
    });

    // Add the 'active' class to the selected tab
    const selectedTab = document.getElementById(`flight-tab-${flightId}`);
    selectedTab.classList.add("active");

    const content = document.querySelectorAll(".tab-content");
    content.forEach((c) => {
        if (parseInt(c.getAttribute("flight-id")) == flightId) {
            c.style.display = "block";
        } else {
            c.style.display = "none";
        }
    });
}

function setupShowActiveFlight() {
    const tabs = document.querySelectorAll(".flight-tab");
    tabs.forEach((tab) => {
        if (tab.classList.contains("active")) {
            let flightId = parseInt(tab.getAttribute("flight-id"));
            const content = document.querySelectorAll(".tab-content");
            content.forEach((c) => {
                if (parseInt(c.getAttribute("flight-id")) == flightId) {
                    c.style.display = "block";
                } else {
                    c.style.display = "none";
                }
            });
        }
    });
}

function setupPlayerDraggableOriginsOld() {
    let flights = document.querySelectorAll(".player-flight-source");

    flights.forEach(function (flight) {
        var sources = flight.querySelectorAll(".draggable-source .draggable-item");
        var hueStep = 360 / sources.length;
        var startHue = Math.floor(Math.random() * 360); // Random starting point

        sources.forEach(function (item, index) {
            var hue = (startHue + hueStep * index) % 360;
            item.style.backgroundColor = `hsl(${hue}, 100%, 80%)`;
        });
    });
}

function setupPlayerDraggableOrigins() {
    let flights = document.querySelectorAll(".player-flight-source");

    flights.forEach(function (flight) {
        var headers = flight.querySelectorAll(".card-header.draggable-source.draggable-target");
        let flightID = flight.getAttribute("flight-id");
        headers.forEach(function (item, index) {
            let parent = item.closest(".player-card");
            let id = parseInt(parent.getAttribute("player-id"));
            let name = parent.getAttribute("player-name");
            let full_name = parent.getAttribute("player-full-name");
            let tile = makeDraggablePlayerTile(id, name, full_name, flightID);
            item.appendChild(tile);
        });

        var sources = flight.querySelectorAll(".draggable-source .draggable-item");
        var hueStep = 360 / sources.length;
        var startHue = Math.floor(Math.random() * 360); // Random starting point

        sources.forEach(function (item, index) {
            var hue = (startHue + hueStep * index) % 360;
            item.style.backgroundColor = `hsl(${hue}, 100%, 80%)`;
        });
    });
}

function createCaptainRadioInput(id, flightID) {

    // Create the radio input element
    let radioInput = document.createElement("input");
    radioInput.type = "radio";
    radioInput.name = `flight-${flightID}-captain`;
    radioInput.id = `player-radio-${id}`;
    radioInput.style.display = "none";

    // Create the checked and unchecked images
    let checkedImage = document.createElement("img");
    checkedImage.src = info.captainChecked; // Use the provided info
    checkedImage.alt = "Captain";

    let uncheckedImage = document.createElement("img");
    uncheckedImage.src = info.captainUnchecked; // Use the provided info
    uncheckedImage.alt = "Not Captain";

    // Create a label element to wrap the images and associate it with the radio input
    let label = document.createElement("label");
    label.htmlFor = `player-radio-${id}`;
    label.style.cursor = "pointer"; // Add pointer cursor for label

    // Append the images to the label
    label.appendChild(checkedImage);
    label.appendChild(uncheckedImage);

    // Add a change event listener to the radio input
    radioInput.addEventListener("change", function () {
        if (radioInput.checked) {
            // If the radio input is checked, show the checked image and hide the unchecked image
            checkedImage.style.display = "inline";
            uncheckedImage.style.display = "none";
        } else {
            // If the radio input is unchecked, show the unchecked image and hide the checked image
            checkedImage.style.display = "none";
            uncheckedImage.style.display = "inline";
        }
    });
    // Initially, set the visibility based on the initial state of the radio input
    if (radioInput.checked) {
        checkedImage.style.display = "inline";
        uncheckedImage.style.display = "none";
    } else {
        checkedImage.style.display = "none";
        uncheckedImage.style.display = "inline";
    }
    return [radioInput, label];
}

function makeDraggablePlayerTile(id, name, fullname, flightID) {
    let draggable = document.createElement("div");
    draggable.classList.add("draggable-item", "d-flex", "justify-content-between", "align-items-center");
    draggable.title = fullname;
    draggable.setAttribute("player-id", id);
    draggable.setAttribute("player-name", name);

    let [radioInput, label] = createCaptainRadioInput(id, flightID);
    let nameDiv = document.createElement("div");
    nameDiv.textContent = name;
    draggable.appendChild(label);
    draggable.appendChild(radioInput);
    draggable.appendChild(nameDiv);

    return draggable;
}

document.addEventListener("DOMContentLoaded", function () {
    setupPlayerDraggableOrigins();
    setupShowActiveFlight();
    document.querySelectorAll(".reveal-after").forEach(function (item) {
        item.style.display = "block";
    });
});
