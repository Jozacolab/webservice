const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const box = 20;
let snake = [{x: 9 * box, y: 10 * box}];
let direction = 'RIGHT';
let food = {
    x: Math.floor(Math.random() * 20) * box,
    y: Math.floor(Math.random() * 20) * box
};
let score = 0;

// Controle via teclado
document.addEventListener('keydown', event => {
    if(event.key === "ArrowLeft" && direction !== 'RIGHT') direction = 'LEFT';
    if(event.key === "ArrowUp" && direction !== 'DOWN') direction = 'UP';
    if(event.key === "ArrowRight" && direction !== 'LEFT') direction = 'RIGHT';
    if(event.key === "ArrowDown" && direction !== 'UP') direction = 'DOWN';
});

// Controle via toque (swipe)
let touchStartX = 0, touchStartY = 0;
canvas.addEventListener('touchstart', e => {
    const touch = e.touches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
});
canvas.addEventListener('touchend', e => {
    const touch = e.changedTouches[0];
    const dx = touch.clientX - touchStartX;
    const dy = touch.clientY - touchStartY;

    if(Math.abs(dx) > Math.abs(dy)){
        if(dx > 0 && direction !== 'LEFT') direction = 'RIGHT';
        else if(dx < 0 && direction !== 'RIGHT') direction = 'LEFT';
    } else {
        if(dy > 0 && direction !== 'UP') direction = 'DOWN';
        else if(dy < 0 && direction !== 'DOWN') direction = 'UP';
    }
});

// Funções do jogo
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Desenha a cobra
    for(let i=0; i<snake.length; i++){
        ctx.fillStyle = (i === 0) ? "green" : "lime";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
    }

    // Desenha a comida
    ctx.fillStyle = "red";
    ctx.fillRect(food.x, food.y, box, box);

    // Posição da cabeça
    let snakeX = snake[0].x;
    let snakeY = snake[0].y;

    if(direction === 'LEFT') snakeX -= box;
    if(direction === 'UP') snakeY -= box;
    if(direction === 'RIGHT') snakeX += box;
    if(direction === 'DOWN') snakeY += box;

    // Comer a comida
    if(snakeX === food.x && snakeY === food.y){
        score++;
        document.getElementById('score').innerText = "Pontuação: " + score;
        food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box
        };
    } else {
        snake.pop();
    }

    // Nova cabeça
    const newHead = {x: snakeX, y: snakeY};

    // Checa colisão
    if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || collision(newHead, snake)){
        alert('Game Over! Sua pontuação: ' + score);
        snake = [{x: 9 * box, y: 10 * box}];
        direction = 'RIGHT';
        score = 0;
        document.getElementById('score').innerText = "Pontuação: " + score;
    }

    snake.unshift(newHead);
}

function collision(head, array){
    for(let i=0; i<array.length; i++){
        if(head.x === array[i].x && head.y === array[i].y) return true;
    }
    return false;
}

function restartGame(){
    snake = [{x: 9 * box, y: 10 * box}];
    direction = 'RIGHT';
    score = 0;
    document.getElementById('score').innerText = "Pontuação: " + score;
}

// Loop do jogo
setInterval(draw, 150);
