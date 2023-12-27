let currentStep = 0;
let maxSteps = 5;
let isMouseDown = false;
let selectedCells = [];
let startPoint = null;
let cellGroups = [];
let undoStack = [];

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
    let icon = document.createElement("i");
    icon.classList.add("fe", "fe-loader");
    let b = document.getElementById("next-button");
    b.innerHTML = "";
    b.appendChild(icon);

    if (stepIndex === 0) {
    } else if (stepIndex === 1) {
        stepIndex2Prep();
    } else if (stepIndex === 2) {
        stepIndex3Prep();
    } else if (stepIndex === 3) {
        cellGroups = removeDuplicates();
        stepIndex4Prep();
    } else if (stepIndex == 4) {
        convertCleanFlightsToJSONAndSend();
        stepIndex += 1;
    }
    // Add more conditions for additional steps as needed
    // Increment only if initial checks pass
    if (stepIndex != 5) {
        showStep(stepIndex + 1);
        b.innerHTML = "Next";
        icon.remove();
    }
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
