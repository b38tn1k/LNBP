var info;

class InfoClass {
    constructor() {
        // Get the info div element by its class name
        this.infoDiv = document.querySelector('.info');

        // Check if the info div exists
        if (this.infoDiv) {
            // Extract attributes and set them as class properties
            this.captainChecked = this.infoDiv.getAttribute('captain_checked');
            this.captainUnchecked = this.infoDiv.getAttribute('captain_unchecked');
            // Add more attributes as needed
        } else {
            console.error('Info div not found.');
        }
    }
}


document.addEventListener("DOMContentLoaded", function () {
    info = new InfoClass();
});
