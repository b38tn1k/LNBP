let playerID = document.currentScript.getAttribute("data-player-id");
$(document).ready(function () {
    // Find all divs with class "flight-availability" and extract their IDs
    let flightDivs = $(".flight-availability");
    let flightIds = flightDivs
        .map(function () {
            return $(this).attr("id");
        })
        .get();

    // Call the function with the player ID and the array of flight IDs
    getAvailabilityData(playerID, flightIds);
    $(".three-way-switch input[type='radio']").change(function () {
        // Get the parent form-block of the changed switch
        const formBlock = $(this).closest(".form-block");

        // Get the flight ID from the parent div
        const flightId = formBlock.attr("id");

        // Initialize an empty array to store the current selected options for switches
        const selectedOptions = [];

        // Loop through all switches inside the form-block
        formBlock.find(".three-way-switch input[type='radio']").each(function () {
            // Check the state of the switch and add the corresponding option to the array
            if ($(this).is(":checked")) {
                // Get the time slot ID from the parent tr element of the switch
                const timeSlotId = $(this).closest("tr").attr("id");

                // Translate the text to the corresponding values (1, 2, or 3)
                const switchValue = $(this).val();

                // Add the time slot ID and switch value to the array as a dictionary
                selectedOptions.push({ timeSlotId: timeSlotId, availability: parseInt(switchValue) });
            }
        });

        // Create the final object with flight ID and availability data
        const availabilityData = { flight_id: flightId, availability: selectedOptions };

        // Send the availability data to the server using the Fetch API
        fetch("/players/" + playerID + "/addAvailability", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(availabilityData),
        })
            .then((response) => {
                if (response.ok) {
                    // Successful response, you can update the UI or perform other actions
                    console.log("Availability data saved successfully.");
                } else {
                    // Error handling if the response is not successful
                    console.log("Failed to save availability data.");
                }
            })
            .catch((error) => {
                console.error("An error occurred while sending the availability data:", error);
            });
    });
});

/**
* @description This function fetches availability data for a given player in multiple 
* flights, then updates radio switches on the web page to reflect the player's 
* availability for each flight.
* 
* @param { string } playerId - The `playerId` input parameter in the `getAvailabilityData()` 
* function represents the ID of the player whose availability data is being requested.
* 
* @param { array } flightIds - The `flightIds` input parameter is an array of flight 
* IDs that are passed to the function to fetch availability data for each flight.
* 
* @returns { object } - This function takes two arguments, `playerId` and an array 
* of `flightIds`. It fetches availability data for each flight ID and updates the 
* corresponding div elements with class "flight-availability" using jQuery.
*/
function getAvailabilityData(playerId, flightIds) {
    // Loop through each flight ID and fetch availability data for each flight
    flightIds.forEach((flightId) => {
        fetch(`/players/${playerId}/getAvailability?flight_id=${flightId}`)
            .then((response) => {
                if (response.ok) {
                    // Parse the response as JSON
                    return response.json();
                } else {
                    // Handle error response
                    throw new Error("Failed to fetch availability data.");
                }
            })
            .then((data) => {
                // Find the corresponding div element with class "flight-availability" and the same ID
                const flightDiv = $(`.flight-availability[id="${data.flight_id}"]`);

                let ad = data.availability;
                for (let a of ad) {
                    let timeSlotId = a.timeSlotId;
                    let switchValue = a.availability;
                    
                    // Find the radio switch with the corresponding time slot ID and switch value
                    const switchInput = flightDiv.find(`input[name="switch_${timeSlotId}"][value="${switchValue}"]`);

                    // Check if the switch exists before updating it
                    if (switchInput.length) {
                        // Check the radio switch and uncheck the others with the same name
                        switchInput.prop("checked", true).addClass("auto-updated-switch");
                        $(`input[name="switch_${timeSlotId}"].auto-updated-switch`).not(switchInput).prop("checked", false).removeClass("auto-updated-switch");
                    } else {
                        // Handle the case when the switch does not exist (e.g., if the time slot was deleted)
                        console.warn(`Switch with name="switch_${timeSlotId}" and value="${switchValue}" not found.`);
                    }
                }
            })
            .catch((error) => {
                console.error(`An error occurred while fetching availability data for flight ${flightId}:`, error);
            });
    });
}
