document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("runScheduleWizard");

    button.addEventListener("click", function () {
        const data = {
            msg: "schedule-all",
        };
        doFetch(data, null, null);
    });
});

/**
* @description This function sends a POST request to the current URL with the given
* data and triggers a callback function for either success or failure based on the
* response status.
* 
* @param { object } data - The `data` input parameter is the data that is being sent
* to the server via POST request.
* 
* @param {  } success - The `success` input parameter is a callback function that
* will be called with the response data from the server when the request is successful
* (i.e., has a status of "success").
* 
* @param {  } failure - The `failure` parameter is a callback function that is called
* if the API request fails (i.e., if the `response.json()` promise is rejected).
*/
function doFetch(data, success, failure) {
    const csrf_token = document.querySelector('#hidden-form input[name="csrf_token"]').value;
    fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((res) => {
            console.log(res);
            if (res.status === "success") {
                // success();
            } else {
                // failure();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
