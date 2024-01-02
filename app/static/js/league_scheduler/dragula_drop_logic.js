function checkAvailabilityBeforeDrop(p, target) {
    let a = getPlayerAvailabilityForCell(p, target);
    return a == 1 || a == 2;
}

function checkFreeSpaceBeforeDrop(el, target) {
    let items = target.querySelectorAll(".draggable-item");
    return items.length <= info.leagueRulesMaxPlayersPerMatch;
}

function checkForNoDuplicates(p, target) {
    let c = getFullColumn(target);
    let count = 0;
    c.forEach((cell) => {
        let items = cell.querySelectorAll(`.draggable-item[player-id="${p}"]`);
        count += items.length;
    });
    return count <= 1;
}

