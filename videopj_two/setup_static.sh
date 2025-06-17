#!/bin/bash

echo "Создание папок..."
mkdir -p static/bootstrap/{css,js}
mkdir -p static/bootstrap-icons/font
mkdir -p static/video-js/{css,js}

echo "Скачивание Bootstrap..."
wget -q https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css -O static/bootstrap/css/bootstrap.min.css
wget -q https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js -O static/bootstrap/js/bootstrap.bundle.min.js

echo "Скачивание Bootstrap Icons..."
wget -q https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css -O static/bootstrap-icons/font/bootstrap-icons.css
wget -q https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/fonts/bootstrap-icons.woff -O static/bootstrap-icons/font/bootstrap-icons.woff
wget -q https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/fonts/bootstrap-icons.woff2 -O static/bootstrap-icons/font/bootstrap-icons.woff2

echo "Скачивание Video.js..."
wget -q https://vjs.zencdn.net/8.6.1/video-js.css -O static/video-js/css/video-js.css
wget -q https://vjs.zencdn.net/8.6.1/video.min.js -O static/video-js/js/video.min.js

echo "Установка завершена!"
echo "Проверьте файлы:"
find static/ -name "*.css" -o -name "*.js" -o -name "*.woff*" | sort

echo "Создайте папку для шрифтов"
mkdir -p static/bootstrap-icons/font/fonts

echo "Скачайте CSS"
wget https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css -O static/bootstrap-icons/font/bootstrap-icons.css

echo "Скачайте шрифты"
wget https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/fonts/bootstrap-icons.woff -O static/bootstrap-icons/font/fonts/bootstrap-icons.woff
wget https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/fonts/bootstrap-icons.woff2 -O static/bootstrap-icons/font/fonts/bootstrap-icons.woff2