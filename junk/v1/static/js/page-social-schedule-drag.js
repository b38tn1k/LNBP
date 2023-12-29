const PLAYER_MULTIPLE = 4;
const LEAGUE_RULE_MIN_GAMES = 4;
var events_from_server = [];
const AVAILABLE = 1;
const AVAILABLE_LP = 2;
const UNAVAILABLE = 3;
const UNK = -1;
var is_dragging = false;

document.addEventListener("DOMContentLoaded", function () {
    initialize();
    setupLayout();
    doDragula();
});

/**
 * @description The function `initialize` retrieves events from the server and sets
 * up event listeners, updates the player count, and sets up radios.
 */
function initialize() {
    getEvents(flightID).then((events) => {
        if (events) {
            events_from_server = events;
        } else {
            events_from_server = [];
        }
        setupEvents();
        updatePlayerCount();
        setupRadios();
        setTimeout(() => {
            resetCellColors();
        }, 200);
    });
}

/**
 * @description This function sets up event listeners for radio buttons with the name
 * "player-is-captain-input" and updates the captain of a court when a new captain
 * is selected.
 */
function setupRadios() {
    // Get all radio buttons with the name "player-is-captain-input"
    var radioButtons = document.querySelectorAll('input[type="radio"][class="player-is-captain-input"]');
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener("change", () => {
            var nearestDraggableTarget = radioButton.closest(".draggable-target");
            if (nearestDraggableTarget) {
                newCaptain = radioButton.getAttribute("data-player-id");
                courtId = nearestDraggableTarget.getAttribute("data-court-id");
                timeId = nearestDraggableTarget.getAttribute("data-time-id");
                // Send data to the server using fetch API
                fetch(`/timeslot/${timeId}/events/updateCaptain`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        // Add other headers if required. For example, if you have CSRF tokens.
                    },
                    body: JSON.stringify({
                        court: courtId,
                        captain: newCaptain, // Assuming you also want to send the captain's ID
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.status === "success") {
                            console.log("Successfully updated captain.");
                            nearestDraggableTarget.setAttribute("data-captain-id", newCaptain);
                            updatePlayerCount();
                        } else {
                            console.error("Error updating captain.");
                        }
                    })
                    .catch((error) => {
                        console.error("There was an error:", error);
                    });
            }

            updatePlayerCount();
        });
    });
}

/**
 * @description The function doDragula initializes a dragula instance with specified
 * options, and registers event listeners for drag, drop, and dragend events.
 */
function doDragula() {
    var drake = dragula({
        isContainer: isDraggableTarget,
        moves: isDraggableItem,
        copy: isDraggableSource,
        accepts: canAcceptDrop,
    });

    drake.on("drag", handleDrag);
    drake.on("drop", handleDrop);
    drake.on("dragend", handleDragEnd);
    drake.on("cancel", handleDragCancel);
}

/**
* @description This function resets the `is_dragging` flag to `false` and calls the 
* `resetCellColors` function.
*/
function handleDragCancel() {
    is_dragging = false;
    resetCellColors();
}

/**
 * @description This function updates the player count and sets up radios when a drag
 * event ends.
 */
function handleDragEnd() {
    is_dragging = false;
    updatePlayerCount();
    setupRadios();
}

/**
 * @description The function "isDraggableTarget" checks if an element has the class
 * "draggable-target".
 *
 * @param el - The `el` input parameter is passed as an element to be checked for draggability.
 *
 * @returns { boolean } - The output returned by the function isDraggableTarget(el)
 * is a boolean value indicating whether the element el has the class "draggable-target".
 */
function isDraggableTarget(el) {
    return el.classList.contains("draggable-target");
}

/**
 * @description The function isDraggableItem(el, source, handle, sibling) checks if
 * the element el has a classList containing "draggable-item".
 *
 * @param el - The `el` input parameter is passed as an element to be checked for draggability.
 *
 * @param source - The `source` input parameter in the `isDraggableItem` function
 * identifies the element from which the dragging operation originated.
 *
 * @param handle - The `handle` input parameter in the `isDraggableItem` function is
 * used to specify the element that is being dragged.
 *
 * @param sibling - The `sibling` input parameter in the `isDraggableItem` function
 * is used to specify the element that the draggable item should be moved in relation
 * to.
 *
 * @returns { boolean } - The output returned by this function is a boolean value
 * indicating whether the provided element is a draggable item or not, based on the
 * presence of the "draggable-item" class.
 */
function isDraggableItem(el, source, handle, sibling) {
    return el.classList.contains("draggable-item");
}

/**
 * @description The function isDraggableSource(el, source) checks if the provided
 * element (el) is within a closest draggable source element (source) and returns a
 * boolean value indicating whether the element is within such an element.
 *
 * @param el - The `el` input parameter in the `isDraggableSource` function is passed
 * as an element to be checked for draggability.
 *
 * @param source - The `source` input parameter in the `isDraggableSource` function
 * is used to determine if the element being checked is a draggable source.
 *
 * @returns { boolean } - The output returned by this function is a boolean value
 * indicating whether the specified element is draggable or not.
 */
function isDraggableSource(el, source) {
    return source.closest(".draggable-source") !== null;
}

