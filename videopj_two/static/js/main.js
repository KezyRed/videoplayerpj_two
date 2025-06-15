// static/js/main.js - Основной JavaScript файл

// Детекция офлайн статуса
function updateOnlineStatus() {
    const indicator = document.getElementById('offline-indicator');
    if (navigator.onLine) {
        indicator.classList.remove('show');
    } else {
        indicator.classList.add('show');
    }
}

// Слушатели событий для статуса сети
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Проверка при загрузке страницы
document.addEventListener('DOMContentLoaded', updateOnlineStatus);

// Video.js глобальная конфигурация
if (typeof videojs !== 'undefined') {
    videojs.options.fluid = true;
    videojs.options.responsive = true;
    
    // Настройки по умолчанию для всех плееров
    videojs.hook('setup', function(player) {
        return {
            playbackRates: [0.5, 0.75, 1, 1.25, 1.5, 2],
            controls: true,
            preload: 'metadata',
            html5: {
                vhs: {
                    overrideNative: !videojs.browser.IS_SAFARI
                }
            },
            techOrder: ['html5'],
            userActions: {
                hotkeys: {
                    volumeStep: 0.1,
                    seekStep: 5,
                    enableModifiersForNumbers: false
                }
            }
        };
    });
} else {
    console.error('Video.js не загружен! Проверьте наличие файлов в static/video-js/');
}

