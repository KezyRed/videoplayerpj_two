// static/js/timecodes.js - Исправленная версия

document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('video-player');
    if (!videoElement) return;

    setTimeout(() => {
        const player = videojs('video-player');
        
        if (!player) {
            console.error('Video.js плеер не найден');
            return;
        }

        const timecodeItems = document.querySelectorAll('.timecode-item');
        console.log('Найдено таймкодов:', timecodeItems.length);

        // Флаг для предотвращения автоскролла во время ручного клика
        let isManualClick = false;

        // Добавляем обработчики кликов для таймкодов
        timecodeItems.forEach(item => {
            item.addEventListener('click', function() {
                const timeSeconds = parseInt(this.dataset.time);
                
                if (!isNaN(timeSeconds)) {
                    console.log('Переход к времени:', timeSeconds, 'секунд');
                    
                    // Устанавливаем флаг ручного клика
                    isManualClick = true;
                    
                    // Убираем активный класс у всех элементов
                    timecodeItems.forEach(el => el.classList.remove('active', 'current'));
                    
                    // Добавляем активный класс к текущему элементу
                    this.classList.add('active', 'current');
                    
                    // Переходим к указанному времени
                    player.currentTime(timeSeconds);
                    
                    // Сбрасываем флаг через небольшую задержку
                    setTimeout(() => {
                        isManualClick = false;
                    }, 1000);
                    
                    // Если видео на паузе, запускаем воспроизведение
                    if (player.paused()) {
                        player.play();
                    }
                }
            });
        });

        // Обновление активного таймкода при воспроизведении
        player.on('timeupdate', function() {
            // Не обновляем активный таймкод во время ручного клика
            if (!isManualClick) {
                const currentTime = player.currentTime();
                updateActiveTimecode(currentTime);
            }
        });

        // Функция обновления активного таймкода
        function updateActiveTimecode(currentTime) {
            let activeTimecode = null;
            
            timecodeItems.forEach(item => {
                const timeSeconds = parseInt(item.dataset.time);
                
                // Убираем текущий класс только если это не ручной клик
                if (!isManualClick) {
                    item.classList.remove('current');
                }
                
                // Если текущее время больше времени таймкода, он может быть активным
                if (currentTime >= timeSeconds) {
                    activeTimecode = item;
                }
            });
            
            // Устанавливаем текущий таймкод только если это не ручной клик
            if (activeTimecode && !isManualClick) {
                timecodeItems.forEach(item => item.classList.remove('current'));
                activeTimecode.classList.add('current');
                
                // Прокручиваем к активному таймкоду только при автоматическом обновлении
                scrollToActiveTimecode(activeTimecode);
            }
        }

        // ИСПРАВЛЕННАЯ функция прокрутки к активному таймкоду
        function scrollToActiveTimecode(activeItem) {
            if (!activeItem || isManualClick) return;
            
            const container = activeItem.closest('.list-group');
            if (!container) return;
            
            // Проверяем, есть ли вертикальная прокрутка у контейнера
            if (container.scrollHeight <= container.clientHeight) return;
            
            const containerRect = container.getBoundingClientRect();
            const itemRect = activeItem.getBoundingClientRect();
            
            // Более точная проверка видимости элемента
            const isVisible = (
                itemRect.top >= containerRect.top + 10 && 
                itemRect.bottom <= containerRect.bottom - 10
            );
            
            // Прокручиваем только если элемент действительно не виден
            if (!isVisible) {
                // Используем более мягкую прокрутку
                const scrollTop = container.scrollTop;
                const itemOffsetTop = activeItem.offsetTop;
                const containerHeight = container.clientHeight;
                const itemHeight = activeItem.offsetHeight;
                
                // Вычисляем оптимальную позицию (центрируем элемент)
                const targetScrollTop = itemOffsetTop - (containerHeight / 2) + (itemHeight / 2);
                
                // Плавная прокрутка
                container.scrollTo({
                    top: Math.max(0, targetScrollTop),
                    behavior: 'smooth'
                });
            }
        }

        // Клавиатурные сокращения (без изменений)
        document.addEventListener('keydown', function(e) {
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

        // Остальной код без изменений...
        timecodeItems.forEach(item => {
            item.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                const timeSeconds = parseInt(this.dataset.time);
                
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    const text = `${this.querySelector('.timecode-time').textContent} - ${this.textContent.trim()}`;
                    navigator.clipboard.writeText(text);
                    showNotification('Таймкод скопирован в буфер обмена');
                }
            });
        });

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

        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'alert alert-success position-fixed';
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; opacity: 0; transition: opacity 0.3s;';
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => notification.style.opacity = '1', 10);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => document.body.removeChild(notification), 300);
            }, 3000);
        }

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

    }, 500);
});