/**
 * @description The function accepts a drop event on an element and returns a boolean
 * value indicating whether the drop is allowed on a target element.
 *
 * @param el - The `el` input parameter is passed as an element to be checked for
 * acceptance of a drop.
 *
 * @param target - The `target` input parameter in the `canAcceptDrop` function is
 * used to determine whether the element can accept the drop.
 *
 * @returns { boolean } - The output returned by the function is "true".
 */
function canAcceptDrop(el, target) {
    return true;
}

/**
 * @description The function handleDrag highlights availability data for a specific
 * player based on the player's ID.
 *
 * @param el - The `el` input parameter in the `handleDrag` function is used to
 * reference the dragged element.
 *
 * @param source - The `source` input parameter in the `handleDrag` function is used
 * to determine the type of drag event that occurred.
 */
function handleDrag(el, source) {
    is_dragging = true;
    var playerId = el.getAttribute("data-player-id");
    var playerAvailData = playerAvailability[playerId];
    highlightAvailability(playerAvailData, playerId);
    clearDraggableOrigins();
}

/**
 * @description The function handleDrop(el, target, source, sibling) handles draggable
 * elements being dropped onto a target element. It checks the availability of the
 * target element and removes the draggable source element if it is not available.
 *
 * @param el - The `el` input parameter in the `handleDrop` function is the draggable
 * element being dropped.
 *
 * @param target - The `target` input parameter in the `handleDrop` function specifies
 * the element upon which the dragged element is being dropped.
 *
 * @param source - The `source` input parameter in the `handleDrop` function represents
 * the element that is being dragged.
 *
 * @param sibling - The `sibling` input parameter in the `handleDrop` function is
 * used to specify the element that the dragged element should be dropped next to.
 */
function handleDrop(el, target, source, sibling) {
    is_dragging = false;
    if (target && target != source) {
        handleDraggableDrop(el, target, source);
        checkCells();
        if (target.getAttribute("data-availability") === "3") {
            removeDraggable(el, source);
        }
    }
    resetCellColors();
}

/**
 * @description The function removes draggable elements from the source if they have
 * been dropped within the source.
 *
 * @param el - The `el` input parameter is passed as the element to be checked for draggability.
 *
 * @param target - The `target` input parameter in the `removeDraggableFromSourceIfDroppedInSource`
 * function is used to specify the element that was dropped.
 *
 * @param source - The `source` input parameter in the `removeDraggableFromSourceIfDroppedInSource`
 * function is used to specify the draggable element that should be removed from the
 * source element if it has been dropped back into the source element.
 */
function removeDraggableFromSourceIfDroppedInSource(el, target, source) {
    if (target.closest(".draggable-source") !== null) {
        removeDraggable(el, source);
    }
}

/**
 * @description The function removes a draggable element from its source if it has a
 * similar draggable element already present in the target element.
 *
 * @param el - The `el` input parameter in the `removeDuplicateDraggableFromTarget`
 * function is the element to be processed.
 *
 * @param target - The `target` input parameter in the `removeDuplicateDraggableFromTarget`
 * function is a reference to the target element where the draggable items are being
 * appended.
 *
 * @param { object } source - The `source` input parameter in the
 * `removeDuplicateDraggableFromTarget` function is the element that is being dragged.
 */
function removeDuplicateDraggableFromTarget(el, target, source) {
    var playerName = el.getAttribute("data-player-name");
    var similarItems = target.querySelectorAll(`.draggable-item[data-player-name="${playerName}"]`);
    if (similarItems.length > 1) {
        removeDraggable(el, source);
    }
}

/**
 * @description The function removeExcessDraggableFromTarget removes draggable items
 * from the target element if there are more than the specified multiple of draggable
 * items present.
 *
 * @param el - The `el` input parameter in the `removeExcessDraggableFromTarget`
 * function is the element to be checked for excess draggables.
 *
 * @param target - The `target` input parameter in the `removeExcessDraggableFromTarget`
 * function is used to specify the element to which the draggable items should be removed.
 *
 * @param source - The `source` input parameter in the `removeExcessDraggableFromTarget`
 * function is used to specify the element from which the draggable items should be
 * removed.
 *
 * @param { integer } multiple - The `multiple` input parameter in the
 * `removeExcessDraggableFromTarget` function determines the number of draggable items
 * that should be removed from the target element when the excess items are detected.
 */
function removeExcessDraggableFromTarget(el, target, source, multiple) {
    var itemCount = target.querySelectorAll(".draggable-item").length;
    if (itemCount == multiple + 1) {
        removeDraggable(el, source);
    }
}

/**
 * @description The function handleEventCreation(el, target, source, multiple) creates
 * a new event on the server when multiple draggable items are dropped on a target element.
 *
 * @param el - The `el` input parameter in the `handleEventCreation` function is the
 * ELEMENT that the event was triggered on.
 *
 * @param target - The `target` input parameter in the `handleEventCreation` function
 * is a reference to the element that triggered the event.
 *
 * @param source - The `source` input parameter in the `handleEventCreation` function
 * is the element that triggered the event.
 *
 * @param { integer } multiple - The `multiple` input parameter in the `handleEventCreation`
 * function determines the number of draggable items that can be selected at once.
 */
