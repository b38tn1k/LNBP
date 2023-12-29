let flightID = document.currentScript.getAttribute("data-flight-id");

document.getElementById("master-court-button").addEventListener("click", function() {
    alert("You have to implement this still!");
});

document.addEventListener("DOMContentLoaded", function () {
    var Draggable = FullCalendar.Draggable;
    var containerEl = document.getElementById("external-events");
    var calendarEl = document.getElementById("calendar");
    var calendarData = calendarEl.dataset.calendarData;

    new Draggable(containerEl, {
        itemSelector: ".fc-event",
/**
* @description This function retrieves information from event element attributes and 
* returns an object with three properties: title, backgroundColor, and textColor.
* 
* @param { object } eventEl - The `eventEl` input parameter is passed to the function 
* as an event element. It provides access to various properties of the event element, 
* such as its text content, background color, and other attributes.
* 
* @returns { object } - The `eventData` function takes an event element as input and 
* returns an object with three properties: `title`, `backgroundColor`, and `textColor`. 
* The values of these properties are extracted from the element's inner text, 
* `style.backgroundColor`, and `style.color`, respectively.
*/
        eventData: function (eventEl) {
            // console.log(eventEl.dataset.flightName, eventEl.dataset.startTime, eventEl.dataset.duration, eventEl.dataset.flightId);
            return {
                title: eventEl.innerText,
                backgroundColor: eventEl.style.backgroundColor,
                textColor: eventEl.style.color,
            };
        },
    });

    var events = [];
    if (calendarData) {
        events = JSON.parse(calendarData);
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        height: "auto",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        events: events,
        editable: true,
        droppable: true, // this allows things to be dropped onto the calendar
/**
* @description The `drop` function takes an `info` parameter and performs a specific 
* action with the input data. The exact purpose of the function cannot be determined 
* from the name alone.
* 
* @param { object } info - The `info` input parameter is passed to the function and 
* its purpose is unknown.
*/
        drop: function (info) {},

/**
* @description This function, `eventReceive`, handles when an event is dropped on 
* the calendar. It retrieves active courts, cancels the event if there are no courts 
* available, and updates the event's start and end times based on the duration and 
* start time provided in the dropped event's metadata.
* 
* @param { object } info - The `info` input parameter is an object that provides 
* information about the dragged element and the event being created. It contains 
* properties such as `draggedEl`, `event`, `start`, and `end`.
*/
        eventReceive: function (info) {
            var courts = getActiveCourts();
            if (courts.length == 0) {
                // cancel this and delete the newly created event
                info.event.remove();
                if (courts.length == 0) {
                    // Cancel this and delete the newly created event
                    info.event.remove();
                    var my_toast = new bootstrap.Toast(document.getElementById("my-toast"));
                    my_toast.show();
                }
            } else {
                var title = info.draggedEl.dataset.flightName;
                var duration = info.draggedEl.dataset.duration;
                var startTime = info.draggedEl.dataset.startTime;
                var flightId = info.draggedEl.dataset.flightId;
                var start = info.event.start;
                var end = info.event.end;

                var startTimeParts = startTime.split(":");
                var startHour = parseInt(startTimeParts[0]);
                var startMinutes = parseInt(startTimeParts[1]);

                var durationTimeParts = duration.split(":");
                var durationHour = parseInt(durationTimeParts[0]);
                var durationMinutes = parseInt(durationTimeParts[1]);

                // Create a new Date object from the start time
                var end = new Date(start.getTime());
                // Add the duration to the end time
                start.setHours(startHour, startMinutes);
                end.setHours(end.getHours() + durationHour);
                end.setMinutes(end.getMinutes() + durationMinutes);
                info.event.setExtendedProp("setup", false);
                info.event.setExtendedProp("courts", courts);
                info.event.setEnd(end);
                info.event.setAllDay(false);
                info.event.setProp("title", title);
                info.event.setProp("display", "block");
                info.event.setStart(start);
                info.event.setEnd(end);
                info.event.setExtendedProp("setup", true);
            }
        },

/**
* @description The eventClick function highlights the timeslot and courts associated 
* with the given event id.
* 
* @param { object } info - The `info` input parameter provides event details, including 
* the ID of the event and a list of court IDs.
*/
        eventClick: function (info) {
            highlightTimeslotById(info.event.id)
            highlightCourtsByID(info.event.extendedProps.courts);
        },

/**
* @description This function handles an event change for a flight, specifically a 
* new or updated timeslot. It extracts information from the event object and sends 
* a POST request to the API with the new or updated data.
* 
* @param { object } info - The `info` input parameter in the `eventChange` function 
* contains information about the event that triggered the function call. It has 
* properties such as `event`, `id`, `title`, `start`, `end`, `courts`, and 
* `extendedProps`. These properties contain information about the specific event 
* that the function is being called for, such as the event ID, title, start and end 
* dates/times, and court information.
*/
        eventChange: function (info) {
            var doUpdate = info.event.extendedProps["setup"];
            var id = info.event.id;
            console.log(doUpdate);
            if (doUpdate || id) {
                var title = info.event.title; // get the title of the event
                var start = info.event.start.toISOString(); // get the start date/time of the event
                var end = info.event.end.toISOString(); // get the end date/time of the event
                var courts = info.event.extendedProps["courts"];
                var timeZoneOffsetMinutes = new Date().getTimezoneOffset();

                var data = {
                    start: start,
                    end: end,
                    courts: courts,
                    timeZoneOffset: timeZoneOffsetMinutes,
                };

                var url, method;
                if (id) {
                    url = "/flights/" + flightID + "/timeslots/" + id + "/edit";
                    method = "POST";
                    data["id"] = id;
                } else {
                    url = "/flights/" + flightID + "/timeslots/new";
                    method = "POST";
                }

                fetch(url, {
                    method: method,
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log("Success:", data);
                        if (!id) {
                            info.event.setProp("id", data.timeslot_id);
                            // Create a new delete button for the newly added timeslot
                            addTimeSlotToManager(info);
                        }
                    })
                    .catch((error) => {
                        console.error("Error:", error);
                    });
            }
        },

/**
* @description This function adds a time slot to a manager.
* 
* @param { object } event - The `event` input parameter in the `eventDidMount` 
* function is passed to the function when the event occurs.
* 
* @param element - The `element` input parameter in the `eventDidMount` function is 
* used to provide the EventTarget object that triggered the event.
*/
        eventDidMount: function (event, element) {
            addTimeSlotToManager(event);
        },
    });

    calendar.render();
    window.calendar = calendar;
});

