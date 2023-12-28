class Diff {
    constructor(event, ids, values) {
        this.event = event;
        this.ids = ids;
        this.values = values;
    }
}

const delta = [];

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