function handleEventCreation(el, target, source, multiple) {
    var itemCount = target.querySelectorAll(".draggable-item").length;
    if (itemCount == multiple) {
        let data = getPlayersCourtTimeSlotID(target);
        let url = "/timeslot/" + data.timeslot + "/events/new";
        sendDataToServer(url, data);
    }
}

/**
 * @description This function handles event deletion.
 *
 * @param el - The `el` input parameter in the `handleEventDeletion` function is the
 * element that triggered the event.
 *
 * @param target - The `target` input parameter in the `handleEventDeletion` function
 * is the element that the event was triggered on.
 *
 * @param source - The `source` input parameter in the `handleEventDeletion` function
 * is a DOM element that represents the source of the event being deleted.
 *
 * @param multiple - The `multiple` input parameter specifies the number of items
 * that can be deleted at once.
 */
function handleEventDeletion(el, target, source, multiple) {
    var sourceItemCount = source.querySelectorAll(".draggable-item").length;
    if (sourceItemCount == multiple - 1) {
        let data = getPlayersCourtTimeSlotID(source);
        let url = "/timeslot/" + data.timeslot + "/events/delete";
        sendDataToServer(url, data);
    }
}

/**
 * @description The function sendDataToServer sends a POST request to the specified
 * URL with the given data.
 *
 * @param { string } url - The `url` input parameter specifies the URL of the server
 * to which the data should be sent.
 *
 * @param data - The `data` input parameter is the data that is sent to the server.
 */
function sendDataToServer(url, data) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

/**
 * @description The function handleDraggableDrop manages the dropping of draggable
 * elements. It removes draggables from their original source if dropped back, removes
 * duplicate draggables from the target, and removes excess draggables from the target.
 *
 * @param el - The `el` input parameter is the draggable element being dropped.
 *
 * @param target - The `target` input parameter in the `handleDraggableDrop` function
 * is the element that the draggable element is being dropped onto.
 *
 * @param { array } source - The `source` input parameter is used to specify the
 * container element from which the draggable element is being dragged.
 */
function handleDraggableDrop(el, target, source) {
    removeDraggableFromSourceIfDroppedInSource(el, target, source);
    removeDuplicateDraggableFromTarget(el, target, source);
    removeExcessDraggableFromTarget(el, target, source, PLAYER_MULTIPLE);
    handleEventCreation(el, target, source, PLAYER_MULTIPLE);
    handleEventDeletion(el, target, source, PLAYER_MULTIPLE);
}

/**
 * @description The function getPlayersCourtTimeSlotID(location) extracts information
 * about a court and its associated players' time slots from a HTML element location,
 * and returns an object with the court ID, time ID, and an array of player IDs.
 *
 * @param location - The `location` input parameter in the `getPlayersCourtTimeSlotID`
 * function is a DOM element that contains information about the court and time slot
 * being queried.
 *
 * @returns { object } - The output returned by the `getPlayersCourtTimeSlotID`
 * function is an object with three properties: `court`, `timeslot`, and `players`.
 */
function getPlayersCourtTimeSlotID(location) {
    var courtId = location.getAttribute("data-court-id");
    var timeId = location.getAttribute("data-time-id");

    var playerIds = [];

    var playerElements = location.querySelectorAll(".draggable-item");
    playerElements.forEach(function (playerElement) {
        var playerId = playerElement.getAttribute("data-player-id");
        playerIds.push(playerId);
    });

    var result = {
        court: courtId,
        timeslot: timeId,
        players: playerIds,
    };

    return result;
}

/**
 * @description The function removeDraggable(el, source) removes the element el from
 * the page.
 *
 * @param el - The `el` input parameter in the `removeDraggable` function serves as
 * the target element to be removed.
 *
 * @param source - The `source` input parameter in the `removeDraggable` function is
 * used to specify the element from which the draggable behavior should be removed.
 */
function removeDraggable(el, source) {
    el.remove();
}

/**
 * @description The function checkCells() counts the number of draggable items in
 * each draggable target cell in the schedule and sets the background color of the
 * cell to lightcoral if the item count is not a multiple of PLAYER_MULTIPLE.
 */
function checkCells() {
    // count draggable-items in each draggable-target cell in the schedule
    var scheduleCells = document.querySelectorAll("#schedule .draggable-target");
    scheduleCells.forEach(function (cell) {
        var itemCount = cell.querySelectorAll(".draggable-item").length;
        if (itemCount % PLAYER_MULTIPLE !== 0) {
            cell.style.backgroundColor = "lightcoral";
        } else {
            // reset the background color when the condition is not met
            cell.style.backgroundColor = "";
        }
    });
}

/**
 * @description This function sets up the layout of a schedule by assigning background
 * colors and text to cells in a table based on the availability of each cell.
 *
 * @returns { array } - The `setupLayout` function returns no output, but instead
 * modifies the styles and content of DOM elements. It sets the background color of
 * cells in a schedule based on their availability and whether they are reserved by
 * another flight.
 */
