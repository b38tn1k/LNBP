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
            captainCount.src = info.captain_warning.src;
        } else {
            captainCount.src = info.captainChecked.src;
        }
    });
}

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
