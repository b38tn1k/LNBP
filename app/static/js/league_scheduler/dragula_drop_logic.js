/**
* @description The `checkAvailabilityBeforeDrop` function checks whether a player
* can drop an item on a specific target cell based on the player's availability.
* 
* @param {  } p - The `p` input parameter is the player whose availability is being
* checked for the specified `target` cell.
* 
* @param { number } target - The `target` parameter is a cell that the player
* (represented by `p`) can be moved to.
* 
* @returns { boolean } Based on the code provided:
* 
* The output of `checkAvailabilityBeforeDrop` function will be either `true` or
* `false`, depending on the availability of the player's character for the given `target`.
*/
function checkAvailabilityBeforeDrop(p, target) {
    let a = getPlayerAvailabilityForCell(p, target);
    return a == 1 || a == 2;
}

/**
* @description The `checkFreeSpaceBeforeDrop` function checks whether there are
* already too many draggable items on the target element before allowing a new item
* to be dropped onto it.
* 
* @param { object } el - The `el` input parameter is not used or referred to anywhere
* within the `checkFreeSpaceBeforeDrop` function.
* 
* @param { object } target - The `target` input parameter represents the drop target
* element where the dragged item will be dropped.
* 
* @returns { boolean } The function `checkFreeSpaceBeforeDrop` takes two arguments:
* `el` and `target`. It returns a boolean value indicating whether there is enough
* space to drop the dragged element (represented by `el`) into the target container
* (represented by `target`).
*/
function checkFreeSpaceBeforeDrop(el, target) {
    let items = target.querySelectorAll(".draggable-item");
    return items.length <= info.leagueRulesPlayersPerMatch;
}

/**
* @description This function checks whether there are no duplicate draggable items
* with the same player ID as the provided `p` value within the elements targeted by
* the `target` parameter. It does so by iterating through each row of cells and
* counting the number of draggable items with the specified player ID.
* 
* @param { string } p - The `p` input parameter is used to pass the player ID as a
* parameter to the function.
* 
* @param {  } target - The `target` input parameter is the HTML table row or column
* being checked for duplicate elements.
* 
* @returns { object } The function `checkForNoDuplicates` takes two arguments `p`
* and `target`. It returns a boolean value indicating whether there are no duplicates
* of the element with the given `player-id` (i.e., `p`) within the given target HTML
* Element.
* 
* In simpler terms: it checks if there is only one element with the specified
* `player-id` inside the target HTML element.
*/
function checkForNoDuplicates(p, target) {
    let c = getFullColumn(target);
    let count = 0;
    c.forEach((cell) => {
        let items = cell.querySelectorAll(`.draggable-item[player-id="${p}"]`);
        count += items.length;
    });
    return count <= 1;
}

