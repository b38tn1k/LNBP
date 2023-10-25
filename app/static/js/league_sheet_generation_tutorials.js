let currentStep = 0;
let maxSteps = 5;
let isMouseDown = false;
let selectedCells = [];
let startPoint = null;
let cellGroups = [];

function updateProgressBar(progressIndex) {
    let progressPercentage = (progressIndex / maxSteps) * 100;
    let progressBar = document.getElementById("progress-bar");
    progressBar.style.width = `${progressPercentage}%`;
    progressBar.setAttribute("aria-valuenow", progressPercentage);
}

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
function checkCellGroups() {
    const tabContentDiv = document.querySelector(".data-label-tab-contents");
    if (cellGroups.length === 0) {
        tabContentDiv.innerHTML = "Please go back and select at least one flight";
        return false;
    }
    return true;
}

// Function to generate an HTML table from a given cell group
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
function appendTableToTabContent(table) {
    const tabContentDiv = document.querySelector(".data-label-tab-contents");
    tabContentDiv.appendChild(table);
}

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

function toggleFlightSubTableVisibility(targetId) {
    // Select all tables with the class 'flight-sub-table'
    const tables = document.querySelectorAll(".flight-sub-table");

    // for (let id = 0; id < cellGroups.length; id++) {
    //     tearDownTableInteraction(String(id));
    // }
    // setUpTableInteraction(String(targetId));

    // Iterate over each table element
    tables.forEach((table) => {
        if (table.id === targetId) {
            // Make the table with the matching id visible
            table.style.display = "block";
        } else {
            // Hide other tables
            table.style.display = "none";
        }
    });
}

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

function stepIndex3Prep() {
    tearDownTableInteraction("csv-table-start");
    cellGroups = cellGroups.filter((group) => group[1].length !== 0 && group[0] == 2);
    // Step 2: Remove duplicate entries
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
    cellGroups = uniqueGroups;
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

function performActionsAndMove(stepIndex) {
    if (stepIndex === 0) {
    } else if (stepIndex === 1) {
        stepIndex2Prep();
    } else if (stepIndex === 2) {
        stepIndex3Prep();
    }
    // Add more conditions for additional steps as needed
    // Increment only if initial checks pass
    showStep(stepIndex + 1);
}

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

function setUpTableInteraction(id) {
    const table = document.getElementById(id);
    table.addEventListener("mousedown", handleMouseDown);
    table.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
}

function tearDownTableInteraction(id) {
    const table = document.getElementById(id);
    table.removeEventListener("mousedown", handleMouseDown);
    table.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);
}

function clearSelections() {
    selectedCells.forEach((cell) => cell.classList.remove("table-primary"));
    selectedCells = [];
}

function selectRectangle(topRow, bottomRow, leftCol, rightCol) {
    for (let i = topRow; i <= bottomRow; i++) {
        for (let j = leftCol; j <= rightCol; j++) {
            const cell = document.querySelector(`[data-row='${i}'][data-col='${j}']`);
            cell.classList.add("table-primary");
            selectedCells.push(cell);
        }
    }
}

function highlightAndSelectCells() {
    for (let cell of selectedCells) {
        cell.classList.remove("table-primary");
        cell.classList.add("table-secondary");
    }
    const newGroup = [];
    selectedCells.forEach((cell) => newGroup.push(cell));
    cellGroups.push([currentStep, newGroup]);
    console.log(cellGroups);
}

function handleMouseDown(event) {
    isMouseDown = true;

    const cell = event.target;
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

function handleMouseMove(event) {
    if (isMouseDown) {
        // Existing logic can remain here if needed
    }
}

function handleMouseUp() {
    isMouseDown = false;
    // Logic for finished selection can go here
}

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

document.getElementById("csv-button").addEventListener("click", () => showStep(1));
document.getElementById("create-button").addEventListener("click", () => showStep(2));
document.getElementById("back-button").addEventListener("click", () => showStep(currentStep - 1));
document.getElementById("next-button").addEventListener("click", () => performActionsAndMove(currentStep));

showStep(0);
