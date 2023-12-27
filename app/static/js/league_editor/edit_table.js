/**
* @description This function takes data from a server and generates an HTML table
* for each flight. It creates the table header and body rows for date and time and
* adds players to the table. Additionally it includes add player button row to each
* flight and lists other flights as well.
* 
* @param { object } data - The `data` input parameter is an array of objects
* representing each league.
* 
* @returns { object } The output returned by the `step4DataFromServer` function is
* a dynamically created HTML table for each league data received from the server.
* Each table contains the following rows:
* 
* 1/ Header row with flight number and an Add Player button.
* 2/ Date and time rows for each game played on that day.
* 3/ A player row for each player participating on that particular flight.
* 4/ An Add Player button at the bottom of the table.
* 
* The function appends each table to the parent element with a specific class name
* ("top-flight", "bottom-flight", or "") based on its position within the list of
* leagues received from the server.
*/
function step4DataFromServer(data) {
    var parent = document.getElementById("clean-league");
    var child = parent.querySelector(".card-body");
    child.style.overflowX = "auto";
    let flightNumber = 1;
    let flightInput;
    let maxFlightNumber = data.length;
    data.forEach(function (league) {
        // Create League Header
        [flightNumber, flightInput] = createFlightHeader(flightNumber);

        child.appendChild(flightInput);

        // Create table
        const table = createFlightTable();
        table.id = "flight-" + String(flightNumber);
        table.classList.add("cleaned-flight");
        if (flightNumber == 1) {
            table.classList.add("top-flight");
        }
        if (flightNumber == maxFlightNumber) {
            table.classList.add("bottom-flight");
        }
        const tbody = document.createElement("tbody");

        // Create date and time rows
        let [dateRow, timeRow] = createFlightDateTimeRows(league);
        tbody.appendChild(dateRow);
        tbody.appendChild(timeRow);

        league.players.forEach(function (p) {
            const playerRow = createFlightPlayerRow(p, flightNumber, maxFlightNumber);
            tbody.appendChild(playerRow);
        });

        const addPlayerRow = createAddPlayerRowFlight(flightNumber);
        tbody.appendChild(addPlayerRow);

        table.appendChild(tbody);

        child.appendChild(table);

        table.addEventListener("click", handleFlightTableClick);
        flightNumber += 1;
    });
}

/**
* @description This function steps forward to step number 4 ( indicated by `stepIndex`
* variable being assigned value `4`) and then calls `step4DataFromServer()` with
* data passed as an argument( `data.data`).
* 
* @param { object } data - The `data` input parameter is passed from the previous
* step (i.e., `step3ClientSend`) and contains the data sent by the client to the server.
* 
* @returns { object } This function takes a single argument `data` and does the following:
* 
* 1/ It sets `stepIndex` to 4.
* 2/ It shows the current step (step 4).
* 3/ It calls `step4DataFromServer` with the data received from the server (which
* is contained within the `data` object).
* 
* The output returned by this function is not specified directly.
*/
function step4ServerResp(data) {
    stepIndex = 4;
    showStep(stepIndex);
    step4DataFromServer(data.data);
}

/**
 * @description This function sends data to the server as a CSV file.
 *
 * @returns { object } The output returned by this function is not defined because
 * it contains undefined statements and the function does not have a return statement.
 */
function stepIndex4Prep() {
    // const data = parseCellGroups();
    // sendToServer(data);

    // test
    fetch("/static/csv_league_import_example.json")
        .then((response) => response.json())
        .then((data) => {
            sendToServer(data, step4ServerResp);
        })
        .catch((error) => console.log("Error loading JSON: ", error));
}

/**
* @description This function takes a HTML table as input and returns an array of ISO
* datetime strings (format: "YYYY-MM-DDTHH:mm:ss") by combining the values from the
* date and time columns of each row.
* 
* @param { object } table - The `table` input parameter is used to pass a table
* element to the function.
* 
* @returns { array } The function `getCleanTimeSlots` takes a HTML table as input
* and returns an array of ISO date-time strings (YYYY-MM-DDTHH:mm:ss) extracted from
* the table's rows. It filters out incomplete or invalid date-time inputs and combines
* the date and time columns from each row to form the final ISO string.
*/
function getCleanTimeSlots(table) {
    const tbody = table.querySelector("tbody");
    const dateRow = tbody.rows[0];
    const timeRow = tbody.rows[1];
    const combinedDateTime = [];

    for (let i = 0; i < timeRow.cells.length; i++) {
        let dateInput = dateRow.cells[i + 1].querySelector("input");
        let timeInput = timeRow.cells[i].querySelector("input");

        if (dateInput && timeInput && dateInput.value && timeInput.value) {
            // Combine date and time directly
            let isoDateTime = dateInput.value + "T" + timeInput.value;
            combinedDateTime.push(isoDateTime);
        }
    }

    return combinedDateTime;
}

