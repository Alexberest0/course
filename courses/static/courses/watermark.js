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



// --- Защита от инструментов разработчика и сохранения ---

(function() {
    // --- Блокировка контекстного меню (правая кнопка мыши) ---
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });

    // --- Блокировка клавиш вызова DevTools ---
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F12' ||
            (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) ||
            (e.ctrlKey && (e.key === 'U' || e.key === 'u')) ||
            (e.ctrlKey && (e.key === 'S' || e.key === 's'))) {
            e.preventDefault();
            return false;
        }
    });

    // --- Обнаружение открытия DevTools через размер окна ---
    let devtoolsOpen = false;
    function detectDevTools() {
        const threshold = 150;
        const widthDiff = window.outerWidth - window.innerWidth;
        const heightDiff = window.outerHeight - window.innerHeight;
        if (widthDiff > threshold || heightDiff > threshold) {
            if (!devtoolsOpen) {
                devtoolsOpen = true;
                // Принудительно очищаем страницу или редиректим
                document.body.innerHTML = '<h1 style="color:red; text-align:center; margin-top:20%;">Инструменты разработчика отключены на этом сайте</h1>';
                // window.location.href = '/';
            }
        } else {
            devtoolsOpen = false;
        }
    }
    setInterval(detectDevTools, 1000);

    // --- Защита водяного знака от удаления ---
    function guardWatermark() {
        const wrapper = document.getElementById('videoWrapper');
        let watermark = document.getElementById('watermark');
        if (!watermark && wrapper && !wrapper.querySelector('.watermark')) {
            const newWatermark = document.createElement('div');
            newWatermark.className = 'watermark';
            newWatermark.id = 'watermark';
            newWatermark.textContent = 'ID: ' + (window.userPublicId || '???');
            wrapper.appendChild(newWatermark);
            console.log('Водяной знак восстановлен');
        }
    }
    setInterval(guardWatermark, 500);

    // --- Дополнительная защита видео ---
    const videos = document.querySelectorAll('video');
    videos.forEach(v => {
        v.setAttribute('controlsList', 'nodownload');
        v.addEventListener('contextmenu', e => e.preventDefault());
        v.addEventListener('dragstart', e => e.preventDefault());
    });

    // --- (Опционально) Плавное движение водяного знака (если нужно) ---
    // Можно оставить старую логику движения, но я её здесь не включаю, чтобы не конфликтовать.
    // Если хотите, добавьте вызов функции moveWatermark из предыдущих версий.
})();