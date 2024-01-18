document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("runScheduleWizard");

    button.addEventListener("click", function () {
        const data = {
            msg: "schedule-all",
        };
        doFetch(data, null, null);
    });
});

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
