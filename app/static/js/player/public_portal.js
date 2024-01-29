document.addEventListener("DOMContentLoaded", function () {
    var availabilities = document.querySelectorAll(".availability_indicator");
    availabilities.forEach(function (button) {
        button.addEventListener("click", function () {
            availabilityCallback(button);
        });
    });
});


/* <button id={{ts.id}} avail={{avail}} type="button" class="availability_indicator btn btn-sm btn-success">I am in!</button>
{% elif avail == 2 %}
<button id={{ts.id}} avail={{avail}} type="button" class="availability_indicator btn btn-sm btn-warning">...Maybe</button>
{% elif avail == 3 %}
<button id={{ts.id}} avail={{avail}} type="button" class="availability_indicator btn btn-sm btn-danger">Nope</button> */


function saveAvailability(){
    elems = document.querySelectorAll('.availability_indicator')
    result = []
    elems.forEach((e)=>{
        a = parseInt(e.getAttribute('avail'))
        ts = parseInt(e.id)
        result.push({'timeslot': ts, 'availability': a})
    })
    console.log(result)
    sendToServer(
        { msg: "availability", data: result },
        (success = () => {
            window.location.reload();
        }),
        (failure = null)
    );
}

function availabilityCallback(button) {
    current = parseInt(button.getAttribute("avail"));
    console.log(current);
    switch (current) {
        case 1:
            button.querySelector('.availability-status').textContent = '...Maybe'
            button.setAttribute("avail", 2)
            button.classList.remove('btn-outline-success')
            button.classList.add('btn-outline-warning')
            break;
        case 2:
            button.querySelector('.availability-status').textContent = 'Nope'
            button.setAttribute("avail", 3)
            button.classList.remove('btn-outline-warning')
            button.classList.add('btn-outline-danger')
            break;
        case 3:
            button.querySelector('.availability-status').textContent = 'I am in!'
            button.setAttribute("avail", 1)
            button.classList.remove('btn-outline-danger')
            button.classList.add('btn-outline-success')
            break;
    }

}

/**
* @description This function sends data to the server via fetch API and handles
* success and failure responses. It takes three arguments: 'data', 'success', and
* 'failure' (which are all optional).
* 
* @param { object } data - The `data` input parameter is the data that is being sent
* to the server via a POST request.
* 
* @param {  } success - The `success` input parameter is an optional callback function
* that is called if the server responds with a "success" status.
* 
* @param {  } failure - The `failure` input parameter is a callback function that
* is executed if the server responds with an error.
* 
* @returns { object } The `sendToServer` function takes a `data` object and two
* callback functions: `success` and `failure`. It sends a POST request to the current
* URL with the `data` object encoded as JSON. If the server responds with an error
* status code (e.g., 404), the function rejects with an error message containing the
* status code. If the server responds with "success", the function logs a success
* message and calls the `success` callback with the response data. Otherwise (i.e.,
* the server returns any other response status code), the function logs an error
* message and calls the `failure` callback with the response data.
*/
function sendToServer(data, success = null, failure = null) {
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
                if (success) {
                    success(data);
                }
            } else {
                console.log("Failure: ", data.error);
                if (failure) {
                    failure(data);
                }
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}

/**
* @description This function called "changeTheme" changes the theme of a web page
* and notifies the server about the new theme. It takes one parameter called "theme"
* and logs a message to the console indicating the new theme.
* 
* @param { string } theme - The `theme` input parameter passed to the `changeTheme()`
* function represents the selected theme that needs to be applied to the page.
* 
* @returns { any } The output returned by this function is "Theme changed to: <selected_theme>".
*/
function changeTheme(theme) {
    // Call your JavaScript function here with the selected theme
    // For example, you can update the page's styles based on the theme.
    sendToServer(
        { msg: "change_theme", theme: theme },
        (success = () => {
            window.location.reload();
        }),
        (failure = null)
    );

    // Replace the console.log with your desired logic.
}
