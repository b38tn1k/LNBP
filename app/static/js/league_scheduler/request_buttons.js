function assignCaptainsCallback(button) {
    console.log(button);
    let flightID = -1;
    let tabs = document.getElementById("flight-tabs");
    flights = tabs.querySelectorAll(".nav-item");
    flights.forEach((i) => {
        a = i.querySelector("a");
        console.log(a);
        if (a.classList.contains("active")) {
            flightID = parseInt(a.getAttribute("flight-id"));
        }
    });
    console.log(flightID);
    // button.disabled = true;
    data = {};
    data["contents"] = "captains";
    data["flight_id"] = flightID;
    sendToServer(
        data,
        () => {
            window.location.reload();
        },
        () => {
            window.location.reload();
        }
    );
}

/**
 * @description The function `saveButtonCallback()` collects all flight data using
 * the function `collectAllFlightData()`.
 */
function saveButtonCallback(event) {
    let data = { contents: "games" };
    data["data"] = getAllGames();
    let button = event.target.closest("button");
    button.disabled = true;

    /**
     * @description This function sets the `disabled` attribute of a button to `true` and
     * changes its display icon to a green check mark ("fe-check-circle") with a success
     * theme (".fg-success").
     *
     * @returns { any } The function `success` takes no arguments and returns nothing (void).
     */
    function success(data) {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-check-circle", "fg-success", "fe-save");
        window.location.reload();
    }

    /**
     * @description This function sets the button `disabled` and changes its appearance
     * to indicate failure (flashing an "X" icon with a red background).
     *
     * @returns { any } The function `failure` does not return any value explicitly. It
     * manipulates the properties of a button object named `button`. It disables the
     * button and displays an error icon and message on the button using `toggleButtonDisabled()`
     * and `flashButtonResult()`.
     */
    function failure(data) {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-x-circle", "fg-failure", "fe-save");
        window.location.reload();
    }

    sendToServer(data, success, failure);
}

/**
 * @description This function creates a callback for a button click event that schedules
 * a flight. It retrieves the currently active flight tab and passes its ID to the
 * server along with other data.
 *
 * @param {  } event - The `event` input parameter is passed to the function from the
 * button's `onClick` event listener.
 *
 * @returns { object } This function takes an event object as a parameter and returns
 * nothing (undefined) because it does not have a return statement. The function
 * prepares data to be sent to the server based on the active flight tab and disables
 * the button. It then calls two functions: success and failure.
 */
function generateButtonCallback(event) {
    let data = { contents: "schedule" };
    const tabs = document.querySelectorAll(".flight-tab");
    let target_flight = -1;
    tabs.forEach((tab) => {
        if (tab.classList.contains("active")) {
            target_flight = parseInt(tab.getAttribute("flight-id"));
        }
    });
    data["data"] = { flight_id: target_flight };
    let button = event.target.closest("button");
    button.disabled = true;
    /**
     * @description This function sets a toggle button's disabled status to false (enabling
     * it), flashes an icon next to the button indicating success and replaces it with a
     * different icon afterwards.
     *
     * @returns { any } The function `success` returns nothing (undefined) because it is
     * an anonymous function and does not have a return statement.
     */
    function success(data) {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-check-circle", "fg-success", "fe-star");
        window.location.reload();
    }
    /**
     * @description This function triggers the failure state of a button by disabling it
     * and changing its appearance with icons and colors.
     *
     * @returns {  } The output of the `failure()` function is not defined because the
     * function contains statements that do not return any value.
     */
    function failure(data) {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-x-circle", "fg-failure", "fe-star");
        window.location.reload();
    }
    sendToServer(data, success, failure);
}

/**
 * @description This function takes a button element and two classes as parameters
 * and applies the two classes to the button's `i` element for 1 second before reverting
 * back to the original "fe-save" class.
 *
 * @param { object } button - The `button` input parameter is not used within the
 * function. It is declared but not referred to or passed as an argument within the
 * function body.
 *
 * @param { string } c1 - The `c1` input parameter is used to add a class name to the
 * HTML element represented by `r` (an icon button's inner button element) for a
 * duration of 1 second before it is removed and the "fe-save" class is added.
 *
 * @param { string } c2 - The `c2` input parameter is used to add an additional CSS
 * class to the `i` element within the `button` element for a duration of 1 second
 * before being removed and replaced by the class "fe-save".
 *
 * @returns {  } The output of this function is that it adds and then removes two
 * class names from an `i` element inside a button after a delay of 1 second.
 *
 * Here's the output concisely described:
 *
 * 	- Add class name "fe-save" to the `i` element.
 * 	- Add class names "c1" and "c2" to the `i` element.
 * 	- Remove class names "c1" and "c2" from the `i` element after 1 second.
 * 	- Remove class name "fe-save" from the `i` element.
 */
function flashButtonResult(button, c1, c2, defaultClass) {
    let r = button.querySelector("i");
    r.classList.remove(defaultClass);
    r.classList.add(c1, c2);
    setTimeout(function () {
        r.classList.remove(c1, c2);
        r.classList.add(defaultClass);
    }, 1000);
}

/**
 * @description This function toggles the disabled state of a button element.
 *
 * @param { object } button - The `button` input parameter of the `toggleButtonDisabled()`
 * function is not used and has no effect on the function's behavior.
 *
 * @returns { any } The output returned by this function is `button.disabled`.
 */
function toggleButtonDisabled(button) {
    button.disabled = !button.disabled;
}

/**
 * @description This function sends a POST request to the server with the given `data`
 * and calls either `success` or `failure` callbacks depending on the server's response
 * status.
 *
 * @param { object } data - The `data` input parameter is used to send data to the
 * server as a JSON-formatted string.
 *
 * @param {  } success - The `success` input parameter is a callback function that
 * is called when the data is successfully ingested by the server.
 *
 * @param {  } failure - The `failure` parameter is a callback function that is
 * executed if the server response indicates failure (i.e., data.status === "error").
 *
 * @returns { object } This function takes three arguments: `data`, `success`, and
 * `failure`. It makes a POST request to the current URL with the data provided and
 * appends an `X-CSRFToken` header with the value of a hidden input on the page.
 *
 * If the fetch is successful (200 status), it parses the JSON response data and
 * checks if it has a "status" key. If "status" is "success", it logs a success message
 * and calls the `success` function. If "status" is anything else or there is no
 * "status" key present at all (400+ status), it logs an error message and calls the
 * `failure` function.
 */
function sendToServer(data, success, failure) {
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
                console.log("Data successfully ingested by server.", data);
                success();
                // window.location.reload();
            } else {
                console.log("Failure: ", data.error);
                failure();
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}
