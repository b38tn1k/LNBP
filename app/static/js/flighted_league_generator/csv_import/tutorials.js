// Function to check if cellGroups is empty and show a message if so
/**
 * @description The provided JavaScript function `checkCellGroups` checks the length
 * of an array called `cellGroups`, and displays an error message if the array is empty.
 *
 * @returns { boolean } The output returned by this function is "true".
 */
function checkCellGroups() {
    const tabContentDiv = document.querySelector(".data-label-tab-contents");
    if (cellGroups.length === 0) {
        tabContentDiv.innerHTML = "Please go back and select at least one flight";
        return false;
    } else {
        tabContentDiv.innerHTML = "";
    }
    return true;
}

// Function to generate an HTML table from a given cell group
/**
 * @description The given function takes a cell group and an ID as inputs and returns
 * a HTML table. It generates the table by parsing each cell's data attributes and
 * creating a row for each distinct row number.
 *
 * @param { object } cellGroup - The `cellGroup` parameter is an array of HTML TABLE
 * cells that the function takes as input.
 *
 * @param { string } id - The `id` input parameter sets the ID attribute of the
 * generated table element.
 *
 * @returns {  } Based on the provided function `generateTableFromCellGroup`, the
 * output returned by this function is a `HTMLTableElement` object.
 */