/**
* @description This function highlights a specific Timeslot element on a page by 
* identifying it using its "data-timeslot-id" attribute, then adding or removing the 
* "highlighted" class to highlight or un-highlight that Timeslot element based on 
* the id passed as a parameter.
* 
* @param { string } id - The `id` input parameter in the `highlightTimeslotById` 
* function is used to specify the unique identifier of the desired timeslot element 
* that needs to be highlighted.
*/
function highlightTimeslotById(id) {
    const timeslotElements = document.querySelectorAll(`div[data-timeslot-id]`);
    timeslotElements.forEach((timeslotElement) => {
        if (timeslotElement.getAttribute("data-timeslot-id") === id) {
            timeslotElement.classList.add("highlighted");
        } else {
            timeslotElement.classList.remove("highlighted");
        }
    });
}

/**
* @description This function highlights rows containing courts with the given IDs, 
* adding "highlighted" class if the court ID is present in the given array, otherwise 
* removing it.
* 
* @param { array } courts - The `courts` input parameter is an array of integers 
* that determines which court rows are highlighted in the DOM. The function iterates 
* through each row, calculates its ID as an integer, and checks if the ID is included 
* in the `courts` array.
*/
function highlightCourtsByID(courts) {
    const courtRows = document.querySelectorAll("#court-selector-toggle tbody tr");
    courtRows.forEach((row) => {
        const courtId = parseInt(row.id);
        if (courts.includes(courtId)) {
            row.classList.add("highlighted");
        } else {
            row.classList.remove("highlighted");
        }
    });
}

/**
* @description This function adds a new timeslot element to the Timeslot Manager 
* component, updates the text of the element with a human-readable date based on the 
* event start time, and creates a delete button that will call the `deleteTimeslot()` 
* function when clicked.
* 
* @param { object } info - The `info` input parameter in the `addTimeSlotToManager` 
* function contains information about an event to be added to the time slot manager.
*/
function addTimeSlotToManager(info) {
    if (info.event.id) {
        const existingTimeslotElement = document.querySelector(`div[data-timeslot-id="${info.event.id}"]`);
        if (existingTimeslotElement) {
            existingTimeslotElement.remove();
        }
        // Create a new timeslot element if it doesn't exist
        const deleteButton = document.createElement("button");
        deleteButton.innerText = "Delete";
        deleteButton.addEventListener("click", function () {
            deleteTimeslot(flightID, info.event.id, function () {
                const timeslotElement = document.querySelector(`div[data-timeslot-id="${info.event.id}"]`);
                if (timeslotElement) {
                    timeslotElement.remove();
                }
            });
        });
        const timeslotManager = document.getElementById("timeslot-manager");
        const timeslotElement = document.createElement("div");
        timeslotElement.setAttribute("data-timeslot-id", info.event.id);
        timeslotElement.setAttribute("class", "timeslot-mgmt");
        timeslotElement.innerText = getHumanReadableDate(info.event.start);
        timeslotElement.appendChild(deleteButton);
        timeslotManager.appendChild(timeslotElement);
    }
}

/**
* @description This function takes an ISO date string and returns a human-readable 
* date in the format "ddd MMM D, YYYY HH:MM".
* 
* @param { string } isoDate - The `isoDate` input parameter provides a string 
* representation of a Date object in ISO format, such as "2023-02-13T14:30:00.000Z".
* 
* @returns { string } - The `getHumanReadableDate` function takes an ISO date string 
* as input and returns a human-readable date in the format "day MM/dd/yyyy hh:mm".
*/
function getHumanReadableDate(isoDate) {
    const date = new Date(isoDate);

    // Get day, month, date, and year in '23 style
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    const day = days[date.getDay()];
    const month = months[date.getMonth()];
    const dateNumber = date.getDate();
    const year = date.getFullYear().toString().slice(-2);

    // Get time hours and minutes
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");

    // Combine the components into the desired format
    const humanReadableDate = `${day} ${month} ${dateNumber} ${year} ${hours}:${minutes}`;

    return humanReadableDate;
}

