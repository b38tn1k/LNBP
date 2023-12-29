// Get the script tag
const scriptTag = document.querySelector("script[src$='module-selector-add-remove-players.js']");

// Get the flight ID from the dataset attribute
const flightId = scriptTag.dataset.flightId;

// Get all the player switches
const playerSwitches = document.querySelectorAll(".player-switch");

// Add event listener to each player switch
playerSwitches.forEach((playerSwitch) => {
    playerSwitch.addEventListener("change", function () {
        const playerId = this.getAttribute("id").replace("player-switch-", "");
        const playerName = this.nextElementSibling.innerText.trim();
        console.log(flightId);

        if (this.checked) {
            // Send a POST request to add the player to the flight
            fetch('/flights/'+flightId+'/players/add', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ player_id: playerId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(`Add player to flight: ID-${playerId}, Name-${playerName}`);
                    console.log("Response:", data);
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        } else {
            // Send a POST request to remove the player from the flight
            fetch('/flights/'+flightId+'/players/remove', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ player_id: playerId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(`Remove player from flight: ID-${playerId}, Name-${playerName}`);
                    console.log("Response:", data);
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        }
    });
});
