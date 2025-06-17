// Исправленная версия для Linux
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация таймкодов...');
    
    const videoElement = document.getElementById('video-player');
    if (!videoElement) {
        console.error('Видео элемент не найден!');
        return;
    }

    // Увеличенная задержка для Linux
    setTimeout(() => {
        console.log('Попытка инициализации Video.js...');
        
        // Проверяем доступность Video.js
        if (typeof videojs === 'undefined') {
            console.error('Video.js не загружен!');
            return;
        }

        const player = videojs('video-player', {
            fluid: true,
            responsive: true,
            controls: true,
            preload: 'metadata'
        });
        
        if (!player) {
            console.error('Video.js плеер не инициализирован');
            return;
        }

        const timecodeItems = document.querySelectorAll('.timecode-item');
        console.log(`Найдено таймкодов: ${timecodeItems.length}`);

        if (timecodeItems.length === 0) {
            console.warn('Таймкоды не найдены на странице');
            return;
        }

        let isManualClick = false;

        // Обработчики кликов для таймкодов
        timecodeItems.forEach((item, index) => {
            console.log(`Настройка таймкода ${index + 1}:`, item.dataset.time);
            
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const timeSeconds = parseInt(this.dataset.time);
                
                if (isNaN(timeSeconds)) {
                    console.error('Неверный формат времени:', this.dataset.time);
                    return;
                }

                console.log(`Переход к времени: ${timeSeconds} секунд`);
                
                isManualClick = true;
                
                // Убираем активные классы
                timecodeItems.forEach(el => {
                    el.classList.remove('active', 'current');
                });
                
                // Добавляем активные классы
                this.classList.add('active', 'current');
                
                // Переходим к времени
                try {
                    player.currentTime(timeSeconds);
                    if (player.paused()) {
                        player.play().catch(err => {
                            console.warn('Автозапуск заблокирован браузером:', err);
                        });
                    }
                } catch (error) {
                    console.error('Ошибка при установке времени:', error);
                }
                
                // Сбрасываем флаг
                setTimeout(() => {
                    isManualClick = false;
                }, 1000);
            });
        });

        // Обновление активного таймкода
        player.on('timeupdate', function() {
            if (isManualClick) return;
            
            const currentTime = player.currentTime();
            updateActiveTimecode(currentTime);
        });

        function updateActiveTimecode(currentTime) {
            let activeTimecode = null;
            
            timecodeItems.forEach(item => {
                const timeSeconds = parseInt(item.dataset.time);
                
                if (!isManualClick) {
                    item.classList.remove('current');
                }
                
                if (currentTime >= timeSeconds) {
                    activeTimecode = item;
                }
            });
            
            if (activeTimecode && !isManualClick) {
                timecodeItems.forEach(item => item.classList.remove('current'));
                activeTimecode.classList.add('current');
            }
        }

        // События плеера для отладки
        player.on('loadstart', () => console.log('Video: загрузка начата'));
        player.on('canplay', () => console.log('Video: готов к воспроизведению'));
        player.on('error', (e) => console.error('Video: ошибка', e));
        
        console.log('Система таймкодов инициализирована успешно');

    }, 1000); // Увеличенная задержка для Linux
});