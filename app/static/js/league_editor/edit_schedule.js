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
    const dates = document.querySelectorAll(".fp_dates");
    for (let date of dates) {
        dateString = date.getAttribute("startTime");
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

    document
        .querySelectorAll(".schedule-table")
        .forEach((table) => table.addEventListener("click", handleFlightTableClick));

    document.querySelectorAll(".reveal-after").forEach((div) => (div.style.display = "block"));
});

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
    updateDelta(new Diff("remove_player_from_league", {'player': playerID}, 0));
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
    updateDelta(new Diff("change_flight", {'player': playerID}, {'new_flight': flightID}));

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
