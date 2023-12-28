const dates = document.querySelectorAll(".fp_dates");
for (let date of dates) {
    dateString = date.getAttribute("startTime");
    flatpickr(date, {
        defaultDate: new Date(date.getAttribute("startTime")),
        enableTime: true,
        dateFormat: "m/d H:i",
/**
* @description The `onChange` function is called whenever the selected dates or time
* change.
* 
* @param { array } selectedDates - The `selectedDates` input parameter is an array
* of dates that the user has selected from the dropdown menu.
* 
* @param { string } dateStr - The `dateStr` input parameter is a string representing
* the selected date and time.
*/
        onChange: function (selectedDates, dateStr) {
            // Update the th content with the selected date and time
            date.innerHTML = dateStr;
        },
    });
}

document.querySelectorAll('.schedule-table').forEach(table => table.addEventListener("click", handleFlightTableClick));

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
