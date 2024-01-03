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
 * @description This function takes all `.player-flight-source` elements and makes
 * their card headers draggable by wrapping them with a tile containing the player
 * ID and name.
 *
 * @returns {  } The `setupPlayerDraggableOrigins` function returns nothing (i.e.,
 * it has no return statement) and instead modifies the HTML elements contained within
 * the `.player-flight-source` elements that are passed as arguments to the function.
 */
function setupPlayerDraggableOrigins() {
    let playerFlightSource = document.querySelectorAll(".player-flight-source");

    playerFlightSource.forEach(function (flight) {
        var headers = flight.querySelectorAll(".pool.draggable-source.draggable-target");
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
    radioInput.setAttribute("flight", flightID);
    radioInput.name = `flight-${flightID}-captain`;
    radioInput.id = `player-radio-${id}`;
    radioInput.style.display = "none";
    // radioInput.classList.add("captain-radio", "source-radio");
    radioInput.classList.add("captain-radio");
    let checkedImage = document.createElement("img");
    checkedImage.classList.add("checked-img");
    checkedImage.src = info.captainChecked.src; // Use the provided info
    checkedImage.alt = "Captain";
    let uncheckedImage = document.createElement("img");
    uncheckedImage.classList.add("unchecked-img");
    uncheckedImage.src = info.captainUnchecked.src; // Use the provided info
    uncheckedImage.alt = "Not Captain";
    let label = document.createElement("label");
    label.htmlFor = `player-radio-${id}`;
    label.style.cursor = "pointer";
    label.appendChild(checkedImage);
    label.appendChild(uncheckedImage);
    label.classList.add("captain-radio");
    // radioInput.addEventListener("click", captainRadioClickCallback);
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
* @description This function sets all the radio buttons with the same name as the
* target button to false and hides their checked images; it then sets the target
* button to true and shows its checked image.
* 
* @param { object } event - In the given function `captainRadioClickCallback`, the
* `event` input parameter is used to get the target radio input element that triggered
* the callback function.
* 
* @returns { any } This function takes an event object as a parameter and returns
* no output.
*/
function captainRadioClickCallback(event) {
    let radioInput = event.target;
    const parentNode = radioInput.parentNode.parentNode;
    parentNode.querySelectorAll(`input[name='${radioInput.name}']`).forEach((radio) => {
        radio.checked = false;
        radio.labels[0].querySelector(".checked-img").style.display = "none";
        radio.labels[0].querySelector(".unchecked-img").style.display = "inline";
    });
    radioInput.checked = true;
    radioInput.labels[0].querySelector(".checked-img").style.display = "inline";
    radioInput.labels[0].querySelector(".unchecked-img").style.display = "none";
    updatePlayerCards(parseInt(radioInput.getAttribute("flight")));
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
    draggable.classList.add("draggable-item", "d-flex", "justify-content-between");
    draggable.title = fullname;
    draggable.setAttribute("player-id", id);
    draggable.setAttribute("player-name", name);
    draggable.setAttribute("flight-id", flightID);

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

/**
 * @description This function adds images to table data using the `addImageToTd()`
 * function for each td element with specified class names. It loops through gameCountTds
 * and captanCountTds to add images from respective arrays.
 *
 * @returns { any } The output returned by the `addImagesToTableData` function is not
 * explicitly specified. However based on the code we can infer that:
 *
 * The function takes no input and has no return statement. Therefore it doesn't
 * return any output explicitly. Instead the function modifies the DOM elements within
 * the specified classes.
 */
function addImagesToTableData() {
    // Select all <td> elements with the specified class names
    const gameCountTds = document.querySelectorAll(".game-count-icon");
    const captainCountTds = document.querySelectorAll(".captain-count-icon");
    const lowPreferenceCountTds = document.querySelectorAll(".low-preference-count-icon");

    // Function to add an image to a <td> element
    /**
     * @description This function adds an <img> element to a td element using the imageSrc
     * parameter as the source of the image.
     *
     * @param {  } td - The `td` input parameter is a HTML table cell element that the
     * function appends the inserted image to.
     *
     * @param { string } imageSrc - The `imageSrc` input parameter is the source URL of
     * the image to be added to theTD element.
     *
     * @returns { any } The output returned by the function `addImageToTd` is an image
     * element that is appended as a child of the specified `td` element.
     */
    function addImageToTd(td, imageSrc) {
        const image = document.createElement("img");
        image.src = imageSrc;
        td.appendChild(image);
    }

    // Loop through and add images to the <td> elements
    gameCountTds.forEach((td) => {
        addImageToTd(td, info.tennisRacketWarning.src);
    });

    captainCountTds.forEach((td) => {
        addImageToTd(td, info.captainUnchecked.src);
    });

    lowPreferenceCountTds.forEach((td) => {
        addImageToTd(td, info.faceNeutral.src);
    });
}

/**
 * @description This function gets a table element from the HTML document based on
 * its `class` and `flight` attribute value matching the provided `id`.
 *
 * @param { string } id - The `id` input parameter passed to the function `getFlightTable`
 * specifies which table to look for and retrieve.
 *
 * @returns { object } The output returned by this function is a HTML table element
 * that matches the given `id` attribute value and has the class `schedule-table`.
 */
function getFlightTable(id) {
    // Use querySelector to find the table with class schedule-table and flight attribute
    const selector = `.schedule-table[flight="${id}"]`;
    return document.querySelector(selector);
}

/**
 * @description The given function `getAllFlightTables` returns a collection of all
 * elements on the page that have a class name of `"schedule-table"`.
 *
 * @returns {  } The function `getAllFlightTables()` returns a NodeList of all elements
 * on the page that have the class `schedule-table`. In other words，it retrieves all
 * the table elements with the specified class from the current document and returns
 * them as a list.
 */
function getAllFlightTables() {
    const selector = `.schedule-table`;
    return document.querySelectorAll(selector);
}

/**
 * @description This function retrieves the header cell for a given cell by fetching
 * the table of flights and returning the nth child <th> element within the first row
 * of the table.
 *
 * @param {  } cell - The `cell` input parameter is used to retrieve the header cell
 * corresponding to a specific data cell within a table.
 *
 * @returns {  } The function takes a `cell` element as an input and returns the
 * corresponding header cell for that cell. If the `flight` attribute of the given
 * cell is a valid flight number (an integer), the function searches for the table
 * with that flight number using `getFlightTable()`.
 */
function getHeaderCellForCell(cell) {
    let table = getFlightTable(parseInt(cell.getAttribute("flight")));
    if (table) {
        let cellIndex = cell.cellIndex;
        let headerCell = table.querySelector("tr:first-child th:nth-child(" + (cellIndex + 1) + ")");

        return headerCell;
    }
    return null;
}

/**
 * @description This function returns the availability of a player for a given cell
 * based on the value of an attribute with the player's name as a prefix.
 *
 * @param { string } p - The `p` input parameter is a player index (a number from 0
 * to 3) that specifies which player's availability should be checked for the given
 * `cell`.
 *
 * @param {  } cell - The `cell` input parameter passes a single cell from the grid
 * as an argument to the function.
 *
 * @returns { integer } The output of the `getPlayerAvailabilityForCell` function is
 * `-1`.
 */
function getPlayerAvailabilityForCell(p, cell) {
    let playerAttributeTag = `player-${p}`;
    let headerCell = getHeaderCellForCell(cell);
    if (headerCell) {
        return parseInt(headerCell.getAttribute(playerAttributeTag));
    }
    return -1;
}

/**
 * @description This function retrieves the full column of cells at a specific column
 * index from a table.
 *
 * @param { object } cell - The `cell` input parameter is a reference to an HTML table
 * cell element.
 *
 * @returns { array } The `getFullColumn` function returns an array of cells from a
 * specific column of a table. It takes a cell as input and returns all the cells
 * that are located at the same column index as the input cell.
 */
function getFullColumn(cell) {
    let table = getFlightTable(parseInt(cell.getAttribute("flight")));
    if (table) {
        let columnIndex = cell.cellIndex;
        let columnCells = [];
        for (let row of table.rows) {
            let cell = row.cells[columnIndex];
            if (cell) {
                columnCells.push(cell);
            }
        }

        return columnCells;
    }
}
