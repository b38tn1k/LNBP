/**
 * @description The function `saveButtonCallback()` collects all flight data using
 * the function `collectAllFlightData()`.
 */
function saveButtonCallback(event) {
    let data = {contents: 'games'}
    data['data'] = getAllGames();
    let button = event.target.closest("button");
    button.disabled = true;

    function success() {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-check-circle", "fg-success");
    }

    function failure() {
        toggleButtonDisabled(button);
        flashButtonResult(button, "fe-x-circle", "fg-failure");
    }

    sendToServer(data, success, failure);
}

function flashButtonResult(button, c1, c2) {
    let r = button.querySelector("i");
    r.classList.remove("fe-save");
    r.classList.add(c1, c2);
    setTimeout(function () {
        r.classList.remove(c1, c2);
        r.classList.add("fe-save");
    }, 1000);
}

function toggleButtonDisabled(button) {
    button.disabled = !button.disabled;
}

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