function generateTableFromCellGroup(cellGroup, id) {
    const table = document.createElement("table");
    const tbody = document.createElement("tbody");
    tbody.classList.add("w-100");

    table.classList.add(
        "csv-table",
        "flight-sub-table",
        "table",
        "table-light",
        "table-bordered",
        "table-hover",
        "table-sm"
    );
    table.id = id;

    let currentRow = -1;
    let tr;

    cellGroup.forEach((cell) => {
        const dataRow = parseInt(cell.getAttribute("data-row"));

        if (dataRow !== currentRow) {
            if (tr) {
                tbody.appendChild(tr);
            }

            tr = document.createElement("tr");
            currentRow = dataRow;
        }

        const td = document.createElement("td");
        td.innerHTML = cell.innerHTML;

        td.setAttribute("data-row", cell.getAttribute("data-row"));
        td.setAttribute("data-col", cell.getAttribute("data-col"));
        tr.appendChild(td);
    });

    if (tr) {
        tr.classList.add("w-100");
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    return table;
}

// Function to append generated table to the tab content div
/**
 * @description This function appends a table to the div with class ".data-label-tab-contents"
 * and sets the overflow property of that div to "auto".
 *
 * @param { object } table - The `table` input parameter takes a table element (<table>)
 * and appends it to the content div of a tab using the `appendChild()` method.
 *
 * @returns {  } The function does not return any value explicitly. It modifies the
 * DOM by appending a table to a specified div element.
 */
function appendTableToTabContent(table) {
    const tabContentDiv = document.querySelector(".data-label-tab-contents");
    tabContentDiv.style.overflow = "auto";
    tabContentDiv.appendChild(table);
}

/**
 * @description This function generates a list of tabs using Bootstrap classes and
 * adds an event listener to each tab to display the corresponding data when clicked.
 *
 * @returns { any } The output returned by this function is an HTML `<ul>` element
 * with the class "nav nav-tabs", containing several `<li>` elements with the class
 * "nav-item", each containing an `<a>` element with the class "nav-link" and a tab
 * title representing a flight number.
 */
function generateDataLabelTabs() {
    const tabContainer = document.querySelector(".data-label-tabs");
    tabContainer.innerHTML = ""; // Clear any existing tabs

    // Create the <ul> element with Bootstrap classes
    const ulElement = document.createElement("ul");
    ulElement.className = "nav nav-tabs";

    cellGroups.forEach((_, index) => {
        // Create the <li> element
        const liElement = document.createElement("li");
        liElement.className = "nav-item";

        // Create the <a> element
        const aElement = document.createElement("a");
        aElement.className = "nav-link";
        if (index == 0) {
            aElement.className = "nav-link active";
        }
        aElement.innerHTML = `Flight ${index + 1}`; // Setting the tab title
        aElement.setAttribute("data-group-index", index); // Storing the group index as a data attribute
        aElement.addEventListener("click", showFlightTab); // Attaching the click event listener

        // Append the <a> element to the <li> element
        liElement.appendChild(aElement);

        // Append the <li> element to the <ul> element
        ulElement.appendChild(liElement);
    });

    // Append the <ul> element to the tab container
    tabContainer.appendChild(ulElement);
}

// Function to handle tab click events
/**
 * @description This function prepares all the tabs for selection. It removes active
 * classes from all other tab links and adds an active class to the selected tab link.
 *
 * @param {  } event - In the function `showFlightTab(event)`, the `event` input
 * parameter is used to access the current click event that triggered the function call.
 *
 * @returns {  } Based on the code provided:
 *
 * The output returned by `showFlightTab` is undefined.
 */
function showFlightTab(event) {
    // Remove active class from all tabs
    const allTabs = document.querySelectorAll(".nav-link");
    allTabs.forEach((tab) => {
        tab.classList.remove("active");
    });

    // Add active class to the clicked tab
    event.target.classList.add("active");

    // Your existing logic
    const groupIndex = event.target.getAttribute("data-group-index");
    toggleFlightSubTableVisibility(groupIndex);
}

/**
 * @description This function toggleFlightSubTableVisibility() allows you to display
 * or hide certain tables on a web page based on an id value passed to the function.
 *
 * @param { string } targetId - The `targetId` input parameter is used to identify
 * which specific table should be made visible when the function is called.
 *
 * @returns {  } Based on the function's implementation and input `targetId`, the
 * output returned by `toggleFlightSubTableVisibility(targetId)` is:
 *
 * 	- All tables with class `'flight-sub-table'` are hidden except for the table with
 * `id` equal to `targetId`.
 */
function toggleFlightSubTableVisibility(targetId) {
    // Select all tables with the class 'flight-sub-table'
    const tables = document.querySelectorAll(".flight-sub-table");

    for (let id = 0; id < cellGroups.length; id++) {
        tearDownTableInteraction(String(id));
    }
    setUpTableInteraction(String(targetId));

    // Iterate over each table element
    tables.forEach((table) => {
        if (table.id === targetId) {
            // Make the table with the matching id visible
            table.style.display = "";
            setUpTableInteraction(table.id, table);
        } else {
            // Hide other tables
            tearDownTableInteraction(table.id, table);
            table.style.display = "none";
        }
    });
}

/**
 * @description This function extracts the contents of a CSV file embedded within an
 * HTML page and displays it as a table. It first retrieves the contents of the input
 * element with the ID "csv-input" and then prepares the content for display as a
 * table using the csvToTable() function.
 *
 * @returns { string } Based on the code provided:
 *
 * The output returned by the `stepIndex2Prep` function is `csvText`, which is the
 * value of the `csv-input` element's `value` attribute.
 */
function stepIndex2Prep() {
    const elem = document.getElementById("csv-input");
    let csvText = document.getElementById("csv-input").value;
    if (elem.hasAttribute("google-csv")) {
        res = elem.getAttribute("google-csv");
        if (res != "None") {
            csvText = res;
        }
    }
    csvToTable(csvText, "csv-table-start");
    setUpTableInteraction("csv-table-start");
}

/**
 * @description The function `removeDuplicates` takes an array of arrays (named
 * `cellGroups`) and returns a new array of distinct groups (groups are identified
 * by the string of their attribute values "data-row" and "data-col"). It does this
 * by creating a set to keep track of already seen group strings and iterating over
 * the input array of groups.
 *
 * @returns { array } The output returned by the function `removeDuplicates()` is an
 * array of unique group objects (`cellGroup` objects), where each object has been
 * seen only once and has its attribute values sorted and joined with a delimiter ("|").
 */
function removeDuplicates() {
    const uniqueGroups = [];
    const seen = new Set();

    for (const group of cellGroups) {
        const groupData = group[1]
            .map((cell) => cell.getAttribute("data-row") + "-" + cell.getAttribute("data-col"))
            .sort()
            .join("|");
        if (!seen.has(groupData)) {
            seen.add(groupData);
            uniqueGroups.push(group);
        }
    }
    return uniqueGroups;
}

/**
 * @description This function preprocesses a list of cell groups and generates HTML
 * tables from them for display on a web page.
 *
 * @returns { any } Based on the code provided:
 *
 * The output of the `stepIndex3Prep` function is `void`, as it does not return
 * anything explicitly. The function performs various operations on arrays and objects
 * but does not return any value explicitly.
 */
function stepIndex3Prep() {
    tearDownTableInteraction("csv-table-start");
    cellGroups = cellGroups.filter((group) => group[1].length !== 0 && group[0] == 2);
    // Step 2: Remove duplicate entries
    cellGroups = removeDuplicates();
    if (checkCellGroups()) {
        console.log("generating tabs");
        generateDataLabelTabs();
        for (let id = 0; id < cellGroups.length; id++) {
            const firstCellGroup = cellGroups[id][1];
            const table = generateTableFromCellGroup(firstCellGroup, id);
            appendTableToTabContent(table);
        }
        toggleFlightSubTableVisibility("0");
    } else {
        console.log("no cell groups!");
    }
}

/**
 * @description The `htmlTableToCsv` function converts HTML tables to a comma-separated
 * values (CSV) string.
 *
 * @param { string } html - The `html` input parameter is the HTML table content that
 * needs to be converted to a CSV string.
 *
 * @returns { string } The output returned by the function `htmlTableToCsv` is a
 * string representing the HTML table data converted to CSV (Comma Separated Values)
 * format.
 */
function htmlTableToCsv(html) {
    let csv = "";
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");
    const rows = doc.querySelectorAll("table tr");
    let maxCells = 0;
    for (const row of rows) {
        const cellCount = row.querySelectorAll("td, th").length;
        if (cellCount > maxCells) {
            maxCells = cellCount;
        }
    }
    for (const row of rows) {
        let rowData = [];
        const cells = row.querySelectorAll("td, th");

        for (const cell of cells) {
            rowData.push(cell.textContent.replace(/"/g, '""').replace(/,/g, ""));
        }
        while (rowData.length < maxCells) {
            rowData.push("");
        }

        csv += rowData.join(",") + "\n";
    }
    return csv;
}

/**
 * @description This function sets up event listeners for mouse down events on a table
 * with the id equal to the given parameter.
 *
 * @param { string } id - The `id` input parameter specifies the id of the table
 * element to which the event listener should be added.
 *
 * @param {  } table - The `table` input parameter is optional and if not provided
 * will be set to the `document.getElementById(id)` element.
 *
 * @returns {  } The output returned by this function is `null`.
 */
function setUpTableInteraction(id, table = null) {
    if (table === null) {
        table = document.getElementById(id);
    }
    table.addEventListener("mousedown", handleMouseDown);
}

/**
 * @description This function removes an event listener for "mousedown" events on a
 * table element with the specified ID.
 *
 * @param { string } id - The `id` input parameter specifies the ID of the table
 * element to be interacted with.
 *
 * @param { string } table - The `table` input parameter is optional and if not
 * provided will default to `document.getElementById(id)`.
 *
 * @returns { any } The function `tearDownTableInteraction` returns `void`, as it
 * does not return anything explicitly.
 */
function tearDownTableInteraction(id, table = null) {
    if (table === null) {
        table = document.getElementById(id);
    }
    table.removeEventListener("mousedown", handleMouseDown);
}

/**
 * @description This function removes the "table-primary" class from all cells currently
 * selected and clears the array of selected cells.
 *
 * @returns {  } The function `clearSelections` removes the `table-primary` class
 * from all cells contained within the `selectedCells` array and empties the array itself.
 */
function clearSelections() {
    selectedCells.forEach((cell) => cell.classList.remove("table-primary"));
    selectedCells = [];
}

/**
 * @description The function selects all table cells within a given top row and bottom
 * row and left column and right column using the CSS selectors `[data-row="${i}"][data-col="${j}"]`,
 * adds a class to them and pushes them to an array of selected cells.
 *
 * @param { number } topRow - The `topRow` input parameter specifies the topmost row
 * that should be selected.
 *
 * @param { number } bottomRow - The `bottomRow` input parameter specifies the end
 * index (inclusive) of the range of rows to select.
 *
 * @param { number } leftCol - The `leftCol` input parameter specifies the leftmost
 * cell to include when selecting a rectangle of cells.
 *
 * @param { number } rightCol - The `rightCol` input parameter specifies the ending
 * column number for the selection.
 *
 * @returns { any } The function selectRectangle logs the rectangular coordinates
 * (topRow%, bottomRow%, leftCol%, rightCol%) and selects all table cells within those
 * rectangular coordinates by adding a class "table-primary". It pushes each selected
 * cell to an array called 'selectedCells'.
 * The output returned by this function is not explicitly defined since it is logging
 * the select parameters.
 */
function selectRectangle(topRow, bottomRow, leftCol, rightCol) {
    console.log((topRow, bottomRow, leftCol, rightCol));
    for (let i = topRow; i <= bottomRow; i++) {
        for (let j = leftCol; j <= rightCol; j++) {
            const cells = document.querySelectorAll(`[data-row='${i}'][data-col='${j}']`);
            cells.forEach((cell) => {
                cell.classList.add("table-primary");
                selectedCells.push(cell);
            });
        }
    }
}

/**
 * @description This function highlights and selects cells based on a specified color
 * class and provides information.
 *
 * @param { string } colorClass - Based on the function code provided:
 *
 * The `colorClass` input parameter sets a CSS class that is added to each cell
 * selected by the function.
 *
 * @param { object } information - Based on the code provided:
 *
 * The `information` parameter is used to store additional data associated with the
 * selected cells and is stored within the `cellGroups` array along with the selected
 * cells and current step.
 *
 * @returns { array } Based on the code provided:
 *
 * The function `highlightAndSelectCells` returns `void` since it does not return
 * anything explicitly.
 */
function highlightAndSelectCells(colorClass, information) {
    for (let cell of selectedCells) {
        cell.classList.add(colorClass);
    }
    const newGroup = [];
    selectedCells.forEach((cell) => newGroup.push(cell));
    clearSelections();
    cellGroups.push([currentStep, newGroup, information]);
    console.log(cellGroups);
    startPoint = null;
}

/**
 * @description This function handles a mouse-down event on a grid of cells and selects
 * a rectangle of cells based on the event target and the previously selected cells.
 *
 * @param { object } event - The `event` input parameter is used to capture the mouse
 * event that triggered the function.
 *
 * @returns { any } The output returned by the `handleMouseDown` function is `undefined`.
 */
function handleMouseDown(event) {
    isMouseDown = true;
    const cell = event.target;
    selectedCells.push(cell);
    const row = parseInt(cell.getAttribute("data-row"), 10);
    const col = parseInt(cell.getAttribute("data-col"), 10);
    if (!startPoint) {
        startPoint = { row, col };
    } else {
        clearSelections();
        const topRow = Math.min(startPoint.row, row);
        const bottomRow = Math.max(startPoint.row, row);
        const leftCol = Math.min(startPoint.col, col);
        const rightCol = Math.max(startPoint.col, col);
        selectRectangle(topRow, bottomRow, leftCol, rightCol);
        startPoint = null;
    }
}

/**
 * @description This function takes a CSV string and an ID and converts it into an
 * HTML table.
 *
 * @param { string } csvText - The `csvText` input parameter is a string containing
 * the raw CSV data to be processed and displayed as a table.
 *
 * @param { string } id - The `id` input parameter is used to create a unique ID for
 * the table that will be generated.
 *
 * @returns { string } The output returned by the `csvToTable` function is a string
 * containing HTML markup for a table.
 */
function csvToTable(csvText, id) {
    const pipeCount = (csvText.match(/\|/g) || []).length;
    const commaCount = (csvText.match(/,/g) || []).length;
    const delimiter = pipeCount > commaCount ? "|" : ",";
    const rows = csvText.split("\n");
    let tableHTML = `<table id='${id}' class='csv-table table table-light table-bordered table-hover table-sm'>`;
    rows.forEach((row, rowIndex) => {
        tableHTML += "<tr>";
        const cells = row.split(delimiter);
        cells.forEach((cell, cellIndex) => {
            tableHTML += `<td data-row='${rowIndex}' data-col='${cellIndex}'>${cell.trim()}</td>`;
        });
        tableHTML += "</tr>";
    });
    tableHTML += "</table>";
    elem = getElemByStepClass(currentStep + 1, ".csv-table-container");
    elem.innerHTML = tableHTML;
}

/**
 * @description This function takes a current step value and a class name as inputs
 * and returns the HTML element with that class within the parent element with the
 * data-index matching the current step value.
 *
 * @param { string } currentStep - The `currentStep` input parameter specifies the
 * index of the current step (i.e., the step being processed) and is used to match
 * the parent element's data-index attribute to find the corresponding container element.
 *
 * @param { string } _class - The `_class` input parameter specifies the CSS class
 * to select elements with.
 *
 * @returns { object } Based on the code provided:
 *
 * The output returned by the function `getElemByStepClass` is `null`.
 */
function getElemByStepClass(currentStep, _class) {
    // Select all elements with the class 'csv-table-container'
    const containers = document.querySelectorAll(_class);
    // Find the correct container by matching the parent's data-index to currentStep
    for (let container of containers) {
        const parent = container.parentNode.parentNode.parentNode; // added cards
        if (parent.getAttribute("data-index") == String(currentStep)) {
            return container;
        }
    }

    // Return null if no matching container is found
    return null;
}

/**
 * @description This function takes an array of cell groups (i.e., rows) as input and
 * performs the following tasks:
 *
 * 1/ Removes duplicate cells from the input array.
 * 2/ Logs the unique cell groups to the console.
 * 3/ Creates a new array of result objects that contains the following properties:
 * 		- "type": The type of group (either "html" or "tableCSV").
 * 		- "data": The corresponding HTML or CSV data for the group.
 * 4/ Appends two additional result objects to the end of the result array:
 * 		- An object with a "type" property set to "tableHTML", containing the entire
 * HTML of the table.
 * 		- An object with a "type" property set to "tableCSV", containing the table data
 * exported as CSV.
 *
 * @returns { object } The output returned by the `parseCellGroups()` function is an
 * array of objects containing the following properties:
 *
 * 1/ `type`: Indicating the type of group (e.g., "tableHTML", "tableCSV")
 * 2/ `data`: Containing the data for that type of group (a string or an array of strings)
 */
function parseCellGroups() {
    cellGroups = removeDuplicates();
    const html = 1;
    const type = 2;
    result = [];
    for (let i = 0; i < cellGroups.length; i++) {
        const htmlStrings = cellGroups[i][html].map((element) => element.outerHTML);
        group = {
            type: cellGroups[i][type],
            data: htmlStrings.join(","),
        };
        result.push(group);
    }
    const tableElement = document.getElementById("csv-table-start");
    const tableHTML = tableElement ? tableElement.parentNode.innerHTML : "Table not found";
    // console.log(tableHTML);
    result.push({
        type: "tableHTML",
        data: tableHTML,
    });
    result.push({
        type: "tableCSV",
        data: htmlTableToCsv(tableHTML),
    });
    return result;
}

/**
* @description This function creates an HTML input field with a specific class and
* attribute and adds an event listener to it to log its current value upon pressing
* the Enter key.
* 
* @param { number } flightNumber - The `flightNumber` input parameter passes a dynamic
* value to the created input element's attribute "flight-number".
* 
* @returns { array } The function `createFlightHeader` takes a single argument
* `flightNumber` and returns an array with two elements:
* 
* 1/ The `flightNumber` parameter passed to the function.
* 2/ A created HTML input element with a value set to "Flight <flightNumber>".
* 
* The input element has three classes (`form-control`, `mb-3`, and `flight-title`)
* and an event listener that listens for the `'keypress'` event and logs the current
* value of the input element to the console when the Enter key is pressed.
*/
function createFlightHeader(flightNumber) {
    const flightInput = document.createElement("input");
    flightInput.setAttribute("type", "text");
    flightInput.classList.add("form-control", "mb-3", "flight-title");
    flightInput.setAttribute("placeholder", "Flight " + flightNumber);
    flightInput.setAttribute("flight-number", flightNumber);
    flightInput.value = "Flight " + flightNumber;

    // Add an event listener for the 'keypress' event
    flightInput.addEventListener("keypress", function (event) {
        // Check if the Enter key was pressed
        if (event.key === "Enter") {
            console.log(flightInput.value); // Log the current value of the input
        }
    });
    return [flightNumber, flightInput];
}

/**
* @description This function creates a new HTML table element with various styling
* classes and styles applied to it.
* 
* @returns { object } Based on the code provided:
* The function `createFlightTable()` returns a new `<table>` element with various
* CSS classes and styles applied to it.
*/
function createFlightTable() {
    const table = document.createElement("table");
    table.classList.add(
        "csv-table",
        "flight-sub-table",
        "table",
        "table-light",
        "table-bordered",
        "table-hover",
        "table-sm"
    );
    table.style.maxWidth = "100%";
    table.style.width = "auto";
    return table;
}

/**
* @description The provided JavaScript function `createFlightDateTimeRows` creates
* two rows of HTML table cells for displaying flight departure and arrival times for
* each player.
* 
* @param { object } league - The `league` input parameter is an array of objects
* containing timeslot information for each player.
* 
* @returns { array } The function `createFlightDateTimeRows` creates two tables rows:
* a `dateRow` and a `timeRow`. The `dateRow` contains one cell with a label for the
* player name that spans two columns and two rows. The `timeRow` contains two cells
* for the date and time input fields.
*/
function createFlightDateTimeRows(league) {
    const dateRow = document.createElement("tr");
    const timeRow = document.createElement("tr");
    const playerLabel = document.createElement("td");
    playerLabel.classList.add("bg-light", "fw-bold");
    playerLabel.setAttribute("rowspan", "2");
    playerLabel.setAttribute("colspan", "2");
    dateRow.appendChild(playerLabel);
    league.timeslots.forEach(function (ts) {
        const dateTime = new Date(ts);
        const dateValue = dateTime.toISOString().split("T")[0]; // YYYY-MM-DD format
        dateTime.setHours(dateTime.getHours() + 12);
        const timeValue = dateTime.toLocaleTimeString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
        const dateCell = document.createElement("td");
        dateCell.classList.add("bg-light", "fw-bold");
        // Create and set the date input
        const dateInput = document.createElement("input");
        dateInput.type = "date";
        dateInput.classList.add("form-control");
        dateInput.value = dateValue;
        dateCell.appendChild(dateInput);
        dateRow.appendChild(dateCell);
        const timeCell = document.createElement("td");
        timeCell.classList.add("bg-light", "fw-bold");
        // Create and set the time input
        const timeInput = document.createElement("input");
        timeInput.type = "time";
        timeInput.classList.add("form-control");
        timeInput.value = timeValue;
        timeCell.appendChild(timeInput);
        timeRow.appendChild(timeCell);
    });
    return [dateRow, timeRow];
}

/**
* @description This function adds a set of buttons to a table row representing a
* player's flights: "delete", "move up", and "move down".
* 
* @param {  } playerRow - The `playerRow` input parameter passed to the function is
* a HTML table row that contains the data for one player's flights.
* 
* @param { number } flightNumber - The `flightNumber` input parameter determines
* which button(s) to show and which to hide.
* 
* @param { number } maxFlightNumber - The `maxFlightNumber` input parameter specifies
* the maximum flight number that can be displayed for a given player row.
* 
* @param { object } p - The `p` input parameter passed to the `addPlayerMacros()`
* function is not used anywhere inside the function and hence can be safely ignored.
* 
* @returns {  } The output returned by this function is an HTML table row with three
* buttons: a delete button and two arrow buttons (up and down) that can be used to
* move the player's flight within the list.
*/
function addPlayerMacros(playerRow, flightNumber, maxFlightNumber, p) {
    // Create and append the delete button
    const deleteButton = document.createElement("button");
    let icon0 = document.createElement("i");
    icon0.classList.add('fe', 'fe-trash')
    deleteButton.appendChild(icon0);
    // deleteButton.innerHTML = "&times;";
    deleteButton.classList.add("btn", "btn-danger", "btn-sm");
    deleteButton.style.margin = "2px";

    deleteButton.addEventListener("click", function () {
        // Save the row data to the undo stack before deletion
        undoStack.push({ action: "deleted", data: p });

        // Remove the row from the table
        playerRow.remove();
    });

    const functionCell = document.createElement("td");

    const moveUpButton = document.createElement("button");
    let icon = document.createElement("i");
    icon.classList.add('fe', 'fe-arrow-up')
    moveUpButton.appendChild(icon);
    // moveUpButton.innerHTML = "&uarr;";
    moveUpButton.classList.add("btn", "btn-primary", "btn-sm", "move-up-button");
    moveUpButton.style.margin = "2px";
    moveUpButton.addEventListener("click", switchPlayerFlightUp);
    functionCell.appendChild(moveUpButton);

    const moveDownButton = document.createElement("button");
    let icon2 = document.createElement("i");
    icon2.classList.add('fe', 'fe-arrow-down')
    moveDownButton.appendChild(icon2);
    moveDownButton.classList.add("btn", "btn-primary", "btn-sm", "move-down-button");
    moveDownButton.style.margin = "2px";
    moveDownButton.addEventListener("click", switchPlayerFlightDown);
    functionCell.appendChild(moveDownButton);

    if (flightNumber == 1) {
        moveUpButton.hidden = true;
    }
    if (flightNumber == maxFlightNumber) {
        moveDownButton.hidden = true;
    }

    functionCell.appendChild(deleteButton);
    functionCell.style.width = "150px";
    functionCell.style.minWidth = "150px";
    functionCell.classList.add("player-macros");
    playerRow.appendChild(functionCell);
}

/**
* @description This function creates a table row for a flight player and adds macros
* for their availability.
* 
* @param { object } p - The `p` input parameter is the player object that contains
* information about a specific player.
* 
* @param { string } flightNumber - The `flightNumber` input parameter specifies the
* unique identifier for a flight that is being displayed.
* 
* @param { number } maxFlightNumber - The `maxFlightNumber` input parameter specifies
* the maximum flight number to be displayed on the player row.
* 
* @returns {  } Based on the code provided , the `createFlightPlayerRow` function
* creates a `tr` element representing a row for a flight and its players.
*/
function createFlightPlayerRow(p, flightNumber, maxFlightNumber) {
    const playerRow = document.createElement("tr");
    playerRow.classList.add("player-row");
    playerRow.setAttribute("flight-number", flightNumber);
    addPlayerMacros(playerRow, flightNumber, maxFlightNumber, p);
    const playerName = document.createElement("td");
    playerName.classList.add("bg-light", "fw-bold");
    playerName.innerHTML = p.names;
    playerName.style.width = "200px";
    playerName.style.minWidth = "200px";
    playerRow.append(playerName);
    p.availability.forEach(function (a) {
        const availability = document.createElement("td");
        availability.setAttribute("availability", a);
        availability.classList.add("availability");
        switch (a) {
            case 1:
                availability.classList.add("bg-free");
                break;
            case 2:
                availability.classList.add("bg-busy");
                break;
            case 3:
                availability.classList.add("bg-unavailable");
                break;
        }
        availability.title = p.names;
        playerRow.append(availability);
    });
    return playerRow;
}

/**
* @description This function creates an HTML table row with two cells: one for a "+"
* button to add a player and one for a text input to enter the player's name.
* 
* @param { string } flightNumber - The `flightNumber` input parameter sets the value
* of the `flight-number` attribute on the newly created `add-player-row` element.
* 
* @returns {  } The output returned by the `createAddPlayerRowFlight` function is a
* new `tr` element representing a row for adding a player to a flight. This row
* contains two cells: one for a "+" button to add a player and one for an input field
* to enter the player's name.
*/
function createAddPlayerRowFlight(flightNumber) {
    const addPlayerButton = document.createElement("button");
    let icon = document.createElement("i");
    icon.classList.add('fe', 'fe-user-plus')
    addPlayerButton.appendChild(icon);
    // addPlayerButton.innerHTML = '<i class="fe >';
    addPlayerButton.classList.add("btn", "btn-primary", "btn-sm");
    addPlayerButton.style.margin = "2px";
    addPlayerButton.addEventListener("click", addPlayerWithName);
    const addPlayerButtonCell = document.createElement("td");
    addPlayerButtonCell.appendChild(addPlayerButton);

    const addPlayerNameCell = document.createElement("td");
    const playerNameInput = document.createElement("input");
    playerNameInput.classList.add("form-control", "new-player-name");

    addPlayerNameCell.appendChild(playerNameInput);

    const addPlayerRow = document.createElement("tr");
    addPlayerRow.classList.add("add-player-row");
    addPlayerRow.appendChild(addPlayerButtonCell);
    addPlayerRow.appendChild(addPlayerNameCell);
    addPlayerRow.setAttribute("flight-number", flightNumber);

    return addPlayerRow;
}

/**
* @description This function counts the number of columns (td elements)in a table's
* tbody by first checking if the tbody has any rows and then counting the cells(td
* elements)in the first row.
* 
* @param {  } table - The `table` input parameter is the table element to be counted.
* 
* @returns { integer } The output of this function is the number of cells (td
* elements)in the first row of the tbody.
*/
function countColumns(table) {
    // Check if the tbody has any rows
    if (table.rows.length > 0) {
        // Count the number of cells (td elements) in the first row
        return table.rows[0].cells.length;
    } else {
        // Return 0 if there are no rows in the tbody
        return 0;
    }
}

/**
* @description This function gets a target table and its associated tbody element
* based on a given target flight. It first identifies the target table using an ID
* preceded by `flight-`, and then retrieves the tbody element within that table.
* 
* @param { string } targetFlight - The `targetFlight` input parameter specifies the
* identifier of the table to be searched for.
* 
* @returns { array } The function takes a `targetFlight` parameter and returns an
* array with two elements:
* 
* 1/ The `targetTable` element of the HTML document that has an id corresponding to
* the `targetFlight` parameter.
* 2/ The `tbody` element of the target table.
* 
* The output is an array with these two elements (the target table and the tbody element).
*/
function getTargetTableAndTbody(targetFlight) {
    console.log(targetFlight);
    const targetTable = document.getElementById(`flight-${targetFlight}`);
    if (!targetTable) {
        console.error(`Target table 'flight-${targetFlight}' not found`);
        return;
    }

    // Get the tbody element of the target table
    const targetTbody = targetTable.querySelector("tbody");
    if (!targetTbody) {
        console.error("No tbody found in the target table");
        return;
    }
    // console.log(targetFlight, targetTable, targetTbody)
    return [targetTable, targetTbody];
}

/**
* @description This function adds a new player to a flight schedule table. It gets
* the information from the form input field and creates a new row with the player
* name and availability status.
* 
* @param {  } event - The `event` input parameter is not used anywhere inside the
* function `addPlayerWithName()`.
* 
* @returns {  } Based on the provided code snippet:
* 
* The output returned by the `addPlayerWithName` function is not explicitly stated
* or returned. However;
* 
* Concerning what the function does and the operations carried out inside the body
* of the function: It takes a event target that refers to a row with information
* about a new player; obtains the flight number from that row; reads the name provided
* for that new player from an input field within that row; updates or resets the
* state of the input field to null (if not null). The newly provided name becomes
* p.name. Further steps are performed using properties created based on newPlayerName
* input; these include defining some object properties and appending newPlayer
* elements using a method createFlightPlayerRow and inserting that method's output
* within the <tBody> element having specified classes for each flight (targetTbody).
* MaxFlightNumber property is computed from that specific table with the appropriate
* classes. Lastly; return void and has no express or explicited function return statements
* 
* I will describe concisely what is returned based on those explanations: nothing
* is directly/explicitly stated or returned as "return" values are void functions.
* It only modifies and inserts information into the HTML table by manipulating object
* properties for an existing array and append child elements at specified indices
* or positions with row-based operations before resetting state and providing feedback
* on successful creation through text content changes.
*/
function addPlayerWithName(event) {
    const newPlayerInfoRow = event.target.closest("tr");
    let targetFlight = parseInt(newPlayerInfoRow.getAttribute("flight-number"));
    const input = newPlayerInfoRow.querySelector(".new-player-name");
    const newPlayerName = input.value;
    input.value = "";
    // if (new_player_name.length == 0) {
    //     return;
    // }
    const p = {};
    // getTargetTableAndTbody(targetFlight);
    const [targetTable, targetTbody] = getTargetTableAndTbody(targetFlight);
    p.names = newPlayerName;
    p.availability = [];
    const avails = countColumns(targetTbody);
    for (let i = 0; i < avails; i++) {
        p.availability.push(1);
    }
    let maxFlightNumber = targetFlight + 1;
    if (targetTable.classList.contains("bottom-flight")) {
        maxFlightNumber = targetFlight;
    }
    const pRow = createFlightPlayerRow(p, targetFlight, maxFlightNumber);
    targetTbody.insertBefore(pRow, targetTbody.rows[targetTbody.rows.length - 1]);
}

/**
* @description This function decreases the player's flight altitude by 1 unit.
* 
* @param {  } event - The `event` input parameter is not used within the body of the
* `switchPlayerFlightUp()` function.
* 
* @returns { any } The output returned by the `switchPlayerFlightUp` function is
* `undefined`. This is because the function does not return any value explicitly.
*/
function switchPlayerFlightUp(event) {
    switchPlayerFlight(event, -1);
}

/**
* @description This function Switches the player's flight direction down (1)
* 
* @param { object } event - The `event` input parameter is not used within the
* function body of `switchPlayerFlightDown`.
* 
* @returns { any } The function `switchPlayerFlightDown(event)` does not return any
* value as it is a void function.
*/
function switchPlayerFlightDown(event) {
    switchPlayerFlight(event, 1);
}

/**
* @description This function switches the flight number of a table row with the
* specified flight number by a given delta (positive or negative), and adjusts the
* order of the rows accordingly.
* 
* @param { object } event - The `event` input parameter is not used at all within
* the functionality of this JavaScript function `switchPlayerFlight()`. As such
* nothing is done with it and it may be omitted entirely.
* 
* @param { number } delta - The `delta` input parameter indicates whether the flight
* number should be increased (delta = 1) or decreased (delta = -1).
* 
* @returns { any } The output returned by the `switchPlayerFlight` function is not
* specified explicitly since it does not return any value explicitly. However. based
* on the function's functionality here is a concise description of the output:
* 
* The function switches the row of a player from one position to another within a
* table. Specifically; if the player is currently at flight number `x` and the delta
* parameter indicates a change of `y` flights up or down (where `y>0` for moving up
* and `y<0` for moving down):
* 
* The function adjusts the value of `currentFlight` accordingly (to either `x+y` or
* `x-y`), Finds the target row corresponding to the desired flight position; inserts
* the current player row into the appropriate position relative to the target row
* insertBefore()` or appendChild())
* and updates button visibility for moving up or down within the respective flight
* ranges based on the top and bottom classes for each table ( `top-flight`, and 'bottom-flight').
* Finally: it updates the attributed "flight-number' attribute to reflect the new
* flight number associated with target Row.
* In essence; this function reorganizes a player row within a particular table section
* for an airline management game or other suitable scenario requiring seat shuffling
* by users., based on some rule.
*/
function switchPlayerFlight(event, delta) {
    const targetRow = event.target.closest("tr");
    if (!targetRow) {
        console.error("No table row found");
        return;
    }

    const currentFlight = parseInt(targetRow.getAttribute("flight-number"));
    const targetFlight = currentFlight + delta;

    const [targetTable, targetTbody] = getTargetTableAndTbody(targetFlight);
    // Insert the targetRow into the target tbody as the 3rd row
    if (targetTbody.rows.length >= 2 && delta > 0) {
        targetTbody.insertBefore(targetRow, targetTbody.rows[2]);
    } else if (targetTbody.rows.length >= 2 && delta < 0) {
        targetTbody.insertBefore(targetRow, targetTbody.rows[targetTbody.rows.length - 1]);
    } else {
        targetTbody.appendChild(targetRow);
    }

    const macros = targetRow.querySelector(".player-macros");
    buttonUp = macros.querySelector(".move-up-button");
    buttonDown = macros.querySelector(".move-down-button");
    if (targetTable.classList.contains("top-flight")) {
        buttonUp.hidden = true;
    } else {
        buttonUp.hidden = false;
    }

    if (targetTable.classList.contains("bottom-flight")) {
        buttonDown.hidden = true;
    } else {
        buttonDown.hidden = false;
    }

    targetRow.setAttribute("flight-number", targetFlight);
}

/**
* @description This function handles clicks on TD elements with a class of 'availability',
* updates the value of the 'availability' attribute based on the previous value and
* the number of times the cell has been clicked (incrementing from 1 to 3), and
* applies a corresponding CSS background class based on the updated availability.
* 
* @param { object } event - The `event` input parameter provides information about
* the click event that triggered the function. It contains properties such as `target`,
* `stopPropagation`, and `preventDefault` that can be used to interact with the
* elements involved with the event.
* 
* @returns { integer } This function takes an event object as input and updates the
* "availability" attribute of the target element (a `<td>` with a certain class).
*/
function handleFlightTableClick(event) {
    let target = event.target;
    // Check if the clicked element is a td with class 'availability'
    if (target.tagName === "TD" && target.classList.contains("availability")) {
        let availability = parseInt(target.getAttribute("availability"), 10);

        // Increment the availability or reset to 1 if it's already 3
        availability = availability >= 3 ? 1 : availability + 1;

        // Update the attribute
        target.setAttribute("availability", availability);

        // Remove all bg- classes
        target.classList.remove("bg-free", "bg-busy", "bg-unavailable");

        // Add the new bg- class based on the updated availability
        switch (availability) {
            case 1:
                target.classList.add("bg-free");
                break;
            case 2:
                target.classList.add("bg-busy");
                break;
            case 3:
                target.classList.add("bg-unavailable");
                break;
        }
    }
}

/**
 * @description This function takes a dataset from a server and creates an HTML table
 * from it. It first builds the header row for each league and then loops through
 * each timeslot to add rows for dates and times.
 *
 * @param { object } data - The `data` input parameter is an array of objects that
 * contains information about each league's schedule.
 *
 * @returns { any } The output returned by the function is an HTML string that
 * represents a table with rows for each league's dates and times.
 */

function step4DataFromServer(data) {
    var parent = document.getElementById("clean-league");
    var child = parent.querySelector(".card-body");
    child.style.overflowX = "auto";
    let flightNumber = 1;
    let flightInput;
    let maxFlightNumber = data.length;
    data.forEach(function (league) {
        // Create League Header
        [flightNumber, flightInput] = createFlightHeader(flightNumber);

        child.appendChild(flightInput);

        // Create table
        const table = createFlightTable();
        table.id = "flight-" + String(flightNumber);
        table.classList.add("cleaned-flight");
        if (flightNumber == 1) {
            table.classList.add("top-flight");
        }
        if (flightNumber == maxFlightNumber) {
            table.classList.add("bottom-flight");
        }
        const tbody = document.createElement("tbody");

        // Create date and time rows
        let [dateRow, timeRow] = createFlightDateTimeRows(league);
        tbody.appendChild(dateRow);
        tbody.appendChild(timeRow);

        league.players.forEach(function (p) {
            const playerRow = createFlightPlayerRow(p, flightNumber, maxFlightNumber);
            tbody.appendChild(playerRow);
        });

        const addPlayerRow = createAddPlayerRowFlight(flightNumber);
        tbody.appendChild(addPlayerRow);

        table.appendChild(tbody);

        child.appendChild(table);

        table.addEventListener("click", handleFlightTableClick);
        flightNumber += 1;
    });
}

/**
* @description This function steps forward to step number 4 ( indicated by `stepIndex`
* variable being assigned value `4`) and then calls `step4DataFromServer()` with
* data passed as an argument( `data.data`).
* 
* @param { object } data - The `data` input parameter is passed from the previous
* step (i.e., `step3ClientSend`) and contains the data sent by the client to the server.
* 
* @returns { object } This function takes a single argument `data` and does the following:
* 
* 1/ It sets `stepIndex` to 4.
* 2/ It shows the current step (step 4).
* 3/ It calls `step4DataFromServer` with the data received from the server (which
* is contained within the `data` object).
* 
* The output returned by this function is not specified directly.
*/
function step4ServerResp(data) {
    stepIndex = 4;
    showStep(stepIndex);
    step4DataFromServer(data.data);
}

/**
 * @description This function sends data to the server as a CSV file.
 *
 * @returns { object } The output returned by this function is not defined because
 * it contains undefined statements and the function does not have a return statement.
 */
function stepIndex4Prep() {
    // const data = parseCellGroups();
    // sendToServer(data);

    // test
    fetch("/static/csv_league_import_example.json")
        .then((response) => response.json())
        .then((data) => {
            sendToServer(data, step4ServerResp);
        })
        .catch((error) => console.log("Error loading JSON: ", error));
}

/**
* @description This function takes a HTML table as input and returns an array of ISO
* datetime strings (format: "YYYY-MM-DDTHH:mm:ss") by combining the values from the
* date and time columns of each row.
* 
* @param { object } table - The `table` input parameter is used to pass a table
* element to the function.
* 
* @returns { array } The function `getCleanTimeSlots` takes a HTML table as input
* and returns an array of ISO date-time strings (YYYY-MM-DDTHH:mm:ss) extracted from
* the table's rows. It filters out incomplete or invalid date-time inputs and combines
* the date and time columns from each row to form the final ISO string.
*/
function getCleanTimeSlots(table) {
    const tbody = table.querySelector("tbody");
    const dateRow = tbody.rows[0];
    const timeRow = tbody.rows[1];
    const combinedDateTime = [];

    for (let i = 0; i < timeRow.cells.length; i++) {
        let dateInput = dateRow.cells[i + 1].querySelector("input");
        let timeInput = timeRow.cells[i].querySelector("input");

        if (dateInput && timeInput && dateInput.value && timeInput.value) {
            // Combine date and time directly
            let isoDateTime = dateInput.value + "T" + timeInput.value;
            combinedDateTime.push(isoDateTime);
        }
    }

    return combinedDateTime;
}

/**
* @description The provided function takes an array of HTML elements `titles` as
* input and returns an array of objects representing flight data.
* 
* @param { array } titles - The `titles` input parameter is an array of elements
* (presumably <title> tags) that the function processes to extract flight data.
* 
* @returns { object } The output returned by the `extractFlightData` function is an
* array of objects with properties such as `title`, `number`, and `playersAndAvailabilities`.
*/
function extractFlightData(titles) {
    return Array.from(titles).map((t) => ({
        name: t.value,
        number: parseInt(t.getAttribute("flight-number")),
        players_and_availabilities: [],
    }));
}

/**
* @description This function takes a HTML table and a flight number as input and
* extracts the player data from the table based on the given flight number.
* 
* @param { any } table - The `table` input parameter is passed a reference to the
* HTML table element that contains the player data.
* 
* @param { string } flightNumber - The `flightNumber` input parameter filters the
* rows to only include those with a matching flight number.
* 
* @returns { object } The `extractPlayerData` function takes a table and a flight
* number as input and returns an array of objects containing information about the
* players on that flight. Each object contains two properties: `name` (the player's
* name) and `availability` (the player's availability for that flight). The function
* filters the table rows to only include rows with a class of "player-row", then
* maps over those rows to extract the name and availability information.
*/
function extractPlayerData(table, flightNumber) {
    return Array.from(table.rows)
        .filter((row) => row.classList.contains("player-row"))
        .map((row) => ({
            name: row.cells[1].innerHTML,
            availability: Array.from(row.cells)
                .filter((cell) => cell.classList.contains("availability"))
                .map((cell) => parseInt(cell.getAttribute("availability"))),
        }));
}


/**
* @description This function takes a 'data' object and checks if the 'status' is
* 'success' with a redirect URL. If so it redirects the user to that URL.
* 
* @param { object } data - The `data` input parameter receives the flight booking
* data from the server-side API call.
* 
* @returns { object } This function takes data as an argument and logs it to the
* console before checking if the status is 'success' and there's a redirect URL. If
* both conditions are true), it redirects the user to the provided URL using `window.location.href`.
*/
function sentCleanFlightNext(data) {
    console.log(data);

    // Check if the status is 'success' and there's a redirect URL
    if (data.status === 'success' && data.redirect_url) {
        // Redirect to the URL provided by the server
        window.location.href = data.redirect_url;
    } else {
        // Handle other statuses or lack of redirect URL
        console.log("No redirection or handling other statuses.");
    }
}


/**
* @description This function takes a list of HTML tables with flight information and
* cleans the data by extracting the time slots and player availabilities.
* 
* @returns { object } Based on the code provided:
* 
* The output of this function is an object named "league" that has several properties:
* 
* 	- "timeslots": An array of cleaned time slots extracted from the first table element
* 	- "flights": An array of flight data objects
* 	- "players_and_availabilities": An array of player and availability objects for
* each flight
* 	- "cleaned": A string indicating whether the data has been cleaned (true) or not
* (false)
* 	- "name": A string with the name of the league
* 	- "type": A string with the type of the league
* 	- "game_duration": A float with the duration of the game (1.5 hours)
* 
* Note that the function also sends the cleaned data to a server using the "sendToServer"
* function and the "sentCleanFlightNext" callback.
*/
function convertCleanFlightsToJSONAndSend() {
    const tables = document.querySelectorAll(".cleaned-flight");
    const titles = document.querySelectorAll(".flight-title");
    let league = {};

    if (tables.length != 0) {
        league.timeslots = getCleanTimeSlots(tables[0]);
    }

    league.flights = titles.length != 0 ? extractFlightData(titles) : [];

    league.flights.forEach((flight) => {
        tables.forEach((table) => {
            if (table.id === `flight-${flight.number}`) {
                flight.players_and_availabilities = extractPlayerData(table, flight.number);
            }
        });
    });
    league.cleaned = "true";
    league.name = document.getElementById("league-name-input").value;
    if (league.name.length == 0) {
        league.name = "New League"
    }
    league.type = document.getElementById("league-type-input").value;
    league.game_duration = parseFloat(document.getElementById("game-duration-slider").value)/60.0;
    sendToServer(league, sentCleanFlightNext);
}

/**
 * @description This function sends a POST request to the server with the given `data`
 * parameter. It includes the CSRF token and sets up a promise chain to handle the
 * response from the server. If the response is not successful (200 OK), it rejects
 * the promise with the status message.
 *
 * @param { object } data - The `data` input parameter is passed as the request body
 * to the server when making a POST request.
 *
 * @returns { object } Based on the code provided the function sendToServer accepts
 * a parameter "data" and makes an asynchronous GET or POST request to the server.
 * The server response JSON data that can contain the "status", and other properties
 * of data such as "data".
 *
 * When successful it returns with data including 'status'.  Therefore output is
 * returned by this function with two cases; one if status=success console.logs ("Data
 * successfully ingested by the server"); if the return has failed an error message
 * of (server failure); or shows server did not provide a proper success status as
 * such the only known response it has no 'data' which the developer expects. This
 * can either produce no output or errors.
 */
function sendToServer(data, next) {
    const currentUrl = window.location.href;
    const csrf_token = document.querySelector('#hidden-form input[name="csrf_token"]').value;

    fetch(currentUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                return Promise.reject("Fetch failed; Server responded with " + response.status);
            }
            return response.json();
        })
        .then((data) => {
            if (data.status === "success") {
                console.log("Data successfully ingested by server.");
                next(data);
            } else {
                console.log("Failure: ", data.error);
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}
