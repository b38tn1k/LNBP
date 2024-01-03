/**
 * @description This function sets up drag and drop functionality for a list of items
 * using the Dragula library.
 */
function setupDragula() {
    var drake = dragula({
        isContainer: isDraggableTarget,
        moves: isDraggableItem,
        copy: isDraggableSource,
        accepts: canAcceptDrop,
        removeOnSpill: true,
    });

    drake.on("drag", handleDrag);
    drake.on("drop", handleDrop);
    drake.on("dragend", handleDragEnd);
    drake.on("cancel", handleDragCancel);
}

/**
 * @description This function checks if the passed element `el` has the class `draggable-target`.
 *
 * @param {  } el - In the function `isDraggableTarget(el)`, `el` is a reference to
 * an Element object representing the DOM element being tested for draggability.
 *
 * @returns { boolean } The output returned by this function is `false`.
 */
function isDraggableTarget(el) {
    return el.classList.contains("draggable-target");
}

/**
 * @description This function checks if an element is a draggable item by checking
 * if it has the class "draggable-item".
 *
 * @param {  } el - The `el` input parameter is the element being checked for draggability.
 *
 * @param { object } source - The `source` input parameter is not used at all because
 * it is defined as `undefined`.
 *
 * @param {  } handle - The `handle` parameter is passed to the `getElementById()`
 * method within the function. This means that the handle serves as an identifier for
 * the element on which to look for the draggable class.
 *
 * @param { object } sibling - The `sibling` parameter is not used inside the
 * `isDraggableItem` function.
 *
 * @returns { boolean } The output returned by this function is `true` if the element
 * passed as `el` has a class list containing "draggable-item", and `false` otherwise.
 */
function isDraggableItem(el, source, handle, sibling) {
    return el.classList.contains("draggable-item");
}

/**
 * @description The provided function `isDraggableSource` checks if an HTML element
 * `el` has a closest parent element with the class `draggable-source`.
 *
 * @param { object } el - The `el` input parameter is not used inside the function `isDraggableSource`.
 *
 * @param {  } source - The `source` input parameter inside the `isDraggableSource()`
 * function refers to the element that triggerd the drag event.
 *
 * @returns { boolean } The function `isDraggableSource` takes two arguments `el` and
 * `source`, and returns a boolean value indicating whether the element `source` is
 * a direct child of an element with the class `draggable-source`.
 *
 * The output returned by this function is simply a boolean value (either `true` or
 * `false`).
 */
function isDraggableSource(el, source) {
    return source.closest(".draggable-source") !== null;
}

/**
 * @description This function does nothing.
 *
 * @param {  } el - In the provided function `canAcceptDrop`, the `el` parameter
 * represents the Element being dragged over the drop zone (target).
 *
 * @param { object } target - The `target` input parameter specifies the element that
 * the dragged element should be dropped onto. In this function implementation shown
 * here `$(target)`, the drop target will only be allowed if it is valid and can
 * accept the dragged element being dropped onto it.
 *
 * @returns { boolean } The output returned by this function is `true`.
 */
function canAcceptDrop(el, target, source, sibling) {
    let isGameSlot = !target.classList.contains("draggable-source");
    playerID = parseInt(el.getAttribute("player-id"));
    let isInPlayerSchedule = checkAvailabilityBeforeDrop(playerID, target);
    return isGameSlot && isInPlayerSchedule;
}

/**
 * @description The given function `handleDrag(el Dragging elements or any other
 * draggable object source)` logs the message "Handle drag" to the console.
 *
 * @param { object } el - The `el` input parameter is the dragged element being handled
 * by the function.
 *
 * @param {  } source - The `source` input parameter is not used or defined within
 * the code fragment you provided.
 *
 * @returns {  } The function `handleDrag` takes two parameters `el` and `source`,
 * but the last `}}>` is missed and hence the function does not have a returning statement.
 */
function handleDrag(el, source) {
    console.log("Handle drag");
    playerID = parseInt(el.getAttribute("player-id"));
    flightID = parseInt(el.getAttribute("flight-id"));
    doScheduleLegend(playerID, flightID);
}

/**
 * @description This function handles the "drag start" event on a widget or element
 * and logs the message "Handle drag start" to the console.
 *
 * @param { object } event - The `event` input parameter passed to the `handleDragStart`
 * function is an object that contains information about the current mouse event that
 * triggered the function's execution.
 */
function handleDragStart(event) {
    // Code to handle drag start
    console.log("Handle drag start");
}

/**
 * @description This function named "handleDrop" logs the message "Handle drop" to
 * the console when the event named "drop" occurs.
 *
 * @param { object } event - The `event` input parameter passed to the `handleDrop()`
 * function is an object that contains information about the dropped file(s) or drag
 * operation.
 */
function handleDrop(el, target, source) {
    console.log("Handle drop");
    if (!target) {
        el.remove();
    } else {
        let noFreeSpace = !checkFreeSpaceBeforeDrop(el, target);
        let duplicates = !checkForNoDuplicates(playerID, target);
        if (noFreeSpace || duplicates) {
            el.remove();
        } else {
            renameRadio(el, target);
        }
    }
}

/**
 * @description This function logs the message "Handle drag end" to the console when
 * a drag event ends.
 *
 * @param {  } event - The `event` input parameter is passed to the function as an
 * argument from the event listener that triggered the function.
 */
function handleDragEnd(event) {
    // Code to handle drag end
    console.log("Handle drag end");
    resetScheduleLegend();
    let flight = parseInt(event.getAttribute("flight-id"));
    updatePlayerCards(flight);
}

/**
 * @description This function called `handleDragCancel()` when a user cancels a drag
 * gesture on an element.
 */
function handleDragCancel(el) {
    // Code to handle drag cancel
    console.log("Handle drag cancel");
    el.remove();
}