function setupLayout() {
    var items = document.querySelectorAll(".draggable-source .draggable-item");
    var hueStep = 360 / items.length;
    var startHue = Math.floor(Math.random() * 360); // Random starting point

    items.forEach(function (item, index) {
        var hue = (startHue + hueStep * index) % 360;
        item.style.backgroundColor = `hsl(${hue}, 100%, 80%)`;
    });

    // Check availability of each cell in the schedule
    var cells = document.querySelectorAll("#schedule td");
    cells.forEach(function (cell) {
        var court_id = cell.getAttribute("data-court-id");
        var time_id = cell.getAttribute("data-time-id");
        var eventExists = other_court_events.some(function (event) {
            return event.court_id == court_id && event.timeslot_id == time_id;
        });

        if (eventExists) {
            var event = other_court_events.find(function (event) {
                return event.court_id == court_id && event.timeslot_id == time_id;
            });
            cell.style.backgroundColor = "#ccc";
            cell.classList.remove("draggable-target");
            cell.classList.add("reserved-by-other-flight");
            cell.innerHTML = event.flight_name;
        }

        var available = cell.getAttribute("data-court-available");
        if (available === "False") {
            cell.style.backgroundColor = "#666";
            cell.classList.remove("draggable-target");
        }
    });
}

// Function to update player game count
/**
 * @description This function updates the game count for a specific player by counting
 * the number of draggable items with the same name as the player, and then displaying
 * the count in a span element using textContent.
 *
 * @param player - The `player` input parameter in the `updatePlayerGameCount` function
 * is passed a DOM element representing a player.
 *
 * @param scheduleDiv - The `scheduleDiv` input parameter in the `updatePlayerGameCount`
 * function is used to select the element representing the player's schedule in the
 * HTML document.
 */
function updatePlayerGameCount(player, scheduleDiv) {
    var playerName = player.getAttribute("data-player-name");
    var playerCount = scheduleDiv.querySelectorAll(`.draggable-item[data-player-name="${playerName}"]`).length;
    var origin = player.closest(".draggable-origin");
    if (origin) {
        var countSpan = origin.querySelector(".player-game-count");
        countSpan.textContent = playerCount;
        var gameCountImage = origin.querySelector(".racket-warning");
        if (playerCount < LEAGUE_RULE_MIN_GAMES) {
            gameCountImage.src = tennis_racket_warning_svg;
        } else {
            gameCountImage.src = tennis_racket_svg;
        }
    } else {
        console.warn(`Could not find count span for player: ${playerName}`);
    }
}

// Function to update player captain count
// Function to update player captain count
/**
 * @description The function updatePlayerCaptainCount updates the text content of the
 * captain count span and switches the image source of the captain switch based on
 * the number of checked radio buttons with the same player name.
 *
 * @param player - The `player` input parameter in the `updatePlayerCaptainCount`
 * function is used to retrieve the player's name and other information.
 *
 * @param scheduleDiv - The `scheduleDiv` input parameter in the `updatePlayerCaptainCount`
 * function is used to select the element that contains the captain count span to be
 * updated.
 */
function updatePlayerCaptainCount(player, scheduleDiv) {
    var playerName = player.getAttribute("data-player-name");
    var captainCount = scheduleDiv.querySelectorAll(
        `.draggable-item[data-player-name="${playerName}"] input[type="radio"][name*="player-is-captain-input"]:checked`
    ).length;
    var origin = player.closest(".draggable-origin");
    if (origin) {
        // console.log(`Found span for player: ${playerName}`);
        var captainCountSpan = origin.querySelector(".player-captain-count");
        captainCountSpan.textContent = captainCount;

        var captainImage = origin.querySelector(".captain-switch");
        if (captainCount > 0) {
            captainImage.src = captain_checked_svg;
        } else {
            captainImage.src = captain_unchecked_svg;
        }
    } else {
        console.warn(`Could not find captain count span for player: ${playerName}`);
    }
}

/**
 * @description The function `updatePlayerScheduleCount` updates the availability
 * count for a given player's schedule. It iterates through the player's availability
 * data, adds unique timeslot IDs to a set, and updates an object with the availability
 * count for each timeslot.
 *
 * @param { any } player - The `player` input parameter in the `updatePlayerScheduleCount`
 * function is a DOM element representing the player being updated.
 *
 * @param scheduleDiv - ! Here's the answer directly:
 *
 * The `scheduleDiv` input parameter in the `updatePlayerScheduleCount` function is
 * a reference to a HTML div element that contains the schedule for the player.
 */
function updatePlayerScheduleCount(player, scheduleDiv) {
    var playerId = player.getAttribute("data-player-id");
    var playerName = player.getAttribute("data-player-name");
    var playerAvailData = playerAvailability[playerId];
    if (playerAvailData) {
        var cells = scheduleDiv.querySelectorAll(`.draggable-item[data-player-name="${playerName}"]`);
        // Create a set to store unique timeslotIds
        var uniqueTimeslotIds = new Set();

        cells.forEach(function (cell) {
            // Get the closest parent 'draggable-target' for each cell
            var parentTarget = cell.closest(".draggable-target");
            if (parentTarget) {
                var timeslotId = parentTarget.getAttribute("data-time-id");
                // Add the timeslotId to the set
                uniqueTimeslotIds.add(String(timeslotId));
            }
        });
        // Initialize a dictionary to store availability count
        var availabilityCount = {
            1: 0,
            2: 0,
            3: 0,
        };
        just_the_score = 0;
        // Loop through playerAvailData and update the availabilityCount for the unique timeslots
        playerAvailData.forEach(function (data) {
            if (data.availability == AVAILABLE_LP) {
                just_the_score += 1;
            }
            let tsid = String(data.timeSlotId);
            if (uniqueTimeslotIds.has(tsid)) {
                availabilityCount[data.availability]++;
            }
        });
        // console.log(availabilityCount)
        var origin = player.closest(".draggable-origin");
        if (origin) {
            // console.log(`Found span for player: ${playerName}`);
            var countSpan = origin.querySelector(".player-badtimeslot-count");
            countSpan.textContent = availabilityCount[2] + "/" + just_the_score;

            var image = origin.querySelector(".low-preference-time-counter");
            if (availabilityCount[2] > 0) {
                image.src = timeslot_check_warning_svg;
            } else {
                image.src = timeslot_check_svg;
            }
        } else {
            console.warn(`Could not find span for player: ${playerName}`);
        }
    }
}

