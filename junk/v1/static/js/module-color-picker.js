let bgColorPicker = document.getElementById("bgcolor-picker");
let fgColorPicker = document.getElementById("fgcolor-picker");
let displayBox = document.getElementById("color-preview");
let svg = document.querySelector("svg");
let rButton = document.getElementById("random-button");
let endpoint = document.currentScript.getAttribute("endpoint");

// Function to update the display box colors
/**
* @description The `updateColors()` function sends the background and foreground 
* color values selected from the respective pickers to be updated.
*/
function updateColors() {
    sendColorsAndUpdate(bgColorPicker.value, fgColorPicker.value);
}

/**
* @description This function sets the background and foreground colors of an HTML 
* element using color pickers, updates the preview box, and sends the colors to an 
* endpoint via fetch API.
* 
* @param { string } bgColor - The `bgColor` input parameter sets the background color 
* of the display box.
* 
* @param { string } fgColor - The `fgColor` input parameter sets the foreground color 
* of the preview box, SVG, and buttons.
*/
function sendColorsAndUpdate(bgColor, fgColor) {
    // Set the colors in the color pickers and the preview box
    bgColorPicker.value = bgColor;
    fgColorPicker.value = fgColor;
    displayBox.style.backgroundColor = bgColor;
    displayBox.style.color = fgColor;
    rButton.style.backgroundColor = bgColor;
    svg.style.color = fgColor;
    fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'fgcolor=' + encodeURIComponent(fgColor) + '&bgcolor=' + encodeURIComponent(bgColor)
      })
}

/**
* @description The `randomColors` function generates two random RGB colors with a 
* hue relationship (complementary, split-complementary, or analogous) based on a 
* random value, and sends them to an update function in hexadecimal format.
*/
function randomColors() {
    // Generate a random hue (0-1)
    let hue = Math.random();

    // Randomly choose a color relationship: complementary, split-complementary, or analogous
    let offset;
    let rand = Math.random();
    if (rand < 0.5) {
        offset = 0.5; // complementary
    } else {
        offset = 0.4; // split-complementary
    }

    // Generate the related hue
    let relatedHue = (hue + offset) % 1;

    // Convert the hues to RGB colors
    let saturation = Math.random() * 0.5 + 0.5;
    let value = 1;

    let bgColor = HSVtoRGB(hue, saturation, value);
    let fgColor = HSVtoRGB(relatedHue, saturation, value);
    sendColorsAndUpdate(RGBtoHex(bgColor), RGBtoHex(fgColor))
}

// Convert HSV to RGB
// h, s, v are from 0-1
/**
* @description This function HSVtoRGB converts an RGB color represented as hue (h), 
* saturation (s), and value (v) to its equivalent RGB representation using a switching 
* statement based on the floor of h modulo 6.
* 
* @param { number } h - The `h` input parameter represents the hue value in the HSV 
* color model, and it is used to determine the appropriate combination of red, green, 
* and blue colors that will be returned by the function.
* 
* @param { number } s - The `s` input parameter in the `HSVtoRGB` function represents 
* the saturation level of the HSV color model. It ranges from 0 (completely desaturated) 
* to 1 (completely saturated).
* 
* @param { number } v - The `v` input parameter determines the brightness of the 
* resulting RGB color.
* 
* @returns { object } - The `HSVtoRGB` function takes an hue (h), saturation (s), 
* and value (v) as input and returns an object with three properties: `r`, `g`, and 
* `b`. These properties represent the corresponding Red, Green, and Blue values of 
* the resulting RGB color, which are calculated based on the given HSV values using 
* a switching formula.
*/
function HSVtoRGB(h, s, v) {
    let r, g, b, i, f, p, q, t;
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0:
            (r = v), (g = t), (b = p);
            break;
        case 1:
            (r = q), (g = v), (b = p);
            break;
        case 2:
            (r = p), (g = v), (b = t);
            break;
        case 3:
            (r = p), (g = q), (b = v);
            break;
        case 4:
            (r = t), (g = p), (b = v);
            break;
        case 5:
            (r = v), (g = p), (b = q);
            break;
    }
    return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

// Convert RGB to Hex
/**
* @description The `RGBtoHex` function converts a ` Color ` object to a hexadecimal 
* string.
* 
* @param c - The `c` input parameter represents a color object and is used as the 
* source for the hexadecimal representation returned by the function.
* 
* @returns { string } - The function RGBtoHex takes a color object (c) as input and 
* returns a string representing the RGB value in hexadecimal format, prefixed with 
* a "#" symbol.
*/
function RGBtoHex(c) {
    let hex = c.r.toString(16).padStart(2, "0") + c.g.toString(16).padStart(2, "0") + c.b.toString(16).padStart(2, "0");
    return "#" + hex;
}

// Add event listeners to the color pickers
bgColorPicker.addEventListener("input", updateColors);
fgColorPicker.addEventListener("input", updateColors);

// Initialize colors
updateColors();
