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

function scheduleWizardButtonCallback() {
    let button = document.getElementById("run-schedule-wizard");
    let loaderClass = setButtonLoading(button, "fe-star")

    const data = {
        msg: "schedule-all",
    };

    function success() {
        flashButtonResult(button, "fe-check-circle", "fg-success", loaderClass, "fe-star");
    }

    function failure() {
        flashButtonResult(button, "fe-x-circle", "fg-failure", loaderClass, "fe-star");
    }
    sendToServer(data, success, failure);
}

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

function setButtonLoading(button, defaultClass) {
    let r = button.querySelector("i");
    r.classList.remove(defaultClass);
    r.classList.add("fe-loader");
    return "fe-loader";
}

function flashButtonResult(button, c1, c2, removableClass, defaultClass) {
    let r = button.querySelector("i");
    r.classList.remove(removableClass);
    r.classList.add(c1, c2);
    setTimeout(function () {
        r.classList.remove(c1, c2);
        r.classList.add(defaultClass);
    }, 1000);
}
