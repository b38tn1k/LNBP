let colorColumns = true;

function getCellsInColumn(headerCell) {
    // Get the table containing the header cell
    let table = headerCell.closest('table');

    // Get the index of the header cell within its row
    let columnIndex = Array.from(headerCell.parentElement.children).indexOf(headerCell);

    // Array to store the cells in the column
    let columnCells = [];

    // Traverse the rows and get the cell at the specified column index
    for (let row of table.rows) {
        let cell = row.cells[columnIndex];
        if (cell) {
            columnCells.push(cell);
        }
    }

    return columnCells;
}


function doScheduleLegend(p, f) {
    let table = getFlightTable(f);
    let timeslots = table.querySelectorAll(".timeslot_header");
    let playerAttributeTag = `player-${p}`;

    timeslots.forEach((ts, index) => {
        let availability = ts.getAttribute(playerAttributeTag);
        if (availability == 1) {
            ts.classList.add("bg-free");
        } else if (availability == 2) {
            ts.classList.add("bg-busy");
        } else {
            ts.classList.add("bg-unavailable");
        }

        if (colorColumns) {
            // Apply the same class to the entire column
            let columnCells = getCellsInColumn(ts);
            columnCells.forEach((cell) => {
                if (availability == FREE) {
                    cell.classList.add("bg-free");
                } else if (availability == BUSY) {
                    cell.classList.add("bg-busy");
                } else {
                    cell.classList.add("bg-unavailable");
                }
            });
        }
    });
}

function resetScheduleLegend() {
    let tables = getAllFlightTables();
    tables.forEach((t, i) => {
        t.querySelectorAll(".timeslot_header").forEach((h, j) => {
            h.classList.remove("bg-free", "bg-busy", "bg-unavailable");

            if (colorColumns) {
                // Remove the same class from the entire column
                let columnCells = getCellsInColumn(h);
                columnCells.forEach((cell) => {
                    cell.classList.remove("bg-free", "bg-busy", "bg-unavailable");
                });
            }
        });
    });
}