/**
 * @description This function updates a table view with the availability of players
 * for each time slot. It retrieves the player ID and target table, then iterates
 * through the cells in the table and sets their inner HTML based on the availability
 * of the player for each time slot.
 *
 * @param { object } player - The `player` input parameter in the `updateTableView`
 * function is used to retrieve the player's availability data and rearrange the table
 * cells accordingly.
 *
 * @param scheduleDiv - The `scheduleDiv` input parameter in the `updateTableView`
 * function is a reference to a DOM element that contains the schedule for the players.
 * The function updates the table view based on the availability of the players and
 * the schedule.
 */
function updateTableView(player, scheduleDiv) {
    var playerId = player.getAttribute("data-player-id");
    var targetTable = document.getElementById("os-schedule-table");
    var cells = targetTable.querySelectorAll(`td[data-player-id="${playerId}"]`);
    var playerAvailData = playerAvailability[playerId];
    var rearrangeAvailData = {};
    for (let a in playerAvailData) {
        rearrangeAvailData[playerAvailData[a]["timeSlotId"]] = playerAvailData[a]["availability"];
    }
    cells.forEach(function (cell) {
        cell.innerHTML = "";
        var timeslotId = cell.getAttribute("data-timeslot-id");
        if (rearrangeAvailData[timeslotId] == AVAILABLE_LP) {
            cell.innerHTML = "---";
        }
        if (rearrangeAvailData[timeslotId] == UNAVAILABLE) {
            cell.innerHTML = "XXX";
        }

        for (let e of events_from_server) {
            if (e["timeslot"] == timeslotId) {
                if (e["players"].includes(parseInt(playerId))) {
                    let myString = "";
                    if (rearrangeAvailData[timeslotId] == AVAILABLE_LP) {
                        myString += "---";
                    }
                    if (rearrangeAvailData[timeslotId] == UNAVAILABLE) {
                        myString += "XXX";
                    }
                    if (e["captain"] == parseInt(playerId)) {
                        myString += "C";
                    }
                    myString += e.court_name;
                    cell.innerHTML = myString;
                }
            }
        }
    });

    let headers = targetTable.querySelectorAll("th");
    let lastHeaderValue = null;
    let colorFlag = false; // flag to decide which color to use

    headers.forEach((header, index) => {
        // if the header value is different from the last one or it's the first header
        if (lastHeaderValue !== header.innerHTML || index === 0) {
            colorFlag = !colorFlag; // toggle the color flag
            lastHeaderValue = header.innerHTML;
        }

        // get all the cells in this column
        let columnCells = targetTable.querySelectorAll(`td:nth-child(${index + 1}), th:nth-child(${index + 1})`);

        // apply the color based on the flag
        columnCells.forEach((cell) => {
            if (colorFlag) {
                cell.style.backgroundColor = "white";
            } else {
                cell.style.backgroundColor = ""; // reset to default color or you can set to another color if desired
            }
        });
    });
}

// Function to rename radio buttons
/**
 * @description The function renameRadioButtons renames the name of radio buttons
 * based on their data-captain-id attribute, and sets the checked state of the radio
 * button to true if the data-player-id matches the value of the shouldBeCaptain attribute.
 *
 * @param { array } draggableTargets - The `draggableTargets` input parameter is an
 * array of HTML elements that are being processed by the function.
 */
function renameRadioButtons(draggableTargets) {
    for (var i = 0; i < draggableTargets.length; i++) {
        var target = draggableTargets[i];
        var courtId = target.getAttribute("data-court-id");
        var timeId = target.getAttribute("data-time-id");
        var shouldBeCaptain = target.getAttribute("data-captain-id");
        var radioButtonName = "player-is-captain-input-" + courtId + "-" + timeId;
        var radioButtons = target.getElementsByTagName("input");
        for (var j = 0; j < radioButtons.length; j++) {
            var radioButton = radioButtons[j];
            if (radioButton.type === "radio") {
                radioButton.name = radioButtonName;
                if (radioButton.getAttribute("data-player-id") == shouldBeCaptain) {
                    radioButton.checked = true; // need to add endpoints
                }
            }
        }
    }
}

// Main function to call the other functions
/**
 * @description The function updatePlayerCount updates the player count and schedules
 * for each player in the draggable items, and renames radio buttons.
 */