/**
* @description The function addTimeslot creates a new event div with the specified 
* background color, text color, and duration, and appends it to an external events 
* container.
* 
* @param { string } fg - The `fg` input parameter specifies the background color of 
* the new event div.
* 
* @param { string } bg - The `bg` input parameter sets the background color of the 
* newly created event div.
* 
* @param { string } id - The `id` input parameter in the `addTimeslot()` function 
* is used to set the `dataset.flightId` property of the new event div element.
* 
* @param { string } name - The `name` input parameter is used to set the name of the 
* flight for the newly created event.
*/
function addTimeslot(fg, bg, id, name) {
    // Get the input values
    let time = document.getElementById("time-input").value;
    let hours = document.getElementById("hour-spinner").value;
    let minutes = document.getElementById("minute-spinner").value;
    let duration = String(hours).padStart(2, "0") + ":" + String(minutes).padStart(2, "0");
    // Create the new event div
    let newEventDiv = document.createElement("div");
    newEventDiv.className = "fc-event fc-h-event fc-daygrid-event fc-daygrid-block-event";
    newEventDiv.innerHTML = '<div class="fc-event-main">&nbsp;' + time + " - " + duration + " hr" + "</div>";
    newEventDiv.style.backgroundColor = bg;
    newEventDiv.style.color = fg;
    newEventDiv.children[0].style.color = fg;
    newEventDiv.dataset.startTime = time;
    newEventDiv.dataset.duration = duration;
    newEventDiv.dataset.flightId = id;
    newEventDiv.dataset.flightName = name;
    // Add the new event div to the external events container
    document.getElementById("external-events-internal").appendChild(newEventDiv);
}

$("#hour-spinner").spinner({
    min: 0,
    max: 23,
/**
* @description This function spin updates the value of a widget with a new value, 
* taking into account whether the input value is less than or equal to 10.
* 
* @param event - The `event` input parameter is passed to the function spin when a 
* spin box value changes due to user input.
* 
* @param { object } ui - The `ui` input parameter in the provided function is an 
* object that contains information about the currently triggered event.
*/
    spin: function (event, ui) {
        $(this).val(ui.value < 10 ? "0" + ui.value : ui.value);
    },
});

$("#minute-spinner").spinner({
    min: 0,
    max: 59,
/**
* @description The spin function takes in an event and ui parameters and updates the 
* value of a element with id specified by 'this' to have a formatted value based on 
* whether the current ui value is less than or equal to 10.
* 
* @param { object } event - The `event` input parameter is not used in the provided 
* `spin` function.
* 
* @param { object } ui - The `ui` input parameter contains information about the 
* user's input, including the value and other relevant details.
*/
    spin: function (event, ui) {
        $(this).val(ui.value < 10 ? "0" + ui.value : ui.value);
    },
});

/**
* @description The function getActiveCourts() collects the IDS of active courts based 
* on checkboxes' states, and it returns an array of these IDs.
* 
* @returns { array } - The output returned by the `getActiveCourts()` function is 
* an array of integer IDs of the checked checkboxes.
*/
function getActiveCourts() {
    // Array to hold the IDs of the active courts
    var activeCourts = [];

    // Get all the checkboxes
    var checkboxes = document.querySelectorAll("#court-selector-toggle .form-check-input");

    // Loop through all checkboxes
    for (var i = 0; i < checkboxes.length; i++) {
        // If the checkbox is checked
        if (checkboxes[i].checked) {
            // Add the ID to the activeCourts array
            activeCourts.push(parseInt(checkboxes[i].id.replace("court-switch-", "")));
        }
    }

    // Return the activeCourts array
    return activeCourts;
}

/**
* @description This function deletes a timeslot with the given ID from the database 
* and removes the corresponding element from the HTML page, as well as any associated 
* events in the calendar.
* 
* @param { object } flightId - The `flightId` input parameter in the `deleteTimeslot` 
* function is used to identify the flight that contains the timeslot being deleted.
* 
* @param { string } timeslotId - The `timeslotId` input parameter in the `deleteTimeslot` 
* function is passed as a route parameter to delete a specific timeslot.
* 
* @param callback - The `callback` input parameter is a function that is called after 
* the asynchronous request to delete the timeslot has been processed.
*/
function deleteTimeslot(flightId, timeslotId, callback) {
    fetch(`/flights/${flightId}/timeslots/${timeslotId}/delete`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            // If the deletion was successful, remove the timeslot from the HTML
            const timeslotElement = document.querySelector(`[data-timeslot-id="${timeslotId}"]`);
            if (timeslotElement) {
                timeslotElement.remove();
            }
            if (window.calendar && data.status === "success") {
                const event = window.calendar.getEventById(timeslotId);
                if (event) {
                    event.remove();
                }
            }
            // Call the callback function if provided
            if (typeof callback === "function") {
                callback();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
