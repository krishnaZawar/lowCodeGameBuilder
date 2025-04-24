Writing games using libraries is a great of starting game development, but, the difficulty increases very fast while doing so, like:
1. file structure for easier management
2. implementing physics according to the game needs
3. detecting and resolving collisions just using the math

The code written can sometimes be difficult to understand for beginners while simultaneously understanding screen functionalities, draw functions to display the output, handling events, etc.
To make game development more understandable and easier, We have written a language to reduce one's development effort while creating fun and interactive games.
This language is currently suitable to create only 2D games.

# How to Use
To create fun and interactive games on our language, follow these simple steps:
1. write your program and save it in "testFile.txt" provided.
2. Run the main file
3. Enjoy playing your very own game!

# Language Documentation
## code structure
Any program written should follow the given structure:
```
initGame;
	# game logic
endGame;
```
## data types
The language is statically typed language. It allows you to create objects of 3 types, namely:
	1. integer
	2. string
	3. game object
They are declared as follows:
```
integer var_name = value;
string var_name = "value";
gameObject object = GameObject(x, y, w, h, r, g, b); # all are integer values
```

## constructs
### conditionals
The language can evaluate if-else-if blocks, just like any other language.
Some changes are:
1. use of keyword "and" and "or" as logical operators.
2. condition follows structure "value relationalOperator value".
### loops
The language can evaluate while loop. Condition should follow the same structure as in if-else-if blocks. "break" and "continue" statements are also implemented.
## Screen Related functions
1. initWindow(w, h) : initializes and displays the window of size (w, h).
2. setWindowTitle(newTitle) : changes the window title to newTitle.
3. setBackgroundColor(r, g, b) : changes the background color to (r, g, b).
4. show() : to update the changes made to the screen.
```
initWindow(1000, 800); # creates a window of size (1000 X 800) pixles
setWindowTitle("my first game");
setBackgroundColor(255, 255, 255); # changes window background to white
show();
```
<b>Note: if initWindow is not called,  the screen won't be visible.</b>

## game object related functions
1. draw(gameObject) : draws the gameObject to the screen.
2. moveX(gameObject, moveDist) : moves gameObject moveDist pixels on the X-axis.
3. moveY(gameObject, moveDist) : moves gameObject moveDist pixels on the Y-axis.
4. getX(gameObject) : returns the x-position of the gameObject.
5. getY(gameObject) : returns the y-position of the gameObject.
```
gameObject player = GameObject(10, 20, 100, 100, 255, 0, 0);
draw(player); # draws the player on the screen.
getY(player); # returns 20
getX(player); # returns 10
moveX(player, 10); # moves player 10 pixels to the right on the x-axis
moveY(player, -10); # moves player 10 pixels upward on the y-axis
```
Note:

## keyboard functions
1. keyDown(value) : returns 1 if key is pressed else 0.
```
keyDown("w");
keyDown("enter");
keyDown("space");
keyDown("0");
keyDown("upArrow);
```
## collision related functions
1. checkCollision(gameObject, gameObject) : returns 1 if both collide else 0;
example 1:
```
gameObject a = GameObject(10, 10, 10, 10, 0, 0, 0);
gameObject b = GameObject(10, 1, 10, 10, 0, 0, 0);
checkCollision(a, b); # returns 1
```
example 2:
```
gameObject a = GameObject(10, 10, 10, 10, 0, 0, 0);
gameObject b = GameObject(10, 0, 10, 10, 0, 0, 0);
checkCollision(a, b); # returns 0
```

# Flappy bird 
This a program to create flappy bird on our language:
```
initGame;
initWindow(800, 600);
setWindowTitle("Flappy Bird");
setBackgroundColor(135, 206, 235);
gameObject bird = GameObject(100, 300, 30, 30, 255, 255, 0);
gameObject ground = GameObject(0, 550, 800, 50, 139, 69, 19);
gameObject topPipe1 = GameObject(600, 0, 60, 200, 0, 200, 0);
gameObject bottomPipe1 = GameObject(600, 350, 60, 250, 0, 200, 0);
gameObject topPipe2 = GameObject(900, 0, 60, 150, 0, 200, 0);
gameObject bottomPipe2 = GameObject(900, 300, 60, 300, 0, 200, 0);
integer running = 1;
integer gameStarted = 0;
integer score = 0;
integer gravity = 1;
integer velocity = 0;
integer pipeSpeed = 2;
integer jumpStrength = -8;
integer pipe1Passed = 0;
integer pipe2Passed = 0;
integer gap = 0;
integer topHeight = 0;
while (running == 1) {
    setBackgroundColor(135, 206, 235);
    if (gameStarted == 0 and keyDown("space") == 1) {
        gameStarted = 1;
        velocity = jumpStrength;
    }
    if (gameStarted == 1) {
        velocity = velocity + gravity;
        moveY(bird, velocity);
        moveX(topPipe1, -pipeSpeed);
        moveX(bottomPipe1, -pipeSpeed);
        moveX(topPipe2, -pipeSpeed);
        moveX(bottomPipe2, -pipeSpeed);
        if (getX(topPipe1) < -60) {
            gap = 150;
            topHeight = 150;
            topPipe1 = GameObject(800, 0, 60, topHeight, 0, 200, 0);
            bottomPipe1 = GameObject(800, topHeight + gap, 60, 550 - topHeight - gap, 0, 200, 0);
            pipe1Passed = 0;
        }
        if (getX(topPipe2) < -60) {
            gap = 150;
            topHeight = 200;
            topPipe2 = GameObject(800, 0, 60, topHeight, 0, 200, 0);
            bottomPipe2 = GameObject(800, topHeight + gap, 60, 550 - topHeight - gap, 0, 200, 0);
            pipe2Passed = 0;
        }
        if (keyDown("space") == 1) {
            velocity = jumpStrength;
        }
        if (checkCollision(bird, ground) == 1 or 
            checkCollision(bird, topPipe1) == 1 or 
            checkCollision(bird, bottomPipe1) == 1 or 
            checkCollision(bird, topPipe2) == 1 or 
            checkCollision(bird, bottomPipe2) == 1) {
            running = 0;
        }
        if (getY(bird) < 0) {
            moveY(bird, 2);
            velocity = 2;
        }
    }
    draw(ground);
    draw(topPipe1);
    draw(bottomPipe1);
    draw(topPipe2);
    draw(bottomPipe2);
    draw(bird);
    show();  
}
endGame;
```