function updatePlayerCount() {
    var scheduleDiv = document.getElementById("schedule");
    var players = document.querySelectorAll(".draggable-item");
    var draggableTargets = scheduleDiv.getElementsByClassName("draggable-target");
    renameRadioButtons(draggableTargets);
    players.forEach(function (player) {
        updatePlayerGameCount(player, scheduleDiv);
        updatePlayerCaptainCount(player, scheduleDiv);
        updatePlayerScheduleCount(player, scheduleDiv);
        updateTableView(player, scheduleDiv);
    });
    populateMatrix();
}

/**
 * @description The function `resetCellColors` resets the background colors and
 * availability values of all cells with the class `draggable-target` within an element
 * with the ID `schedule`.
 */
function resetCellColors() {
    var allCells = document.querySelectorAll("#schedule .draggable-target");
    allCells.forEach(function (cell) {
        cell.style.backgroundColor = "";
        cell.setAttribute("data-availability", 0);
    });

    highlightDuplicatePlayers();
}

/**
 * @description The function highlightDuplicatePlayers scans a table of player names
 * and highlights cells that contain duplicate player names.
 */
function highlightDuplicatePlayers() {
    // Select the table element
    const table = document.querySelector("#custom-grid");

    // Go through each column (skipping the first one, which has court names)
    const colLength = table.rows[0].cells.length;
    for (let colIndex = 1; colIndex < colLength; colIndex++) {
        const playerNames = {};
        const firstOccurrenceCells = {}; // Keep track of where each player name first appears
        const duplicateCells = [];

        // Go through each row in the current column
        for (let rowIndex = 0; rowIndex < table.rows.length; rowIndex++) {
            const cell = table.rows[rowIndex].cells[colIndex];
            const draggableItems = cell.querySelectorAll(".draggable-item");

            // Go through each draggable item in the cell
            draggableItems.forEach((draggableItem) => {
                const playerName = draggableItem.getAttribute("data-player-name");

                // Initialize the player name count or increment it
                if (!playerNames[playerName]) {
                    playerNames[playerName] = 0;
                    firstOccurrenceCells[playerName] = cell; // Store the first occurrence
                }
                playerNames[playerName]++;

                // Mark the cell for highlighting if a player is duplicated
                if (playerNames[playerName] > 1) {
                    duplicateCells.push(cell);

                    // Also add the cell where this player name first appeared
                    duplicateCells.push(firstOccurrenceCells[playerName]);
                }
            });
        }

        // If duplicates exist, highlight the duplicate cells in this column
        if (duplicateCells.length > 0) {
            // Use a Set to ensure that each cell is only added once
            const uniqueDuplicateCells = [...new Set(duplicateCells)];

            uniqueDuplicateCells.forEach((cell) => {
                cell.style.backgroundColor = "darkorange";
            });
        }
    }
}

/**
 * @description This function highlights the availability of time slots in a schedule.
 *
 * @param { array } playerAvailData - The `playerAvailData` input parameter is an
 * array of objects, where each object represents a time slot and contains the
 * availability status for that time slot.
 */
function highlightAvailability(playerAvailData, playerID) {
    // Reset colors and availability attributes
    resetCellColors();

    // Check availability for each time slot
    if (Array.isArray(playerAvailData)) {
        playerAvailData.forEach(function (timeSlot) {
            const timeSlotId = timeSlot["timeSlotId"];
            const availability = timeSlot["availability"];

            const cells = document.querySelectorAll(`#schedule .draggable-target[data-time-id="${timeSlotId}"]`);
            cells.forEach(function (cell) {
                cell.setAttribute("data-availability", availability);

                switch (availability) {
                    case 1:
                        cell.style.backgroundColor = "lightgreen";
                        break;
                    case 2:
                        cell.style.backgroundColor = "lightyellow";
                        break;
                    case 3:
                        cell.style.backgroundColor = "lightcoral";
                        break;
                    default:
                        cell.style.backgroundColor = "";
                }

                // Check if the player already exists in the cell
                const draggableItems = cell.querySelectorAll(".draggable-item");
                draggableItems.forEach((draggableItem) => {
                    const playerIDval = draggableItem.getAttribute("data-player-id");

                    if (playerID == playerIDval) {
                        // Replace this condition with the actual condition to match the player
                        cell.style.backgroundColor = "blue";
                    }
                });
            });
        });
    }
}
// function highlightAvailability(playerAvailData) {
//     // Reset colors and availability attributes
//     resetCellColors();

//     // Check availability for each time slot
//     if (Array.isArray(playerAvailData)) {
//         playerAvailData.forEach(function (timeSlot) {
//             var timeSlotId = timeSlot["timeSlotId"];
//             var availability = timeSlot["availability"];

//             var cells = document.querySelectorAll(`#schedule .draggable-target[data-time-id="${timeSlotId}"]`);
//             cells.forEach(function (cell) {
//                 cell.setAttribute("data-availability", availability);
//                 switch (availability) {
//                     case 1:
//                         cell.style.backgroundColor = "lightgreen";
//                         break;
//                     case 2:
//                         cell.style.backgroundColor = "lightyellow";
//                         break;
//                     case 3:
//                         cell.style.backgroundColor = "lightcoral";
//                         break;
//                     default:
//                         cell.style.backgroundColor = "";
//                 }
//             });
//         });
//     }
// }

