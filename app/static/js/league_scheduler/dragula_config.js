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

function handleDragStart(event) {
    // Code to handle drag start
    console.log("Handle drag start");
}

function handleDrop(event) {
    // Code to handle drop
    console.log("Handle drop");
}

function handleDragEnd(event) {
    // Code to handle drag end
    console.log("Handle drag end");
}

function handleDragCancel() {
    // Code to handle drag cancel
    console.log("Handle drag cancel");
}