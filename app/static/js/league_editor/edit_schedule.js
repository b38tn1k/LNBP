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
    const existingDiffIndex = delta.findIndex((diff) =>
        diff.event === data.event &&
        JSON.stringify(diff.ids) === JSON.stringify(data.ids)
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
    if (typeof diff.ids === 'object') {
        idsString = Object.entries(diff.ids).map(([key, value]) => `${key}:${value}`).join(', ');
    }

    // If values is an object, convert it to a string representation of key-value pairs
    if (typeof diff.values === 'object') {
        valuesString = Object.entries(diff.values).map(([key, value]) => `${key}:${value}`).join(', ');
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
    const month = String(dateTime.getMonth() + 1).padStart(2, '0'); // Month is 0-based
    const day = String(dateTime.getDate()).padStart(2, '0');
    const hours = String(dateTime.getHours()).padStart(2, '0');
    const minutes = String(dateTime.getMinutes()).padStart(2, '0');
    const seconds = '00'
    const milliseconds = '000'
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}`;
}

document.addEventListener("DOMContentLoaded", function () {
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
                updateDelta(
                    new Diff('timeslot_update', parseInt(date.getAttribute("ts")), formatLocalDateTime(newDate))
                )
            },
        });
    }

    document
        .querySelectorAll(".schedule-table")
        .forEach((table) => table.addEventListener("click", handleFlightTableClick));
});

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

        const ids = {'timeslot' : parseInt(target.getAttribute('timeslot')), 'player' : parseInt(target.getAttribute('player'))}

        updateDelta(
            new Diff('availability_update', ids , availability)
        )

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
