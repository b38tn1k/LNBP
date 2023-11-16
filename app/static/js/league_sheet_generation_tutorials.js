let currentStep = 0;
let maxSteps = 5;
let isMouseDown = false;
let selectedCells = [];
let startPoint = null;
let cellGroups = [];

/**
* @description This function updates the width of a progress bar element based on a
* progress index and sets the aria-valuenow attribute to reflect the current progress
* percentage.
* 
* @param { number } progressIndex - The `progressIndex` input parameter passed to
* the `updateProgressBar` function represents the current step number out of the
* maximum steps (`maxSteps`).
* 
* @returns {  } The output returned by this function is the string value of the
* `style.width` property of the element with the ID "progress-bar", which is a
* percentage value representing the progress made so far (e.g., "15%", "30%", etc.).
*/
function updateProgressBar(progressIndex) {
    let progressPercentage = (progressIndex / maxSteps) * 100;
    let progressBar = document.getElementById("progress-bar");
    progressBar.style.width = `${progressPercentage}%`;
    progressBar.setAttribute("aria-valuenow", progressPercentage);
}

/**
* @description The `showStep` function displays a specific step of a multi-step form
* based on its index and updates the progress bar accordingly.
* 
* @param { number } index - The `index` input parameter passed to the `showStep()`
* function specifies which step should be displayed next.
* 
* @returns { number } The output returned by this function is the current div that
* corresponds to the specified index.
*/
function showStep(index) {
    let currentDiv;
    document.querySelectorAll(".step").forEach((div, i) => {
        if (i === index) {
            currentDiv = div;
            div.style.display = "block";
        } else {
            div.style.display = "none";
        }
    });

    // Read progress-index attribute from the current div
    let progressIndex = parseInt(currentDiv.getAttribute("progress-index"), 10);

    // Update progress bar
    updateProgressBar(progressIndex);

    document.getElementById("stepper").style.display = index === 0 ? "none" : "block";
    currentStep = index;
    let toDelete = [];
    for (let i = 0; i < cellGroups.length; i++) {
        if (cellGroups[i][0] >= currentStep) {
            toDelete.push(i);
        }
    }
    for (let i = toDelete.length - 1; i >= 0; i--) {
        cellGroups.splice(toDelete[i], 1);
    }
}

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
            table.style.display = "block";
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
    cellGroups = removeDuplicates()
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
* @description This function takes an integer `stepIndex` and performs the appropriate
* actions for that step index. It shows the next step by incrementing `stepIndex`
* unless a conditional check fails.
* 
* @param { number } stepIndex - The `stepIndex` input parameter determines which
* step of the workflow to execute next.
* 
* @returns { object } The output returned by the `performActionsAndMove` function
* is not specified.
*/
function performActionsAndMove(stepIndex) {
    if (stepIndex === 0) {
    } else if (stepIndex === 1) {
        stepIndex2Prep();
    } else if (stepIndex === 2) {
        stepIndex3Prep();
    } else if (stepIndex === 3) {
        cellGroups = removeDuplicates()
        sendCSVHTMLMap();
        
    }
    // Add more conditions for additional steps as needed
    // Increment only if initial checks pass
    showStep(stepIndex + 1);
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
            cells.forEach(cell => {
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
    console.log(cellGroups);
    const html = 1
    const type = 2
    result = []
    for (let i = 0; i < cellGroups.length; i++) {
        const htmlStrings = cellGroups[i][html].map(element => element.outerHTML);
        group = {
            'type' : cellGroups[i][type],
            'data' : htmlStrings.join(",")
        }
        result.push(group)
    }
    const tableElement = document.getElementById("csv-table-start");
    const tableHTML = tableElement ? tableElement.parentNode.innerHTML : "Table not found";
    // console.log(tableHTML);
    result.push({
        'type' : 'tableHTML',
        'data' : tableHTML
    })
    result.push({
        'type' : 'tableCSV',
        'data' : htmlTableToCsv(tableHTML)
    })
    return result
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
    var parent = document.getElementById("data-from-server");
    var child = parent.querySelector('.card-body'); // Make sure to include the '.' for class selector

    // Start building the table HTML
    var tableHTML = "<table>";

    // Loop through the leagues
    data.forEach(function(league) {
        // Add a row for each league
        // tableHTML += "<tr><td colspan='2'> <input placeholder='flight name'></input> </td></tr>"; // Assuming 'league' has a 'name' property

        // Initialize rows for dates and times
        var dateRow = "<tr><td></td>";
        var timeRow = "<tr><td></td>";

        // Loop through the timeslots for each league
        league.timeslots.forEach(function(ts) {
            // Parse the ISO date-time string
            var dateTime = new Date(ts); // Assuming 'ts' has an 'isoDateTime' property
            var date = dateTime.toISOString().split('T')[0];
            var time = dateTime.toTimeString().split(' ')[0];

            // Build rows for dates and times
            dateRow += "<td>" + date + "</td>";
            timeRow += "<td>" + time + "</td>";
        });

        // Close the date and time rows
        dateRow += "</tr>";
        timeRow += "</tr>";

        // Add the date and time rows to the table
        tableHTML += dateRow + timeRow;
    });

    // Close the table tag
    tableHTML += "</table>";

    // Set the innerHTML of the child element
    child.innerHTML = tableHTML;
}


/**
* @description This function sends data to the server as a CSV file.
* 
* @returns { object } The output returned by this function is not defined because
* it contains undefined statements and the function does not have a return statement.
*/
function sendCSVHTMLMap() {
    // const data = parseCellGroups();
    // sendToServer(data);

    // test
    fetch('/static/csv_league_import_example.json')
    .then(response => response.json())
    .then(data => {
        sendToServer(data);
    })
    .catch(error => console.log("Error loading JSON: ", error));
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
function sendToServer(data) {
    const currentUrl = window.location.href;
    const csrf_token = document.querySelector('#hidden-form input[name="csrf_token"]').value;

    fetch(currentUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return Promise.reject("Fetch failed; Server responded with " + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "success") {
            console.log("Data successfully ingested by server.");
            stepIndex = 4;
            showStep(stepIndex)
            step4DataFromServer(data.data);
        } else {
            console.log("Failure: ", data.error);
        }
    })
    .catch(error => console.log("Fetch error: ", error));
}

document.querySelectorAll("textarea").forEach((textarea) => {
    textarea.addEventListener("paste", async function (e) {
        const text = e.clipboardData.getData("text/html"); // Gets the HTML content
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        // Check if the document contains a <table> tag
        if (doc.querySelector("table")) {
            csv = htmlTableToCsv(text);
            document.getElementById("csv-input").setAttribute("google-csv", csv);
        } else {
            document.getElementById("csv-input").setAttribute("google-csv", "None");
        }
        setTimeout(function () {
            window.scrollTo(0, 0);
        }, 0);
    });
});

document.addEventListener("keydown", function (event) {
    if (event.code === "Enter") {
        highlightAndSelectCells();
    }
});

document.getElementById("csv-button").addEventListener("click", () => showStep(1));
document.getElementById("back-button").addEventListener("click", () => showStep(currentStep - 1));
document.getElementById("next-button").addEventListener("click", () => performActionsAndMove(currentStep));

showStep(0);
