class Diff {
    /**
     * @description This function is a constructor that takes three arguments - `event`,
     * `ids`, and `values` - and assigns them to the corresponding properties of an object.
     *
     * @param {  } event - The `event` input parameter is not used within the function
     * and is therefore ignored.
     *
     * @param { array } ids - The `ids` input parameter is an array of identifiers that
     * corresponds to the indexes of the items being added or updated.
     *
     * @param { array } values - The `values` input parameter is an array of values
     * associated with the IDs passed through the `ids` parameter.
     *
     * @returns { object } The output of this function is undefined.
     */
    constructor(event, ids, values) {
        this.event = event;
        this.ids = ids;
        this.values = values;
    }
}

const delta = [];
let pushTSCounter = 0;

/**
 * @description This function updates a `delta` array with new differences between
 * two arrays of data.
 *
 * @param { object } data - The `data` input parameter is passed as an object with
 * properties 'event', 'ids' and 'values' representing the updated information.
 *
 * @returns { object } The `updateDelta` function updates an existing diff or adds a
 * new one to an array called `delta`, depending on if an existing diff with the same
 * event and IDs already exists.
 */
function updateDelta(data) {
    // Check if a diff with the same event and IDs already exists in the delta array
    const existingDiffIndex = delta.findIndex(
        (diff) => diff.event === data.event && JSON.stringify(diff.ids) === JSON.stringify(data.ids)
    );

    if (existingDiffIndex !== -1) {
        // Update the existing diff with the new value
        delta[existingDiffIndex].values = data.values;
    } else {
        // Add the new diff to the delta array
        delta.push(data);
    }

    console.log("DIFF UPDATE");
    for (let diff of delta) {
        logDiff(diff);
    }
}

/**
 * @description This function logs a diff object to the console. It takes an object
 * diff as its argument and outputs a string to the console with the following format:
 *
 * Event=<event>, IDs=<IDs_as_string>, Values=<values_as_string>
 *
 * where:
 *
 * 	- Event is the diff event type (e.g.
 *
 * @param { object } diff - The `diff` input parameter is an object containing
 * information about the difference between two states of a system or process.
 *
 * @returns { any } The output of this function is a string representation of the
 * differences between two objects. The string includes three parts: `Event`, `IDs`,
 * and `Values`. The `Event` part is a fixed string that is always the same. The `IDs`
 * and `Values` parts are arrays of key-value pairs representing the differences
 * between the two objects.
 */
function logDiff(diff) {
    let idsString = JSON.stringify(diff.ids);
    let valuesString = JSON.stringify(diff.values);

    // If IDs is an object, convert it to a string representation of key-value pairs
    if (typeof diff.ids === "object") {
        idsString = Object.entries(diff.ids)
            .map(([key, value]) => `${key}:${value}`)
            .join(", ");
    }

    // If values is an object, convert it to a string representation of key-value pairs
    if (typeof diff.values === "object") {
        valuesString = Object.entries(diff.values)
            .map(([key, value]) => `${key}:${value}`)
            .join(", ");
    }

    console.log(`Event=${diff.event}, IDs=${idsString}, Values=${valuesString}`);
}

/**
 * @description This function formats a JavaScript `Date` object as a string following
 * the ISO 8601 format: `YYYY-MM-DDTHH:mm:ss.SSS`.
 *
 * @param { object } dateTime - The `dateTime` input parameter is a JavaScript Date
 * object that is being passed into the `formatLocalDateTime` function to be formatted
 * into a string representation of the current date and time.
 *
 * @returns { string } The output returned by the `formatLocalDateTime` function is
 * a string representation of a date and time value passed as an argument to the function.
 */
