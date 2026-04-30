// courses/static/courses/watermark.js

let moveInterval = null;
const watermark = document.getElementById('watermark');
const wrapper = document.getElementById('videoWrapper');
const video = document.querySelector('video');

// Функция перемещения водяного знака в случайную позицию
function moveWatermark() {
    if (!watermark || !wrapper) return;

    const wrapperRect = wrapper.getBoundingClientRect();
    const markRect = watermark.getBoundingClientRect();

    let maxTop = wrapperRect.height - markRect.height - 10;
    let maxLeft = wrapperRect.width - markRect.width - 10;

    if (maxTop < 10) maxTop = 10;
    if (maxLeft < 10) maxLeft = 10;

    const top = 5 + Math.random() * maxTop;
    const left = 5 + Math.random() * maxLeft;

    watermark.style.top = top + 'px';
    watermark.style.left = left + 'px';
}

function startMoving() {
    if (moveInterval !== null) return;
    moveWatermark(); // сразу сдвигаем
    moveInterval = setInterval(moveWatermark, 2000);
}

function stopMoving() {
    if (moveInterval !== null) {
        clearInterval(moveInterval);
        moveInterval = null;
    }
}

// Обработчики событий видео
if (video) {
    video.addEventListener('play', startMoving);
    video.addEventListener('pause', stopMoving);
    video.addEventListener('ended', stopMoving);
    video.addEventListener('seeked', () => {
        if (!video.paused) startMoving();
    });
    // Если видео уже загружено и не на паузе (например, автостарт)
    if (!video.paused) startMoving();
} else {
    // Если видео по какой-то причине нет – двигаем знак всё равно
    startMoving();
}

// При изменении размера окна или выходе из полноэкранного режима пересчитываем позицию
window.addEventListener('resize', () => {
    if (moveInterval !== null) moveWatermark();
});

// Событие полноэкранного режима
function onFullscreenChange() {
    if (moveInterval !== null) {
        // Небольшая задержка, чтобы браузер успел пересчитать размеры
        setTimeout(moveWatermark, 50);
    }
}
document.addEventListener('fullscreenchange', onFullscreenChange);
document.addEventListener('webkitfullscreenchange', onFullscreenChange);
document.addEventListener('mozfullscreenchange', onFullscreenChange);