new p5(function (bgSketch) {
    let shapes = [];

    class Shape {
/**
* @description The provided constructor function initializes object properties: `x`, 
* `y`, `size`, and `color` with the passed arguments, while randomly setting the 
* `speedX` and `speedY` properties within a defined range using `bgSketch.random()`.
* 
* @param { number } x - SETS x PARAMETER TO VALUE GIVEN
* 
* @param { number } y - SETS `this.y`.
* 
* @param { number } size - The `size` input parameter sets the size of the object.
* 
* @param { string } color - The `color` input parameter sets the color of the object.
*/
        constructor(x, y, size, color) {
            this.x = x;
            this.y = y;
            this.size = size;
            this.color = color;
            this.speedX = bgSketch.random(-0.5, 0.5);
            this.speedY = bgSketch.random(-0.5, 0.5);
            this.collisionCooldown = false;
        }

/**
* @description The `update()` function constrains the speed of a shape to a valid 
* range, moves it based on its speed, bounces it off the edges of the background 
* sketch, and detects collisions with other shapes.
*/
        update() {
            this.speedX = bgSketch.constrain(this.speedX, -0.5, 0.5);
            this.speedY = bgSketch.constrain(this.speedY, -0.5, 0.5);
            // Move the shape
            this.x += this.speedX;
            this.y += this.speedY;

            // Bounce off the edges
            if (this.x < 0 || this.x > bgSketch.width) {
                this.speedX *= -1;
            }
            if (this.y < 0 || this.y > bgSketch.height) {
                this.speedY *= -1;
            }

            // Collision detection with other shapes
            if (!this.collisionCooldown) {
                for (let i = 0; i < shapes.length; i++) {
                    const other = shapes[i];
                    if (other !== this) {
                        const dx = other.x - this.x;
                        const dy = other.y - this.y;
                        const distance = bgSketch.sqrt(dx * dx + dy * dy);
                        const minDistance = (this.size + other.size) / 2;

                        if (distance < minDistance) {
                            // Shapes have collided, adjust speeds
                            const angle = bgSketch.atan2(dy, dx);
                            const targetX = this.x + bgSketch.cos(angle) * minDistance;
                            const targetY = this.y + bgSketch.sin(angle) * minDistance;
                            const ax = (targetX - other.x) * 0.01;
                            const ay = (targetY - other.y) * 0.01;

                            this.speedX -= ax;
                            this.speedY -= ay;
                            other.speedX += ax;
                            other.speedY += ay;
                            this.collisionCooldown = true;
                            setTimeout(() => {
                                this.collisionCooldown = false;
                            }, 500);
                        }
                    }
                }
            }
        }

/**
* @description This function draws an ellipse on the canvas using the given color 
* and size.
*/
        display() {
            // Draw the shape
            bgSketch.noStroke();
            bgSketch.fill(this.color);
            bgSketch.ellipse(this.x, this.y, this.size);
        }
    }

/**
* @description The function "setupScreen" prepares the background of a graphics 
* window by setting the random seed for drawing shapes, creating a canvas element 
* with specific dimensions and styles, and defining some colors.
*/
    function setupScreen() {
        bgSketch.randomSeed(Date.now());
        const cnv = bgSketch.createCanvas(bgSketch.windowWidth, bgSketch.windowHeight);
        cnv.style("user-select", "none");
        cnv.style("-webkit-user-select", "none");
        cnv.style("-moz-user-select", "none");
        cnv.style("-ms-user-select", "none");
        cnv.id("p5JsBG");
        bgSketch.frameRate(60);
        let colors = [];
        colors.push(bgSketch.color(179, 204, 102, 100)); // Light Yellow-Green (75% opacity)
        colors.push(bgSketch.color(153, 179, 77, 100)); // Medium Yellow-Green (75% opacity)
        colors.push(bgSketch.color(128, 153, 51, 100)); // Dark Yellow-Green (75% opacity)

        if (shapes.length < 20) {
            // Create initial shapes
            let tries = 0;
            while (shapes.length < 20 && tries < 100) {
                const x = bgSketch.random(bgSketch.width);
                const y = bgSketch.random(bgSketch.height);
                const size = bgSketch.random(50, 200);
                const c = bgSketch.random(colors);

                let isCollision = false;
                for (let i = 0; i < shapes.length; i++) {
                    const other = shapes[i];
                    const dx = other.x - x;
                    const dy = other.y - y;
                    const distance = bgSketch.sqrt(dx * dx + dy * dy);
                    const minDistance = size + other.size + 50;
                    if (distance < minDistance) {
                        isCollision = true;
                        break;
                    }
                }

                if (!isCollision) {
                    shapes.push(new Shape(x, y, size, c));
                }

                tries++;
            }
        }
    }

    bgSketch.setup = function () {
        setupScreen();
    };

    bgSketch.deviceTurned = function () {
        setupScreen();
    };

    bgSketch.windowResized = function () {
        setupScreen();
    };

    bgSketch.draw = function () {
        bgSketch.clear();
        // Update and display shapes
        for (let i = 0; i < shapes.length; i++) {
            const shape = shapes[i];

            shape.update();
            shape.display();
        }
    };
});
