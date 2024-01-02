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
    });

    drake.on("drag", handleDrag);
    drake.on("drop", handleDrop);
    drake.on("dragend", handleDragEnd);
    drake.on("cancel", handleDragCancel);
}

document.addEventListener("DOMContentLoaded", function () {
    setupDragula();
});

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
function handleDrop(event) {
    // Code to handle drop
    console.log("Handle drop");
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
}

/**
* @description This function called `handleDragCancel()` when a user cancels a drag
* gesture on an element.
*/
function handleDragCancel() {
    // Code to handle drag cancel
    console.log("Handle drag cancel");
}