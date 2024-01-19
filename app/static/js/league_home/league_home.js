document.addEventListener("DOMContentLoaded", function () {
    // document.getElementById("run-schedule-wizard").addEventListener("click", function () {
    //     const data = {
    //         msg: "schedule-all",
    //     };
    //     doFetch(data, null, null);
    // });
    // document.getElementById("test-email").addEventListener("click", function () {
    //     const data = {
    //         msg: "test-email",
    //     };
    //     doFetch(data, null, null);
    // });
});

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
    let loaderClass = setButtonLoading(button, "fe-star")

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
    }
    sendToServer(data, success, failure);
}

/**
* @description This function sends data to the server via fetch API. It sets the
* content type to application/json and includes the csrf token to prevent CSRF
* attacks. The function makes a POST request to the current URL and if the response
* is not okay (200), it will reject the promise with the status message. Then it
* parses the response as JSON and checks the status of the response. If the status
* is "success" it logs a success message and calls the success callback function.
* If the status is "failure" it logs an error message and calls the failure callback
* function.
* 
* @param { object } data - The `data` input parameter is used to send a JSON object
* of data to the server for ingestion.
* 
* @param {  } success - The `success` input parameter is a callback function that
* is called when the data is successfully ingested by the server.
* 
* @param {  } failure - The `failure` parameter is a callback function that is called
* if the server response has an error or status that is not "success".
* 
* @returns { Promise } The output of this function is a promise that resolves to the
* server's response JSON data. The function takes three arguments: `data`, `success`,
* and `failure`. It sends a POST request to the current URL with the provided data
* and CSFR token. If the response status is not "ok", it rejects the promise with
* an error message. Otherwise it returns the response JSON data.
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
                console.log("Data successfully ingested by server.");
                success();
                // window.location.reload();
            } else {
                console.log("Failure: ", data.error);
                failure();
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
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