/**
* @description The provided function takes an array of HTML elements `titles` as
* input and returns an array of objects representing flight data.
* 
* @param { array } titles - The `titles` input parameter is an array of elements
* (presumably <title> tags) that the function processes to extract flight data.
* 
* @returns { object } The output returned by the `extractFlightData` function is an
* array of objects with properties such as `title`, `number`, and `playersAndAvailabilities`.
*/
function extractFlightData(titles) {
    return Array.from(titles).map((t) => ({
        name: t.value,
        number: parseInt(t.getAttribute("flight-number")),
        players_and_availabilities: [],
    }));
}

/**
* @description This function takes a HTML table and a flight number as input and
* extracts the player data from the table based on the given flight number.
* 
* @param { any } table - The `table` input parameter is passed a reference to the
* HTML table element that contains the player data.
* 
* @param { string } flightNumber - The `flightNumber` input parameter filters the
* rows to only include those with a matching flight number.
* 
* @returns { object } The `extractPlayerData` function takes a table and a flight
* number as input and returns an array of objects containing information about the
* players on that flight. Each object contains two properties: `name` (the player's
* name) and `availability` (the player's availability for that flight). The function
* filters the table rows to only include rows with a class of "player-row", then
* maps over those rows to extract the name and availability information.
*/
function extractPlayerData(table, flightNumber) {
    return Array.from(table.rows)
        .filter((row) => row.classList.contains("player-row"))
        .map((row) => ({
            name: row.cells[1].innerHTML,
            availability: Array.from(row.cells)
                .filter((cell) => cell.classList.contains("availability"))
                .map((cell) => parseInt(cell.getAttribute("availability"))),
        }));
}


/**
* @description This function takes a `data` object as input and logs it to the
* console. It then checks if the status is "success" and there's a redirect URL.
* 
* @param { object } data - The `data` input parameter receives and logs the flight
* booking response data from the server to the console for debugging purposes.
* 
* @returns { object } This function takes a `data` object as an argument and logs
* it to the console. It then checks if the `status` property of the `data` object
* is equal to `'success'` and if there is a `redirect_url` property. If both conditions
* are true`, it sets the URL of the web page to the value of the `redirect_url`
* property using `window.location.href`. otherwise.
*/
function sentCleanFlightNext(data) {
    console.log(data);

    // Check if the status is 'success' and there's a redirect URL
    if (data.status === 'success' && data.redirect_url) {
        // Redirect to the URL provided by the server
        window.location.href = data.redirect_url;
    } else {
        // Handle other statuses or lack of redirect URL
        console.log("No redirection or handling other statuses.");
    }
}


/**
* @description This function takes a list of HTML tables with flight information and
* cleans the data by extracting the time slots and player availabilities.
* 
* @returns { object } Based on the code provided:
* 
* The output of this function is an object named "league" that has several properties:
* 
* 	- "timeslots": An array of cleaned time slots extracted from the first table element
* 	- "flights": An array of flight data objects
* 	- "players_and_availabilities": An array of player and availability objects for
* each flight
* 	- "cleaned": A string indicating whether the data has been cleaned (true) or not
* (false)
* 	- "name": A string with the name of the league
* 	- "type": A string with the type of the league
* 	- "game_duration": A float with the duration of the game (1.5 hours)
* 
* Note that the function also sends the cleaned data to a server using the "sendToServer"
* function and the "sentCleanFlightNext" callback.
*/
function convertCleanFlightsToJSONAndSend() {
    const tables = document.querySelectorAll(".cleaned-flight");
    const titles = document.querySelectorAll(".flight-title");
    let league = {};

    if (tables.length != 0) {
        league.timeslots = getCleanTimeSlots(tables[0]);
    }

    league.flights = titles.length != 0 ? extractFlightData(titles) : [];

    league.flights.forEach((flight) => {
        tables.forEach((table) => {
            if (table.id === `flight-${flight.number}`) {
                flight.players_and_availabilities = extractPlayerData(table, flight.number);
            }
        });
    });
    league.cleaned = "true";
    league.name = document.getElementById("league-name-input").value;
    if (league.name.length == 0) {
        league.name = "New League"
    }
    league.type = document.getElementById("league-type-input").value;
    league.game_duration = parseFloat(document.getElementById("game-duration-slider").value)/60.0;
    sendToServer(league, sentCleanFlightNext);
}

/**
 * @description This function sends a POST request to the server with the given `data`
 * parameter. It includes the CSRF token and sets up a promise chain to handle the
 * response from the server. If the response is not successful (200 OK), it rejects
 * the promise with the status message.
 *
 * @param { object } data - The `data` input parameter is passed as the request body
 * to the server when making a POST request.
 *
 * @returns { object } Based on the code provided the function sendToServer accepts
 * a parameter "data" and makes an asynchronous GET or POST request to the server.
 * The server response JSON data that can contain the "status", and other properties
 * of data such as "data".
 *
 * When successful it returns with data including 'status'.  Therefore output is
 * returned by this function with two cases; one if status=success console.logs ("Data
 * successfully ingested by the server"); if the return has failed an error message
 * of (server failure); or shows server did not provide a proper success status as
 * such the only known response it has no 'data' which the developer expects. This
 * can either produce no output or errors.
 */
function sendToServer(data, next) {
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
                next(data);
            } else {
                console.log("Failure: ", data.error);
            }
        })
        .catch((error) => console.log("Fetch error: ", error));
}
