/**
* @description The `searchPlayers` function searches through a table of rows, hides 
* those that don't match the input search value, and displays only those that contain 
* the searched value in the first column's text content.
*/
function searchPlayers() {
    // Get the search input value
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("player-search-input");
    filter = input.value.toLowerCase();
    table = document.getElementById("player-table-body");
    tr = table.getElementsByTagName("tr");
    // Loop through all table rows and hide those that don't match the search input
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; // Assuming the name is in the first column
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Attach an event listener to the search input to trigger the search on input change
document.getElementById("player-search-input").addEventListener("input", searchPlayers);
