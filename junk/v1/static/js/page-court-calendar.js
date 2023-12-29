document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    var calendarData = calendarEl.dataset.calendarData; // Access the data from the dataset attribute
    // console.log(calendarData);
    var events = [];
    if (calendarData) {
        events = JSON.parse(calendarData);
    }
    var calendar = new FullCalendar.Calendar(calendarEl, {
        height: "auto",
        initialView: "dayGridMonth",
        events: events,
    });
    calendar.render();
});