function formatLocalDateTime(dateTime) {
    const year = dateTime.getFullYear();
    const month = String(dateTime.getMonth() + 1).padStart(2, "0"); // Month is 0-based
    const day = String(dateTime.getDate()).padStart(2, "0");
    const hours = String(dateTime.getHours()).padStart(2, "0");
    const minutes = String(dateTime.getMinutes()).padStart(2, "0");
    const seconds = "00";
    const milliseconds = "000";
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}`;
}

document.addEventListener("DOMContentLoaded", function () {
    // INFO
    const info = document.getElementById("infoElement");
    const title = document.getElementById("league-name-input");
    title.value = info.getAttribute("leagueName");

    title.addEventListener("input", function () {
        updateDelta(new Diff("name", "league_name", this.value));
    });

    const gameDuration = info.getAttribute("leagueGameDuration");
    const durationSlider = document.getElementById("game-duration-slider");
    const displaySpan = document.getElementById("duration-display");
    displaySpan.textContent = gameDuration;
    durationSlider.value = parseInt(gameDuration);

    /**
     * @description This function updates the text content of an element with the ID
     * "displaySpan" to a given value.
     *
     * @param { string } value - The `value` input parameter passes a string value to the
     * `displaySpan.textContent` property setter to update the text content of the element
     * with the ID "displaySpan".
     *
     * @returns {  } The function `updateDisplay(value)` takes a single argument `value`,
     * and it sets the `textContent` of an element with an ID `displaySpan` to the provided
     * value.
     */
    function updateDisplay(value) {
        displaySpan.textContent = value;
    }

    durationSlider.addEventListener("input", function () {
        updateDisplay(this.value);
        updateDelta(new Diff("duration", "game_duration", parseInt(this.value)));
    });

    const typeSelector = document.getElementById("league-type-input");
    typeSelector.value = info.getAttribute("leagueType");
    typeSelector.addEventListener("change", function () {
        updateDelta(new Diff("type", "league_type", this.value));
    });

    updateDisplay(rangeInput.value);

    // SCHEDULE
    const leagueTypeSelector = document.getElementById("league-type-input");
    leagueTypeSelector.value = info.getAttribute("leagueType");
    const dates = document.querySelectorAll(".timeslot_header");
    for (let date of dates) {
        dateString = date.getAttribute("startTime");
        timeslot = date.getAttribute("ts");
        flatpickr(date, {
            defaultDate: new Date(date.getAttribute("startTime")),
            enableTime: true,
            dateFormat: "m/d H:i",
            /**
             * @description This function updates the values of a `<time>` element's `innerHTML`
             * property and a `ts` attribute with the selected date using `Date()` constructor
             * and `formatLocalDateTime()` method.
             *
             * @param { array } selectedDates - The `selectedDates` input parameter is an array
             * of dates selected by the user through a dropdown or other interface element.
             *
             * @param { string } dateStr - Based on the code provided:
             *
             * The `dateStr` input parameter is a string representing the date displayed on the
             * webpage via the `innerHTML` assignment.
             *
             * @returns { object } The function takes two arguments `selectedDates` and `dateStr`.
             * It updates the `innerHTML` of an element with the value of `dateStr`, and then
             * creates a new `Date` object from the selected dates.
             */
            onChange: function (selectedDates, dateStr) {
                date.innerHTML = dateStr;
                const newDate = new Date(selectedDates);
                updateDelta(new Diff("timeslot", parseInt(date.getAttribute("ts")), formatLocalDateTime(newDate)));
                for (let otherDate of dates) {
                    const otherTimeslot = otherDate.getAttribute("ts");
                    if (otherTimeslot === timeslot) {
                        console.log(otherDate);
                        // TODO: Update matching dates
                    }
                }
            },
        });
    }

    const flightNameInputs = document.querySelectorAll(".flight-name-input");
    for (let input of flightNameInputs) {
        input.addEventListener("change", function () {
            updateDelta(new Diff("flight_name", parseInt(this.getAttribute("flight")), this.value));
        });
    }

    const flightCount = parseInt(info.getAttribute("flightCount"));
    const flightTables = document.querySelectorAll(".flight-sub-table");
    for (let table of flightTables) {
        if (parseInt(table.getAttribute("flight-number")) == 1) {
            table.classList.add("top-flight");
        }
        if (parseInt(table.getAttribute("flight-number")) == flightCount) {
            table.classList.add("bottom-flight");
        }
    }
    const macro_buttons = document.querySelectorAll(".player_macro_button");
    for (let button of macro_buttons) {
        const macroType = button.getAttribute("macro-type");
        const flightNumber = parseInt(button.getAttribute("flight-number"));
        parent_card = button.closest(".card");
        if (macroType == "up" && flightNumber == 1) {
            button.hidden = true;
        }
        if (macroType == "down" && flightNumber == flightCount) {
            button.hidden = true;
        }

        switch (macroType) {
            case "up":
                button.addEventListener("click", moveUpCallback);
                break;

            case "down":
                button.addEventListener("click", moveDownCallback);
                break;

            case "remove":
                button.addEventListener("click", removeCallback);
                break;
        }
    }

    const facilities = document.querySelectorAll(".facility-checker");
    facilities.forEach((f) => {
        f.addEventListener("change", () => {
            updateDelta(new Diff("facility_in_league", parseInt(f.getAttribute("facility")), f.checked));
        });
    });

    const addPlayerButton = document.getElementById("add-player-button");
    if (addPlayerButton) {
        addPlayerButton.addEventListener("click", () => {
            const playerSelector = document.getElementById("add_player_select");
            const playerID = parseInt(playerSelector.value);
            const playerName = playerSelector.options[playerSelector.selectedIndex].textContent;
            const flightID = parseInt(document.getElementById("add_player_flight_select").value);
            if (playerID != -1 && flightID != -1) {
                updateDelta(new Diff("add_player_to_league", { player: playerID, flight: flightID }, 0));
                addNewPlayerToFlight(playerName, playerID, flightID);
            }
        });
    }

    document
        .querySelectorAll(".schedule-table")
        .forEach((table) => table.addEventListener("click", handleFlightTableClick));

    const leagueRules = document.querySelectorAll(".league-rules");
    leagueRules.forEach((rule) => {
        rule.addEventListener("change", (event) => {
            leagueRulesChangeCallback(event, leagueRules);
        });
    });

    document.getElementById("save-button").addEventListener("click", saveButtonCallback);
    // document.getElementById("push-timeslot-button").addEventListener("click", pushTimeSlot);
    // document.getElementById("pop-timeslot-button").addEventListener("click", popTimeSlot);

    document.querySelectorAll(".reveal-after").forEach((div) => (div.style.display = "block"));
});

/**
 * @description This function adds an event listener to all nav links and hides all
 * existing active state and information tabs.
 *
 * @param { object } e - The `e` input parameter is an event object that contains
 * information about the click event that triggered the function.
 *
 * @returns { object } This function takes an event object as an argument (e) and
 * performs the following actions:
 *
 * 1/ Logs the event object to the console.
 * 2/ Removes the "active" class from all elements with the class ".nav-link".
 * 3/ Sets all elements with the class ".nav-info-tab" to hidden.
 * 4/ Adds the "active" class to the current element (e).
 * 5/ Retrieves the target attribute of the current element and logs it to the console.
 * 6/ Finds the element with the ID specified by the target attribute and sets its
 * hidden property to false.
 *
 * The output returned by this function is:
 *
 * 	- The current element with the class ".nav-link" has the "active" class added and
 * its ID is logged to the console.
 * 	- All elements with the class ".nav-info-tab" are set to hidden.
 * 	- The element with the ID specified by the target attribute is revealed (its
 * hidden property is set to false).
 */
function navClicker(e) {
    document.querySelectorAll(".nav-link").forEach((i) => {
        i.classList.remove("active");
    });

    document.querySelectorAll(".nav-info-tab").forEach((i) => {
        i.hidden = true;
    });

    e.classList.add("active");
    let target = e.getAttribute("target");
    let info = document.getElementById(target);
    info.hidden = false;
}

/**
 * @description This function decrements a counter called `pushTSCounter` and updates
 * the value of an HTML attribute called `starttime` based on the previous value of
 * `pushTSCounter`.
 *
 * @returns {  } Based on the code provided:
 *
 * The `pushTimeSlot()` function:
 *
 * 1/ Decrements the `pushTSCounter` variable by 1.
 * 2/ Queryes all elements with the class name `.schedule-table` (presumably a table
 * containing schedules).
 * 3/ Selects the first (`0`) element of the array using `querySelector()` and retrieves
 * the `<thead>` element within it.
 * 4/ Selects the `<tr>` element within the `<thead>`, and then selects all the `<th>`
 * elements within that row using `querySelectorAll()`.
 * 5/ Retrieves the text content of the last `<th>` element (based on the `starttime`
 * attribute).
 * 6/ Updates a Diff object with the "push_time_slot" key and the values `pushTSCounter`,
 * `starttime`.
 *
 * The output of this function would be the text content of the last `<th>` element
 * within the first table (in the .schedule-table class), after subtracting 1 from
 * the pushTSCounter variable.
 */
function pushTimeSlot() {
    pushTSCounter -= 1;
    schedules = document.querySelectorAll(".schedule-table");
    const tableHead = schedules[0].querySelector("thead");
    const headerRow = tableHead.querySelector("tr");
    const headerColumns = headerRow.querySelectorAll("th");
    starttime = headerColumns[headerColumns.length - 1].getAttribute("starttime");
    updateDelta(new Diff("push_time_slot", pushTSCounter, starttime));
}

// Define the function for the "popTimeSlot" event handler
/**
 * @description This function does nothing because it is undefined.
 *
 * @returns { any } The function `popTimeSlot()` will log the message "Pop Time Slot
 * button clicked!" to the console.
 */
function popTimeSlot() {
    // Add your logic for popping a timeslot here
    console.log("Pop Time Slot button clicked!");
}

/**
 * @description The provided JavaScript function `alignRules` takes two input elements
 * with `value` properties (`min` and `max`), and updates the `value` property of the
 * `max` element to be equal to the value of the `min` element if the former is greater
 * than the latter.
 *
 * @param { object } min - The `min` input parameter specifies the smaller value of
 * the two arrays being compared.
 *
 * @param { object } max - The `max` input parameter is passed by reference and updated
 * within the function to be set equal to the value of `min` if `min` is greater than
 * `max`.
 *
 * @returns { any } The function `alignRules` takes two parameters `min` and `max`,
 * both of which are `HTMLInputElement` objects representing input fields.
 */
function alignRules(min, max) {
    if (parseInt(min.value) > parseInt(max.value)) {
        max.value = parseInt(min.value);
    }
}

/**
 * @description This function takes an array of league rules and updates the values
 * for each rule. It aligns the minimum and maximum values for certain rules (games
 * total/day), and converts values to appropriate data types (integer/float).
 *
 * @param { object } event - The `event` input parameter is not used or referenced
 * within the provided code snippet.
 *
 * @param { object } allRules - The `allRules` input parameter is an array of all the
 * league rules that are being updated.
 *
 * @returns { object } Based on the code provided:
 *
 * The `leagueRulesChangeCallback` function takes two parameters: `event` and `allRules`.
 * It updates the `minGT`, `maxGT`, `minGD`, `maxGD`, `minC`, and `maxC` variables
 * with the values from the `allRules` array. It then aligns the rules using the
 * `alignRules` function.
 */
function leagueRulesChangeCallback(event, allRules) {
    newRules = {};
    let minGT, maxGT, minGD, maxGD, minC, maxC;
    for (let rule of allRules) {
        switch (rule.name) {
            case "min_games_total":
                minGT = rule;
                break;
            case "max_games_total":
                maxGT = rule;
                break;
            case "min_games_day":
                minGD = rule;
                break;
            case "max_games_day":
                maxGD = rule;
                break;
            case "min_captained":
                minC = rule;
                break;
            case "max_captained":
                maxC = rule;
                break;
        }
    }

    alignRules(minGT, maxGT);
    alignRules(minGD, maxGD);
    alignRules(minC, maxC);

    for (let rule of allRules) {
        value = rule.value;
        if (rule.name != "assume_busy") {
            if (rule.name == "minimum_subs_per_game") {
                value = parseFloat(value);
            } else {
                value = parseInt(value);
            }

            if (value < 0) {
                rule.value = 0;
                value = 0;
            }
        }
        newRules[rule.name] = value;
    }
    updateDelta(new Diff("rule_update", 0, newRules));
}

/**
 * @description This function saves the data represented by the `delta` variable to
 * the server via a web request.
 *
 * @param { object } event - The `event` parameter is not used anywhere inside the
 * `saveButtonCallback` function. It is passed as an argument to the function but is
 * not referred to or utilized within the code.
 *
 * @returns {  } This function takes an `event` parameter and returns nothing (i.e.,
 * it does not return a value).
 */
function saveButtonCallback(event) {
    const saveString = JSON.stringify(delta);
    sendToServer({ msg: "save", data: saveString });
}

/**
 * @description This function sends a POST request to the current URL with the given
 * data and handles the response from the server.
 *
 * @param { object } data - The `data` input parameter is passed to the fetch API as
 * the body of the request.
 *
 * @returns { Promise } This function takes a `data` parameter and sends it to the
 * server using fetch API. It then handles the response from the server and logs
 * messages to the console.
 */

function sendToServer(data, success = null, failure = null) {
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
                if (success) {
                    success();
                }
            } else {
                console.log("Failure: ", data.error);
                if (failure) {
                    failure();
                }
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}

// function sendToServer(data) {
//     const currentUrl = window.location.href;
//     const csrf_token = document.querySelector('#hidden-form input[name="csrf_token"]').value;

//     fetch(currentUrl, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrf_token,
//         },
//         body: JSON.stringify(data),
//     })
//         .then((response) => {
//             if (!response.ok) {
//                 return Promise.reject("Fetch failed; Server responded with " + response.status);
//             }
//             return response.json();
//         })
//         .then((data) => {
//             if (data.status === "success") {
//                 console.log("Data successfully ingested by server.");
//                 window.location.reload();
//             } else {
//                 console.log("Failure: ", data.error);
//             }
//         })
//         .catch((error) => console.log("Fetch error: ", error));
// }

/**
 * @description This function adds a new player to a flight table by cloning an
 * existing row and modifying its content with the given player name and ID.
 *
 * @param { string } playerName - The `playerName` input parameter specifies the name
 * of the player to be added to the flight.
 *
 * @param { string } playerID - The `playerID` input parameter is used to set the
 * `playerID` attribute for each new row added to the flight table.
 *
 * @param { number } flightID - The `flightID` input parameter identifies which flight
 * the new player should be added to.
 *
 * @returns { object } The `addNewPlayerToFlight` function takes three arguments:
 * `playerName`, `playerID`, and `flightID`. It first finds the target table with the
 * given flight ID and clones the first row of its tbody element. It then modifies
 * the content of the cloned row by setting the player name and player ID attributes.
 * Next it updates the availability cells and macro buttons on the row using event listeners.
 */
function addNewPlayerToFlight(playerName, playerID, flightID) {
    // Find flight table
    const flightTables = document.querySelectorAll(".flight-sub-table");
    let targetTable;
    for (let table of flightTables) {
        if (parseInt(table.getAttribute("flight")) == flightID) {
            targetTable = table;
        }
    }

    // Find the tbody in the target table
    const tbody = targetTable.querySelector("tbody");

    // Clone the first tr element in the tbody
    const firstRow = tbody.querySelector("tr:first-child");
    const newRow = firstRow.cloneNode(true); // true to clone child nodes

    // Modify the content of the new row
    newRow.cells[1].textContent = playerName;

    // Set player ID attribute
    newRow.setAttribute("playerID", playerID);

    // Update availability cells in the new row
    const availabilityCells = newRow.querySelectorAll(".availability");
    availabilityCells.forEach((cell) => {
        cell.classList.remove("bg-busy", "bg-unavailable"); // Remove previous classes
        cell.classList.add("bg-free"); // Set default class
        cell.title = playerName;
        cell.setAttribute("player", playerID);
        cell.setAttribute("availability", 1); // Set availability attribute to 1
    });

    // Update macro buttons in the new row
    const macroButtons = newRow.querySelectorAll(".player_macro_button");
    macroButtons.forEach((button) => {
        button.setAttribute("flight", flightID);
        button.setAttribute("playerID", playerID);
        const macroType = button.getAttribute("macro-type");
        switch (macroType) {
            case "up":
                button.addEventListener("click", moveUpCallback);
                break;

            case "down":
                button.addEventListener("click", moveDownCallback);
                break;

            case "remove":
                button.addEventListener("click", removeCallback);
                break;
        }
    });

    // Append the new row to the tbody
    tbody.appendChild(newRow);
}

/**
 * @description The `moveUpCallback` function moves the player's flight direction
 * down by one step when triggered by an event.
 *
 * @param { object } event - The `event` input parameter is not used or referenced
 * within the function body of `moveUpCallback`.
 *
 * @returns { any } The output returned by the `moveUpCallback` function is `undefined`.
 */
function moveUpCallback(event) {
    switchPlayerFlight(event, -1);
}

/**
 * @description The function `moveDownCallback` is called when the user moves down
 * (via arrow key or other keyboard input) during a game or simulation.
 *
 * @param { any } event - The `event` parameter is not used within the function
 * `moveDownCallback`. It is passed as an argument to the function but is not referred
 * to or acted upon within the code.
 *
 * @returns { any } The function `moveDownCallback` does not return any value.
 */
function moveDownCallback(event) {
    switchPlayerFlight(event, 1);
}

/**
 * @description This function removes a callback event listener from an HTML table
 * row element ( `<tr>` ) that is closest to the event target .
 *
 * @param { object } event - The `event` input parameter is not used within the
 * `removeCallback` function.
 *
 * @returns { object } The function `removeCallback` does not return anything since
 * it is defined as a function with no `return` statement. Instead of returning any
 * value itself.  It logs the `row` element that is closest to the `event.target`
 * element inside the event handler of whatever `event` is passed into this function
 * call on line `<event>`.
 */
function removeCallback(event) {
    const row = event.target.closest("tr");
    const playerID = parseInt(row.getAttribute("playerID"));
    updateDelta(new Diff("remove_player_from_league", { player: playerID }, 0));
    row.remove();
}

/**
 * @description This function retrieves the `tbody` element of a table with an ID
 * containing a specified flight number and returns an array containing the table and
 * its tbody element.
 *
 * @param { string } targetFlight - The `targetFlight` input parameter specifies the
 * ID of the table to be retrieved.
 *
 * @returns { array } The output of the `getTargetTableAndTbody` function is an array
 * containing two elements:
 *
 * 1/ The `targetTable` element (an HTML table element with an id containing the value
 * of `targetFlight`).
 * 2/ The `targetTbody` element (a tbody element within the target table).
 *
 * The function takes a `targetFlight` parameter and returns these two elements if
 * they exist and are found within the DOM.
 */
function getTargetTableAndTbody(targetFlight) {
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
 * @description This function allows a user to switch a player's flight by clicking
 * on their row and increasing or decreasing their flight number.
 *
 * @param { any } event - The `event` input parameter is not used within the functionality
 * of the `switchPlayerFlight` function. It is passed to the function as an undefined
 * value and then ignored.
 *
 * @param { integer } delta - The `delta` input parameter specifies the difference
 * between the current flight number and the new flight number that the row should
 * be moved to.
 *
 * @returns {  } Based on the code provided:
 *
 * The `switchPlayerFlight` function takes two parameters: `event` and `delta`. It
 * retrieves the currently selected table row using `event.target.closest("tr")` and
 * calculates the new flight number by adding or subtracting the given delta to the
 * current flight number. Then it updates the DOM elements related to the target
 * flight and modifies the button visibility based on whether the table is a top or
 * bottom flight table. Finally ,it returns undefined .
 */
function switchPlayerFlight(event, delta) {
    const targetRow = event.target.closest("tr");
    if (!targetRow) {
        console.error("No table row found");
        return;
    }

    const currentFlight = parseInt(targetRow.getAttribute("flight-number"));
    const targetFlight = currentFlight + delta;
    targetRow.setAttribute("flight-number", targetFlight);

    const [targetTable, targetTbody] = getTargetTableAndTbody(targetFlight);

    const flightID = parseInt(targetTable.getAttribute("flight"));
    const playerID = parseInt(targetRow.getAttribute("playerID"));
    updateDelta(new Diff("change_flight", { player: playerID }, { new_flight: flightID }));

    // Insert the targetRow into the target tbody as the 3rd row
    if (targetTbody.rows.length >= 2 && delta > 0) {
        targetTbody.insertBefore(targetRow, targetTbody.rows[0]);
    } else if (targetTbody.rows.length >= 2 && delta < 0) {
        targetTbody.insertBefore(targetRow, targetTbody.rows[targetTbody.rows.length]);
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
 * @description This function updates the availability of a seat at a flight by
 * clicking on the TD element representing that seat.
 *
 * @param {  } event - The `event` input parameter passed to the function provides
 * information about the user's click event on the table cell element being handled.
 */
function handleFlightTableClick(event) {
    let target = event.target;
    // Check if the clicked element is a td with class 'availability'
    if (target.tagName === "TD" && target.classList.contains("availability")) {
        let availability = parseInt(target.getAttribute("availability"), 10);

        // Increment the availability or reset to 1 if it's already 3
        availability = availability >= 3 ? 1 : availability + 1;

        const ids = {
            timeslot: parseInt(target.getAttribute("timeslot")),
            player: parseInt(target.getAttribute("player")),
        };

        updateDelta(new Diff("availability", ids, availability));

        // Update the attribute
        target.setAttribute("availability", availability);

        // Remove all bg- classes
        target.classList.remove("bg-free", "bg-busy", "bg-unavailable", "bg-populated");

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
 * @description This function prepares a button for loading by adding a spinner and
 * changing its appearance.
 *
 * @returns {  } The function `scheduleWizardButtonCallback` takes no arguments and
 * returns nothing (it is a void function). It sets up a button's loading state using
 * `setButtonLoading`, prepares data to be sent to the server via `sendToServer`, and
 * defines two callback functions: `success` and `failure`. The output returned by
 * this function is nothing; it does not return any values.
 */
function scheduleWizardButtonCallback() {
    let button = document.getElementById("run-schedule-wizard");
    let loaderClass = setButtonLoading(button, "fe-star");

    const data = {
        msg: "schedule-all",
    };

    /**
     * @description This function updates the appearance of a button using various CSS
     * classes to display a check mark and a success icon (a star) after a successful operation.
     *
     * @returns { any } This function does not return any value or output.
     */
    function success() {
        flashButtonResult(button, "fe-check-circle", "fg-success", loaderClass, "fe-star");
        window.location.reload();
    }

    /**
     * @description This function sets the button's icon to a failuresymbol with a red
     * border and star rating.
     *
     * @returns { any } The output returned by the `failure` function is:
     *
     * 	- A flashing button with the button identifier `button`, displaying a "x" circle
     * icon and the text "fg-failure".
     */
    function failure() {
        flashButtonResult(button, "fe-x-circle", "fg-failure", loaderClass, "fe-star");
        window.location.reload();
    }
    sendToServer(data, success, failure);
}

/**
 * @description This function sets the loading state of a button by adding a "fe-loader"
 * class to the button's icon element (represented by "r") and removing any previously
 * assigned "defaultClass".
 *
 * @param { object } button - The `button` input parameter is used to select the
 * button element that should have its loading state changed.
 *
 * @param { string } defaultClass - The `defaultClass` input parameter is used to
 * specify a default class that will be removed from the icon element before adding
 * the "fe-loader" class.
 *
 * @returns { string } The function `setButtonLoading()` takes a button element and
 * a default class as arguments. It removes the default class from the button's icon
 * (represented by an `i` element) and adds the class "fe-loader". The output returned
 * by the function is the name of the added class i.e.
 */
function setButtonLoading(button, defaultClass) {
    let r = button.querySelector("i");
    r.classList.remove(defaultClass);
    r.classList.add("fe-loader");
    return "fe-loader";
}

/**
 * @description This function toggles the class names "c1" and "c2" on an i-tag within
 * a button element for 1 second before reverting back to the default class "defaultClass".
 *
 * @param {  } button - The `button` input parameter is not used anywhere within the
 * provided function implementation.
 *
 * @param { string } c1 - In the given function `flashButtonResult`, the `c1` parameter
 * is used to add a class to the element (`i`) immediately after removing the `removableClass`.
 *
 * @param { string } c2 - The `c2` input parameter adds a second class to the button's
 * icon element (represented by the `i` selector) that will be applied for one second
 * before being removed.
 *
 * @param { string } removableClass - The `removableClass` input parameter is used
 * to specify a class name that should be removed from the button's "i" element
 * immediately after adding the `c1` and `c2` classes.
 *
 * @param { string } defaultClass - The `defaultClass` parameter is used to set the
 * class that will be added to the `i` element after the animation finishes (i.e.,
 * after 1 second).
 *
 * @returns { any } This function takes five arguments: `button`, `c1`, `c2`,
 * `removableClass`, and `defaultClass`. It selects an icon element within the button
 * using `querySelector` and adds two classes `c1` and `c2` to it.
 */
function flashButtonResult(button, c1, c2, removableClass, defaultClass) {
    let r = button.querySelector("i");
    r.classList.remove(removableClass);
    r.classList.add(c1, c2);
    setTimeout(function () {
        r.classList.remove(c1, c2);
        r.classList.add(defaultClass);
    }, 1000);
}

/**
* @description This function schedules a flight using a button click event. It sets
* the button as loading with a specified class name and retrieves the flight ID from
* the button's attribute. It then sends a JSON object to the server with the scheduled
* flight information and specifies two callback functions for success and failure.
* 
* @param {  } button - The `button` input parameter passed to the `scheduleFlight()`
* function is used as a reference to the HTML button element that triggered the
* function call.
* 
* @returns {  } The `scheduleFlight` function returns nothing (i.e., `undefined`)
* because it is a function that sets the button loading state and sends a request
* to the server with the button's flight ID.
*/
function scheduleFlight(button) {
    let loaderClass = setButtonLoading(button, "fe-star");
    let flightID = button.getAttribute("flight-id");

    const data = {
        msg: "schedule-flight",
        data: { flight_id: flightID },
    };

/**
* @description This function executes when a success condition is met and it has the
* following actions:
* 
* 1/ Flashes a button with a check mark icon.
* 2/ Reloads the current web page.
* 
* @returns { any } The output of the function `success` is:
* 
* 	- Flashing a button with a success icon (a check circle) and a green fill color.
* 	- Reloading the page.
*/
    function success() {
        flashButtonResult(button, "fe-check-circle", "fg-success", loaderClass, "fe-star");
        window.location.reload();
    }
/**
* @description This function displays a failing/error message to the user and then
* reloads the current web page.
* 
* @returns { any } This function takes no arguments and returns nothing (void),
* meaning it does not produce any output or return any values.
*/
    function failure() {
        flashButtonResult(button, "fe-x-circle", "fg-failure", loaderClass, "fe-star");
        window.location.reload();
    }
    sendToServer(data, success, failure);
}

/**
* @description This function clears a flight reservation. It sets a button to loading
* state while making a server request to clear the flight. If the request is successful
* (i.e., the server acknowledges the request), it updates the button's appearance
* with a success message and reloads the page.
* 
* @param {  } button - The `button` input parameter is passed as a reference to the
* HTML button element that triggered the function.
* 
* @returns { any } The output returned by this function is two flags (loading and
* error) and a string of the button's new class names.
* 
* Concisely:
* 
* 	- loading: false or "fe-star" if the flight was cleared successfully
* 	- error: false or "fe-x-circle" if there was an error while clearing the flight
* 	- classes: a space-separated string of new class names for the button ("fe-check-circle
* fg-success" or "fe-x-circle fg-failure")
*/
function clearFlight(button) {
    let loaderClass = setButtonLoading(button, "fe-star");
    let flightID = button.getAttribute("flight-id");

    const data = {
        msg: "clear-flight",
        data: { flight_id: flightID },
    };

/**
* @description This function calls the `flashButtonResult` function with various
* arguments to stylishly update the appearance of a button using Font Awesome icons
* and CSS classes.
* 
* @returns {  } The function `success()` returns no value or void.
*/
    function success() {
        flashButtonResult(button, "fe-check-circle", "fg-success", loaderClass, "fe-star");
        window.location.reload();
    }
/**
* @description This function calls `flashButtonResult` with various arguments to
* update the appearance of a button and then immediately reloads the current page
* (by calling `window.location.reload()`).
* 
* @returns {  } The function `failure` takes no arguments and has no return statement.
* Therefore it does not return any value or output.
*/
    function failure() {
        flashButtonResult(button, "fe-x-circle", "fg-failure", loaderClass, "fe-star");
        window.location.reload();
    }
    sendToServer(data, success, failure);
}