/**
 * @description This function sets up event handling for incoming events from the server.
 */
function setupEvents() {
    console.log(events_from_server);
    for (let e of events_from_server) {
        let courtID = e["court"];
        let timeID = e["timeslot"];
        // Find the td that matches courtID and timeID
        let targetTd = document.querySelector(`td[data-court-id="${courtID}"][data-time-id="${timeID}"]`);
        for (let playerID of e["players"]) {
            // Find the draggable item with data-player-id == playerID
            let playerDiv = document.querySelector(`div[data-player-id="${playerID}"]`);
            // Make a copy of the draggable item
            let playerDivCopy = playerDiv.cloneNode(true);
            // Put the copy in the td
            targetTd.appendChild(playerDivCopy);
            targetTd.setAttribute("data-captain-id", e["captain"]);
        }
    }
}

/**
 * @description The function `clearSchedule()` removes all child elements of an element
 * with the ID "schedule" that have a class of "draggable-item".
 */
function clearSchedule() {
    var scheduleDiv = document.getElementById("schedule");
    var players = scheduleDiv.querySelectorAll(".draggable-item");
    players.forEach(function (player) {
        var playerParent = player.parentNode;
        playerParent.removeChild(player);
    });
}

/**
 * @description This function fetches events for a specific flightID.
 *
 * @param { string } flightID - The `flightID` input parameter is used to specify the
 * ID of the flight for which the function should retrieve events.
 *
 * @returns { object } - The output returned by this function is an array of events.
 */
