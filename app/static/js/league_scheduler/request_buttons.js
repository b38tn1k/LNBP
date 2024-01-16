/**
 * @description The function `saveButtonCallback()` collects all flight data using
 * the function `collectAllFlightData()`.
 */
function saveButtonCallback(event) {
    let data = {contents: 'games'}
    data['data'] = getAllGames();
    let button = event.target.closest("button");
    button.disabled = true;

/**
* @description This function sets the `disabled` attribute of a button to `true` and
* changes its display icon to a green check mark ("fe-check-circle") with a success
* theme (".fg-success").
* 
* @returns { any } The function `success` takes no arguments and returns nothing (void).
*/
    function success() {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-check-circle", "fg-success", "fe-save");
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
    function failure() {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-x-circle", "fg-failure", "fe-save");
    }

    sendToServer(data, success, failure);
}

function generateButtonCallback(event) {
    let data = {contents: 'schedule'}
    const tabs = document.querySelectorAll(".flight-tab");
    let target_flight = -1;
    tabs.forEach((tab) => {
        if (tab.classList.contains("active")) {
            target_flight = parseInt(tab.getAttribute("flight-id"));
        }
    });
    data['data'] = {flight_id : target_flight}
    let button = event.target.closest("button");
    button.disabled = true;
    function success() {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-check-circle", "fg-success", "fe-star");
        window.location.reload();
    }
    function failure() {
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
* @description This function sends JSON-formatted data to the server using `fetch`,
* with the option to perform an HTTP POST request and specify a CSRF token for validation.
* 
* @param { object } data - The `data` input parameter is the JSON payload that will
* be sent to the server.
* 
* @param {  } after - The `after` parameter is a callback function that is called
* after the asynchronous request to the server has been made and the response has
* been processed.
* 
* @returns { Promise } The output of the `sendToServer` function is a Promise that
* resolves with the response from the server (either success or failure) after sending
* data to the server using fetch API.
*/
function sendToServer(data, after) {
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
                after();
                // window.location.reload();
            } else {
                console.log("Failure: ", data.error);
                after();
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}
