/**
* @description The function "recountPlayers" updates the game count and busy scheduled
* count for each player based on the draggable items dropped on a facility timeslot
* table and the player availability for that cell.
* 
* @param { string } flight - The `flight` input parameter is used to retrieve a
* specific flight's table from the HTML structure and update the player data for
* that flight.
*/
function recountPlayers(flight) {
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
            p.busy_count += parseInt(ts.getAttribute(`player-${p.id}`)) == BUSY;
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
            targetPlayer.busy_scheduled_count += avail == BUSY;
            let radio = pi.querySelector('[type="radio"]');
            targetPlayer.captain_count += radio.checked;
        });
    });

    console.log(players);
}
