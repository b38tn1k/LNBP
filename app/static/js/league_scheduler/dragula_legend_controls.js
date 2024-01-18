let colorColumns = true;

/**
 * @description This function takes a header cell as input and returns an array of
 * all cells found within the table that are located at the same column index as the
 * header cell.
 *
 * @param {  } headerCell - The `headerCell` input parameter is the cell that contains
 * the header text for which we want to get all the cells located below it (in the
 * same column) within the table.
 *
 * @returns { array } The `getCellsInColumn` function returns an array of cells that
 * are present at a specific column index within a table. It takes a header cell as
 * input and traverses the rows of the table to retrieve all the cells that are present
 * at the specified column index.
 */
function getCellsInColumn(headerCell) {
    // Get the table containing the header cell
    let table = headerCell.closest("table");

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

/**
 * @description This function does the following:
 *
 * 	- Retrieves a table of flights and a player attribute tag (e.g., "player-John")
 * 	- Iterates through each timeslot cell within the table
 * 	- Based on the availability of that timeslot (as indicated by a Player attribute),
 * adds a class to the cell to indicate its status (free/busy/unavailable)
 *
 * If there is color columns feature enabled (through another configuration), it also
 * applies those classes to entire column.
 *
 * @param { string } p - The `p` input parameter specifies the player for whom the
 * availability is being checked.
 *
 * @param { object } f - The `f` input parameter represents a flight schedule and is
 * used to retrieve information about availability of time slots.
 *
 * @returns { array } The output returned by this function is a collection of DOM
 * elements ( `<td>` and `<th>` ) that have had their background colors updated based
 * on the availability of the time slot they are contained within.
 */
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
                if (!cell.classList.contains("subs")) {
                    if (availability == AVAILABLE) {
                        cell.classList.add("bg-free");
                    } else if (availability == AVAILABLE_LP) {
                        cell.classList.add("bg-busy");
                    } else {
                        cell.classList.add("bg-unavailable");
                    }
                }
            });
        }
    });

    let cells = table.querySelectorAll(".draggable-target");
    cells = filterOutCellsByClass(cells, 'subs');
    cells = filterOutCellsByClass(cells, 'unavailable');
    // function that takes cells and filters out cells with 'subs' also in class list
    cells.forEach((c) => {
        let ps = c.querySelectorAll(".draggable-item");
        ps.forEach((po) => {
            if (parseInt(po.getAttribute("player-id")) == parseInt(p)) {
                c.classList.remove("bg-free", "bg-busy", "bg-unavailable", "bg-populated");
                c.classList.add("bg-populated");
                if (colorColumns) {
                    let columnCells = getCellsInColumn(c);
                    columnCells.forEach((cell) => {
                        if (!cell.classList.contains("subs")) {
                            cell.classList.remove("bg-free", "bg-busy", "bg-unavailable", "bg-populated");
                            cell.classList.add("bg-populated");
                        }
                    });
                }
            }
        });
    });
}

/**
* @description This function takes an array of cells and a class name as input and
* returns an array of cells that do not have the given class name.
* 
* @param { object } cells - The `cells` input parameter is an array of HTML cells
* (probably `td` or `th`) that the function should filter based on the `class` attribute.
* 
* @param { string } cclass - The `cclass` input parameter is a string that specifies
* the class name to filter out.
* 
* @returns { array } The function takes two arguments: `cells` which is an HTML
* collection of cells and `cclass` a string representing the class name of cells to
* filter out.
* The function returns an array of cells that do not have the `cclass` class.
* 
* In other words the function uses the `filter()` method and the `!...contains()`
* method to filter out all elements that do not have the specified class and returns
* an array of those elements.
*/
function filterOutCellsByClass(cells, cclass) {
    return Array.from(cells).filter((cell) => !cell.classList.contains(cclass));
}

/**
 * @description The function `resetScheduleLegend` resets the styles of tables used
 * to display flight information by removing all previously added CSS classes
 * (`.bg-free`, `.bg-busy`, and `.bg-unavailable`) from all header cells (`timeslot_header`)
 * within each table.
 *
 * @returns { array } The `resetScheduleLegend` function takes no arguments and returns
 * undefined.
 *
 * It iterates over all flight tables using `getAllFlightTables()` and then removes
 * any previously added CSS classes (`"bg-free", "bg-busy", "bg-unavailable"`}) from
 * the header cells of each table using `querySelectorAll(".timeslot_header")`, and
 * if `colorColumns` is true it also removes the same class from the entire column
 * using `getCellsInColumn(h)`.
 */
function resetScheduleLegend() {
    let tables = getAllFlightTables();
    tables.forEach((t, i) => {
        t.querySelectorAll(".timeslot_header").forEach((h, j) => {
            h.classList.remove("bg-free", "bg-busy", "bg-unavailable", "bg-populated");

            if (colorColumns) {
                // Remove the same class from the entire column
                let columnCells = getCellsInColumn(h);
                columnCells.forEach((cell) => {
                    cell.classList.remove("bg-free", "bg-busy", "bg-unavailable", "bg-populated");
                });
            }
        });
    });
}
