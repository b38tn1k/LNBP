/**
* @description This function updates the player cards on a webpage based on the
* information from a flight table. It calculates and displays the number of games
* and captain counts for each player and checks if they have satisfied the league
* rules for minimum games played or captained.
* 
* @param { object } flight - The `flight` input parameter retrieves information from
* the HTML tables for players and passes it to an anonymous function to update
* players' card data. The information retrieved includes player IDs for flight
* scheduling on available facilities with potential opponents; flight is defined but
* empty (""), which means nothing has yet been retrieved—a "flight." It is up to the
* application using this code snippet not the user who makes an attempt to call it
* with valid content like another JavaScript method's result or direct input (i.e.,
* not through the page DOM) rather than being left unchanged by allowing defaults
* within <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arrow_functions>
* an arrow function does nothing since there isn't anything passed through when
* flight == null—since undefined arguments cause issues upon invocation when relying
* only onto global 'this'. Instead an immediately invoked anonymous self invocation
* IIFE inside each arrow() works best like so IIFEs within then(): () => { return }
* ();  which helps set local 'this.x = x', and does work well. As always review any
* third-party provided functions including window to help improve functionality
* especially considering this isn't a native DOM property like those available when
* accessing window.matchMedia(). If true arguments aren't being ignored either IIFE
* could reassign IIFEs' variables after IIFE completion because their returned value
* wouldn't apply globally within immediate anonymous function(ii) if not declared
* using let but instead hoisted variable at its place using 'const'(no initializationchk
* or var ident).
* 
* @returns {  } The `updatePlayerCards` function takes a flight as input and updates
* the player cards on the page based on the available games for each player.
*/
function updatePlayerCards(flight) {
    let table = getFlightTable(flight);
    let playerFlightSource = document.querySelector(`.player-flight-source[flight-id="${flight}"]`);
    let player_cards = playerFlightSource.querySelectorAll(".player-card");
    players = [];
    player_cards.forEach((p, i) => {
        players.push({
            id: parseInt(p.getAttribute("player-id")),
            captain_count: 0,
            game_count: 0,
            busy_count: 0,
            busy_scheduled_count: 0,
        });
    });
    let timeslots = table.querySelectorAll(".timeslot_header");
    timeslots.forEach((ts, i) => {
        for (let p of players) {
            p.busy_count += parseInt(ts.getAttribute(`player-${p.id}`)) == AVAILABLE_LP;
        }
    });
    let possible_game = table.querySelectorAll(".facility-timeslot");
    possible_game.forEach((pg) => {
        playerItems = pg.querySelectorAll(".draggable-item");

        playerItems.forEach((pi) => {
            let pid = parseInt(pi.getAttribute("player-id"));
            let targetPlayer = players.find((player) => player.id === pid);
            targetPlayer.game_count += 1;
            let avail = getPlayerAvailabilityForCell(pid, pg);
            targetPlayer.busy_scheduled_count += avail == AVAILABLE_LP;
            let radio = pi.querySelector('[type="radio"]');
            targetPlayer.captain_count += radio.checked;
        });
    });
    player_cards.forEach((pc) => {
        pid = parseInt(pc.getAttribute("player-id"));
        let targetPlayer = players.find((player) => player.id === pid);
        pc.querySelector(".player-game-count").innerHTML = targetPlayer.game_count;
        pc.querySelector(".player-captain-count").innerHTML = targetPlayer.captain_count;
        let gc = (pc.querySelector(
            ".player-badtimeslot-count"
        ).innerHTML = `${targetPlayer.busy_scheduled_count}/${targetPlayer.busy_count}`);

        const gameCount = pc.querySelector(".game-count-icon").querySelector("img");
        const captainCount = pc.querySelector(".captain-count-icon").querySelector("img");
        const lowPreferenceCount = pc.querySelector(".low-preference-count-icon").querySelector("img");
        if (
            targetPlayer.game_count < info.leagueRulesMinGamesTotal ||
            targetPlayer.game_count > info.leagueRulesMaxGamesTotal
        ) {
            gameCount.src = info.tennisRacketWarning.src;
        } else {
            gameCount.src = info.tennisRacket.src;
        }

        if (targetPlayer.lowPreferenceCount > info.leagueRulesMinGamesTotal / 2) {
            lowPreferenceCount.src = info.faceNeutralWarning.src;
        } else {
            lowPreferenceCount.src = info.faceNeutral.src;
        }
        if (targetPlayer.captain_count < info.leagueRulesMinCaptained) {
            captainCount.src = info.captainUnchecked.src;
        } else if (targetPlayer.captain_count > info.leagueRulesMaxCaptained) {
            captainCount.src = info.captainWarning.src;
        } else {
            captainCount.src = info.captainChecked.src;
        }
    });
}

/**
* @description This function generates a random hexadecimal string of the given
* length by picking a character from a predefined set of characters
* "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" and concatenating
* them together to create a random hash.
* 
* @param { number } length - The `length` input parameter specifies the desired
* length of the generated hash string.
* 
* @returns { string } The function `generateRandomHash(length)` takes an integer
* parameter `length` and returns a string of length `length` composed of random
* characters from the alphabet defined by "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".
*/
function generateRandomHash(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    const charactersLength = characters.length;
    let hash = "";

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charactersLength);
        hash += characters.charAt(randomIndex);
    }

    return hash;
}

/**
* @description This function renames a group of radio buttons and their corresponding
* labels by generating a new random hash value and assigning it to the radio button's
* ID and the label's htmlFor attribute. It also updates the name attribute of all
* radio buttons within the target element to a new name that includes the facilityID
* and timeslot parameters.
* 
* @param { object } el - The `el` input parameter is the element that the radio
* button(s) are located within.
* 
* @param {  } target - The `target` parameter is an HTML element that is being
* processed by the renaming functionality of the function.
* 
* @returns { any } The function `renameRadio` takes two parameters: `el` and `target`.
* It updates the `id`, `disabled`, `checked`, and `name` attributes of all radio
* buttons within the element `target`, and adds an event listener to each radio
* button to call a callback function named `captainRadioClickCallback`.
* 
* The output returned by this function is not specified explicitly since it does not
* return any value.
*/
function renameRadio(el, target) {
    let radioCopy = el.querySelector('[type="radio"]');
    let labelCopy = el.querySelector("label");
    radioCopy.disabled = false;
    radioCopy.checked = false;
    let newHash = generateRandomHash(10);
    radioCopy.id = newHash;
    labelCopy.htmlFor = newHash;
    let newName = target.getAttribute("facility") + target.getAttribute("timeslot") + target.getAttribute("flight");
    let radios = target.querySelectorAll('[type="radio"]');
    radios.forEach((radio) => {
        radio.name = newName;
    });

    radios.forEach((radio) => {
        radio.addEventListener("click", captainRadioClickCallback);
    });
}