async function getEvents(flightID) {
    try {
        const response = await fetch(`/flights/${flightID}/events/get`, {
            method: "POST", // or 'GET' if your endpoint is designed to respond to GET
            headers: {
                "Content-Type": "application/json",
                // Include additional headers here like authorization headers if necessary
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            console.error(`Server responded with error: ${data.error}`);
            return null;
        } else {
            return data.events;
        }
    } catch (error) {
        console.error(`Failed to fetch events: ${error}`);
        return null;
    }
}

/**
 * @description The function lerp(start, end, amt) returns a value that is a linear
 * interpolation of start and end, based on the amount amt.
 *
 * @param { number } start - START PROCESSING.
 *
 * @param { number } end - END INPUT PARAMETER PROVIDES THE FINAL VALUE TOWARDS WHICH
 * THE START VALUE SHOULD BE LERPED.
 *
 * @param amt - The `amt` input parameter in the `lerp` function determines the amount
 * of movement between the `start` and `end` values.
 *
 * @returns {  } - The output returned by this function is the value obtained by
 * adding the difference between the start and end values to the start value, multiplied
 * by the given amount.
 */
function lerp(start, end, amt) {
    return start + (end - start) * amt;
}

/**
 * @description The function rgbLerp takes three arguments: rgb1, rgb2, and amt, and
 * returns an object with the RGB values of the two input colors linearly interpolated
 * based on the amount of interpolation.
 *
 * @param { object } rgb1 - The `rgb1` input parameter provides the starting color
 * value for the interpolation.
 *
 * @param { object } rgb2 - The `rgb2` input parameter provides the target color for
 * the lerping process.
 *
 * @param amt - The `amt` input parameter controls the amount of interpolation between
 * the two RGB values.
 *
 * @returns { object } - The output returned by the `rgbLerp` function is an object
 * with three properties: `r`, `g`, and `b`, each containing a rounded value of the
 * linear interpolation of the corresponding component of the two input RGB values.
 */
function rgbLerp(rgb1, rgb2, amt) {
    return {
        r: Math.round(lerp(rgb1.r, rgb2.r, amt)),
        g: Math.round(lerp(rgb1.g, rgb2.g, amt)),
        b: Math.round(lerp(rgb1.b, rgb2.b, amt)),
    };
}

/**
 * @description The function `populateMatrix` populates a matrix with player pair
 * counts based on draggable targets and flight rules. It loops through each draggable
 * target, gathers player IDs, and calculates the number of pairs for each player ID.
 *
 * @returns { object } - The `populateMatrix()` function returns nothing, as it only
 * modifies the styles and content of the HTML table element with id "player-matrix".
 * The function populates the table with player pair counts, using a compact and
 * efficient algorithm that assigns a unique key to each player pair and uses a hash
 * table to keep track of the counts.
 */
function populateMatrix() {
    let playerPairCounts = {};

    // Gather all player IDs available in the matrix
    let playerIds = [];
    $("#player-matrix [data-player-anchor]").each(function () {
        playerIds.push($(this).data("player-anchor"));
    });

    // Init the counts
    for (let i = 0; i < playerIds.length; i++) {
        for (let j = 0; j < playerIds.length; j++) {
            if (i !== j) {
                let key = `${playerIds[i]}-${playerIds[j]}`;
                playerPairCounts[key] = 0;
            }
        }
    }

    // Loop through each draggable-target to gather counts
    $(".draggable-target").each(function () {
        let presentPlayerIds = $(this)
            .find(".draggable-item")
            .map(function () {
                return $(this).data("player-id");
            })
            .get();

        for (let i = 0; i < presentPlayerIds.length; i++) {
            for (let j = i + 1; j < presentPlayerIds.length; j++) {
                let key1 = `${presentPlayerIds[i]}-${presentPlayerIds[j]}`;
                let key2 = `${presentPlayerIds[j]}-${presentPlayerIds[i]}`;
                if (key1 in playerPairCounts) {
                    playerPairCounts[key1]++;
                }
                if (key2 in playerPairCounts) {
                    playerPairCounts[key2]++;
                }
            }
        }
    });

    // let maxCount = Math.max(...Object.values(playerPairCounts));
    let maxCount = LEAGUE_RULE_MIN_GAMES;

    let green = { r: 173, g: 255, b: 47 };
    let red = { r: 240, g: 128, b: 128 };

    $("#always-empty, #player-matrix td[data-player-row][data-player-column]")
        .filter(function () {
            return $(this).data("player-row") === $(this).data("player-column");
        })
        .css("background-color", "darkgrey");

    $("#player-matrix td:not(:first-child)").each(function () {
        let rowPlayerId = $(this).data("player-row");
        let colPlayerId = $(this).data("player-column");
        let countKey = `${rowPlayerId}-${colPlayerId}`;
        let count = playerPairCounts[countKey] || 0;

        if (rowPlayerId === colPlayerId) {
            $(this).css("background-color", "darkgrey");
            return; // skip to the next iteration without further processing for this cell
        }

        $(this).text(count);

        if (count === 0) {
            $(this).css("background-color", "grey");
        } else if (count === 1) {
            $(this).css("background-color", `rgb(${green.r},${green.g},${green.b})`);
        } else {
            let lerpAmt = (count - 1) / (maxCount - 1);
            let color = rgbLerp(green, red, lerpAmt);
            $(this).css("background-color", `rgb(${color.r},${color.g},${color.b})`);
        }
    });
}

/**
* @description This function clearDraggableOrigins resets the background color of 
* all elements with a class name draggable-origin to an empty string, voiding any 
* previously set background colors.
*/
function clearDraggableOrigins() {
    const allDraggableOrigins = document.querySelectorAll(".draggable-origin");
    allDraggableOrigins.forEach((origin) => {
        origin.style.backgroundColor = ""; // Resetting the background color to empty
    });
}

// Function to highlight draggable origins based on availability
/**
 * @description The function highlightAvailablePlayers adds an event listener to each
 * cell in a custom grid, listening for mousedown and mouseup events. When a cell is
 * clicked, it resets the background colors of all draggable origin elements, and
 * then checks the availability of each player for the current time slot.
 */
function highlightAvailablePlayers() {
    // Get all the cells in the custom grid
    const cells = document.querySelectorAll("#custom-grid .draggable-target");

    // Add a mouse-down event listener to each cell
    cells.forEach((cell) => {
        cell.addEventListener("mousedown", function () {
            setTimeout(() => {
                if (!is_dragging) {
                    const timeslot = cell.getAttribute("data-time-id");

                    // 1. Get the index of the column of the clicked cell.
                    const columnIndex = [...cell.parentNode.children].indexOf(cell);

                    // 2. Use this column index to select all the cells in this column.
                    const columnCells = [
                        ...document.querySelectorAll(`#custom-grid tr td:nth-child(${columnIndex + 1})`),
                    ];

                    // 3. From these cells, extract the player IDs.
                    let playerIdsInColumn = [];
                    columnCells.forEach((columnCell) => {
                        const draggableItems = columnCell.querySelectorAll(".draggable-item");
                        draggableItems.forEach((item) => {
                            const playerId = item.getAttribute("data-player-id");
                            playerIdsInColumn.push(playerId);
                        });
                    });

                    // // Deduplicate the player IDs in case there are any duplicates.
                    // playerIdsInColumn = [...new Set(playerIdsInColumn)];
                    // Reset all draggable origin backgrounds first
                    const allDraggableOrigins = document.querySelectorAll(".draggable-origin");
                    allDraggableOrigins.forEach((origin) => {
                        origin.style.backgroundColor = "";
                        const draggableItem = origin.querySelector(".draggable-item");
                        const playerId = draggableItem.getAttribute("data-player-id");
                        var docolor = true;
                        if (playerIdsInColumn.includes(playerId)) {
                            docolor = false;
                        } 
                        const foundTimeSlot = playerAvailability[playerId].find(
                            (record) => record.timeSlotId === parseInt(timeslot)
                        );
                        if (docolor && foundTimeSlot) {
                            // console.log(`The availability for timeSlotId ${timeslot} is ${foundTimeSlot.availability}`);
                            if (foundTimeSlot.availability == AVAILABLE) {
                                origin.style.backgroundColor = "lightgreen";
                            } else if (foundTimeSlot.availability == AVAILABLE_LP) {
                                origin.style.backgroundColor = "lightyellow";
                            } else {
                                origin.style.backgroundColor = "lightcoral";
                            }
                        }
                    });
                } else {
                    clearDraggableOrigins();
                }
            }, 0);
        });
        document.addEventListener("mouseup", function () {
            clearDraggableOrigins();
        });
    });
}

// Call the function to set up the mouse-down event listeners
highlightAvailablePlayers();
