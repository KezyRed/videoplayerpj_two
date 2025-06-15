// static/js/timecodes.js - JavaScript для работы с таймкодами

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация Video.js плеера
    const videoElement = document.getElementById('video-player');
    if (!videoElement) return;

    // Ждем полной инициализации Video.js
    setTimeout(() => {
        const player = videojs('video-player');
        
        if (!player) {
            console.error('Video.js плеер не найден');
            return;
        }

        console.log('Video.js плеер инициализирован:', player);

        // Получаем все элементы таймкодов
        const timecodeItems = document.querySelectorAll('.timecode-item');
        console.log('Найдено таймкодов:', timecodeItems.length);

        // Добавляем обработчики кликов для таймкодов
        timecodeItems.forEach(item => {
            item.addEventListener('click', function() {
                const timeSeconds = parseInt(this.dataset.time);
                
                if (!isNaN(timeSeconds)) {
                    console.log('Переход к времени:', timeSeconds, 'секунд');
                    
                    // Убираем активный класс у всех элементов
                    timecodeItems.forEach(el => el.classList.remove('active', 'current'));
                    
                    // Добавляем активный класс к текущему элементу
                    this.classList.add('active');
                    
                    // Переходим к указанному времени
                    player.currentTime(timeSeconds);
                    
                    // Если видео на паузе, запускаем воспроизведение
                    if (player.paused()) {
                        player.play();
                    }
                } else {
                    console.error('Неверное время для таймкода:', this.dataset.time);
                }
            });
        });

        // Обновление активного таймкода при воспроизведении
        player.on('timeupdate', function() {
            const currentTime = player.currentTime();
            updateActiveTimecode(currentTime);
        });

        // Функция обновления активного таймкода
        function updateActiveTimecode(currentTime) {
            let activeTimecode = null;
            
            timecodeItems.forEach(item => {
                const timeSeconds = parseInt(item.dataset.time);
                
                // Убираем текущий класс
                item.classList.remove('current');
                
                // Если текущее время больше времени таймкода, он может быть активным
                if (currentTime >= timeSeconds) {
                    activeTimecode = item;
                }
            });
            
            // Устанавливаем текущий таймкод
            if (activeTimecode) {
                timecodeItems.forEach(item => item.classList.remove('current'));
                activeTimecode.classList.add('current');
                
                // Прокручиваем к активному таймкоду
                scrollToActiveTimecode(activeTimecode);
            }
        }

        // Функция прокрутки к активному таймкоду
        function scrollToActiveTimecode(activeItem) {
            if (!activeItem) return;
            
            const container = activeItem.closest('.list-group');
            if (container) {
                const containerRect = container.getBoundingClientRect();
                const itemRect = activeItem.getBoundingClientRect();
                
                // Проверяем, виден ли элемент
                if (itemRect.top < containerRect.top || itemRect.bottom > containerRect.bottom) {
                    activeItem.scrollIntoView({
                        behavior: 'smooth',
                        block: 'nearest'
                    });
                }
            }
        }

        // Клавиатурные сокращения для навигации по таймкодам
        document.addEventListener('keydown', function(e) {
            // Проверяем, что фокус не на элементах ввода
            if (document.activeElement.tagName === 'INPUT' || 
                document.activeElement.tagName === 'TEXTAREA') {
                return;
            }

            const currentActive = document.querySelector('.timecode-item.current');
            let targetTimecode = null;

            switch(e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    if (currentActive && currentActive.previousElementSibling) {
                        targetTimecode = currentActive.previousElementSibling;
                    }
                    break;
                    
                case 'ArrowDown':
                    e.preventDefault();
                    if (currentActive && currentActive.nextElementSibling) {
                        targetTimecode = currentActive.nextElementSibling;
                    } else if (!currentActive && timecodeItems.length > 0) {
                        targetTimecode = timecodeItems[0];
                    }
                    break;
                    
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (currentActive) {
                        currentActive.click();
                    }
                    break;
            }

            if (targetTimecode) {
                targetTimecode.click();
            }
        });

        // Контекстное меню для таймкодов (опционально)
        timecodeItems.forEach(item => {
            item.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                const timeSeconds = parseInt(this.dataset.time);
                const timeDisplay = formatTime(timeSeconds);
                
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    const text = `${this.querySelector('.timecode-time').textContent} - ${this.textContent.trim()}`;
                    navigator.clipboard.writeText(text);
                    
                    // Показываем уведомление
                    showNotification('Таймкод скопирован в буфер обмена');
                }
            });
        });

        // Функция форматирования времени
        function formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {
                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            } else {
                return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            }
        }

        // Функция показа уведомлений
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'alert alert-success position-fixed';
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; opacity: 0; transition: opacity 0.3s;';
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            // Показываем уведомление
            setTimeout(() => notification.style.opacity = '1', 10);
            
            // Скрываем через 3 секунды
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => document.body.removeChild(notification), 300);
            }, 3000);
        }

        // Добавляем индикаторы загрузки
        player.on('waiting', function() {
            console.log('Видео загружается...');
        });

        player.on('canplay', function() {
            console.log('Видео готово к воспроизведению');
        });

        player.on('error', function(e) {
            console.error('Ошибка воспроизведения видео:', e);
        });

        console.log('Система таймкодов полностью инициализирована');

    }, 500); // Задержка для корректной инициализации Video.js
});

// Дополнительные функции для расширенной функциональности

// Функция для создания прогресс-бара с маркерами таймкодов
function createTimecodeProgressBar() {
    const timecodeItems = document.querySelectorAll('.timecode-item');
    const videoElement = document.getElementById('video-player');
    
    if (!videoElement || timecodeItems.length === 0) return;

    const player = videojs('video-player');
    if (!player) return;

    // Создаем контейнер для прогресс-бара
    const progressContainer = document.createElement('div');
    progressContainer.className = 'timecodes-progress-container mb-3';
    progressContainer.innerHTML = `
        <div class="progress-track">
            <div class="progress-fill" style="width: 0%"></div>
        </div>
    `;

    // Добавляем маркеры таймкодов
    player.ready(() => {
        const duration = player.duration();
        if (duration && duration > 0) {
            timecodeItems.forEach(item => {
                const timeSeconds = parseInt(item.dataset.time);
                const percentage = (timeSeconds / duration) * 100;
                
                const marker = document.createElement('div');
                marker.className = 'progress-marker';
                marker.style.left = percentage + '%';
                marker.dataset.time = timeSeconds;
                
                if (item.classList.contains('chapter-item')) {
                    marker.classList.add('chapter-marker');
                }
                
                marker.addEventListener('click', () => {
                    player.currentTime(timeSeconds);
                    item.click();
                });
                
                progressContainer.querySelector('.progress-track').appendChild(marker);
            });
        }
    });

    // Обновляем прогресс-бар
    player.on('timeupdate', () => {
        const currentTime = player.currentTime();
        const duration = player.duration();
        
        if (duration > 0) {
            const percentage = (currentTime / duration) * 100;
            const progressFill = progressContainer.querySelector('.progress-fill');
            if (progressFill) {
                progressFill.style.width = percentage + '%';
            }
        }
    });

    // Вставляем прогресс-бар перед списком таймкодов
    const timecodesList = document.querySelector('.list-group');
    if (timecodesList && timecodesList.parentNode) {
        timecodesList.parentNode.insertBefore(progressContainer, timecodesList);
    }
}

// Инициализируем прогресс-бар после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(createTimecodeProgressBar, 1000);
});