/**
* @description This function selects a tab based on a flight ID and displays the
* associated content by removing the 'active' class from all tabs and adding it to
* the selected tab and setting the display property of the corresponding content
* section to 'block' or 'none'.
* 
* @param { string } flightId - The `flightId` input parameter is used to select the
* appropriate tab based on its value.
* 
* @returns { object } The output returned by this function is a toggle effect on all
* tabs with the class "flight-tab", where only the tab with the corresponding flightId
* has the "active" class added to it and the others have it removed.
*/
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

/**
* @description This function sets up the display of content tabs based on which tab
* is currently active.
* 
* @returns { any } The output returned by the given function `setupShowActiveFlight`
* is not specified directly. Instead it is inferred from the code that the function
* modifies the `display` CSS property of elements with a specific `flight-id` attribute
* to either "block" or "none".
* 
* More specifically:
* 
* 	- The function selects all elements with the class ".tab-content" and iterates
* over them using `.forEach()`.
* 	- For each element content(), it checks if the `flightId` attribute matches the
* current active flight by parsing the value of `getAttribute("flight-id")` to a
* number and comparing it to the `flightId`.
* 	- If the `content` element is active (i.e., its `flightId` matches the current
* active flight), the function sets its `display` property to "block".
*/
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

/**
* @description This function sets up draggable elements on a web page by giving them
* a random starting hue based on their position and a consistent hue step between
* each item.
* 
* @returns { any } This function takes a list of elements with class `.draggable-source
* .draggable-item` and sets their background color randomly using a hue range from
* startHue to hueStep times the index of the element.
* 
* Output: Randomly set background colors for each element within the class specification
* using hue ranges and random starting point.
*/
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

/**
* @description This function takes all `.player-flight-source` elements and makes
* their card headers draggable by wrapping them with a tile containing the player
* ID and name.
* 
* @returns {  } The `setupPlayerDraggableOrigins` function returns nothing (i.e.,
* it has no return statement) and instead modifies the HTML elements contained within
* the `.player-flight-source` elements that are passed as arguments to the function.
*/
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

/**
* @description This function creates a radio input field and two images (checked and
* unchecked) to represent the options "Captain" and "Not Captain".
* 
* @param { string } id - The `id` input parameter is used to generate a unique
* identifier for the radio input element and its associated label element. It is
* used to construct the `for` attribute of the label element and is also included
* as a part of the `id` attribute of the radio input element.
* 
* @param { string } flightID - The `flightID` input parameter is used to create a
* unique name for the radio input element.
* 
* @returns { array } The function `createCaptainRadioInput` returns an array containing
* two elements: a radio input element and a label element. The radio input element
* has a unique ID and is initially hidden. The label element contains two image
* elements representing "Captain" and "Not Captain", and is associated with the radio
* input element through the `for` attribute.
*/
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

/**
* @description This function creates a draggable div element representing a player
* tile with the given name and id.
* 
* @param { string } id - The `id` input parameter is used to set the `player-id`
* attribute of the created draggable div element.
* 
* @param { string } name - In the provided function `makeDraggablePlayerTile`, the
* `name` input parameter is used to set the text content of a `<div>` element that
* represents the player's name.
* 
* @param { string } fullname - The `fullname` input parameter is used to set the
* title of the div element created by the function.
* 
* @param { string } flightID - The `flightID` input parameter is used to set the
* value of the `player-id` attribute on the generated `<div>` element.
* 
* @returns {  } Based on the code provided: The `makeDraggablePlayerTile()` function
* creates a new `div` element with a class list that includes "draggable-item",
* "d-flex", "justify-content-between", and "align-items-center".
*/
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

/**
* @description The function `revealHidden()` selects all elements with the class
* `reveal-after` and sets their `display` style to `"block"`, revealing them on the
* page.
* 
* @returns { any } The function `revealHidden()` uses `document.querySelectorAll()`
* to select all elements with the class `"reveal-after"`, and then uses `forEach()`
* to set the `display` style of each selected element to `"block"`.
* 
* The output returned by this function is that all elements with the class
* `"reveal-after"` will have their display changed to `"block"`, revealing any hidden
* content within them.
*/
function revealHidden() {
    document.querySelectorAll(".reveal-after").forEach(function (item) {
        item.style.display = "block";
    });
}
