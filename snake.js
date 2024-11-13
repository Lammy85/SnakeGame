let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let rows = 20;
let cols = 20;
let snake = [{ x: 9, y: 3 }];
let food;
let cellWidth = canvas.width / cols;
let cellHeight = canvas.height / rows;
let direction = '';
let foodCollected = false;
let counter = 300;
let score = 0;
//const scoreList = [{ "username": "Test", "score": 100 }];

gameIntervall = setInterval(gameLoop, counter);
document.addEventListener('keydown', KeyDown);
document.getElementById('tutorialButton').addEventListener("click", showTutorial);
document.getElementById('playButton').addEventListener("click", closeTutorial);
document.getElementById('againButton').addEventListener("click", playAgain);
//document.getElementById('saveButton').addEventListener("click", saveScoreList);


placeFood();
draw();
getScorelist();


function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'lightgreen';

    snake.forEach(part => add(part.x, part.y));

    ctx.fillStyle = 'red';
    add(food.x, food.y);

    requestAnimationFrame(draw);
}

function testGameOver() {

    let firstPart = snake[0];
    let otherParts = snake.slice(1);
    let duplicatePart = otherParts.find(part => part.x == firstPart.x && part.y == firstPart.y)


    if (snake[0].x < 0 || snake[0].x > cols - 1 || snake[0].y < 0 || snake[0].y > rows - 1 || duplicatePart) {
        clearInterval(gameIntervall);
        document.getElementById('result').hidden = false;
        document.getElementById('canvas').hidden = true;
        document.getElementById('total').textContent = score;
    }
}

function placeFood() {
    let randomX = Math.floor(Math.random() * cols);
    let randomY = Math.floor(Math.random() * rows);

    food = { x: randomX, y: randomY };
}


function add(x, y) {
    ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth - 1, cellHeight - 1)
}

function shiftSnake() {
    for (let i = snake.length - 1; i > 0; i--) {
        const part = snake[i];
        const lastPart = snake[i - 1];
        part.x = lastPart.x;
        part.y = lastPart.y;
    }
}

function speedUp() {
    counter = counter * 0.95;
    clearInterval(gameIntervall)
    gameIntervall = setInterval(gameLoop, counter);
}

function gameLoop() {
    document.getElementById('tutorial').hidden = true;
    document.getElementById('canvas').hidden = false;
    document.getElementById('result').hidden = true;
    document.getElementById('score').textContent = score;
    testGameOver();
    if (foodCollected) {
        snake = [{ x: snake[0].x, y: snake[0].y }, ...snake];
        foodCollected = false;
        score = score + 100;
        speedUp();
    }

    shiftSnake();

    if (direction == 'LEFT') {
        snake[0].x--;
    }
    if (direction == 'RIGHT') {
        snake[0].x++;
    }
    if (direction == 'UP') {
        snake[0].y--;
    }
    if (direction == 'DOWN') {
        snake[0].y++;
    }

    if (snake[0].x == food.x && snake[0].y == food.y) {
        foodCollected = true;
        placeFood();
    }
}

function KeyDown(e) {
    if (e.keyCode == 37) {
        direction = 'LEFT';
    }
    if (e.keyCode == 38) {
        direction = 'UP';
    }
    if (e.keyCode == 39) {
        direction = 'RIGHT';
    }
    if (e.keyCode == 40) {
        direction = 'DOWN';
    }
}

function showTutorial() {
    clearInterval(gameIntervall);
    document.getElementById('tutorial').hidden = false;
    document.getElementById('canvas').hidden = true;
    document.getElementById('results').hidden = true;
}

function closeTutorial() {
    location.reload();
}

function playAgain() {
    location.reload();
}

function saveScoreList() {
    document.getElementById('username').textContent = username;
    //let scoreList = JSON.parse(localStorage.getItem("scoreList"))|| "[]";
    const scoreList = [];
    let newScore = { "username": username, "score": score };
    scoreList.push(newScore);
    localStorage.setItem("scoreList", JSON.stringify(scoreList));
    location.reload();
}

function getScorelist() {

    for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        var item = JSON.parse(localStorage.getItem(key)|| "[]");
        highscore.innerHTML += `
                <tr>
                <td><span>${item[i].username}</span></td>
                <td><span>${item[i].score}</span></td>
              </tr>                `
    };
}