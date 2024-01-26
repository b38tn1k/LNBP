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


function availabilityCallback(button) {
    console.log("Button clicked:", button.textContent);
    current = parseInt(button.getAttribute("avail"));
    console.log(current);
    switch (current) {
        case 1:
            button.textContent = '...Maybe'
            button.setAttribute("avail", 2)
            button.classList.remove('btn-success')
            button.classList.add('btn-warning')
            break;
        case 2:
            button.textContent = 'Nope'
            button.setAttribute("avail", 3)
            button.classList.remove('btn-warning')
            button.classList.add('btn-danger')
            break;
        case 3:
            button.textContent = 'I am in!'
            button.setAttribute("avail", 1)
            button.classList.remove('btn-danger')
            button.classList.add('btn-success')
            break;
    }

}

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

function changeTheme(theme) {
    // Call your JavaScript function here with the selected theme
    // For example, you can update the page's styles based on the theme.
    console.log("Theme changed to:", theme);

    sendToServer(
        { msg: "change_theme", theme: theme },
        (success = () => {
            window.location.reload();
        }),
        (failure = null)
    );

    // Replace the console.log with your desired logic.
}
