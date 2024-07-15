# Linux System Inspector

## Описание

Linux System Inspector - это легковесная утилита командной строки, написанная на C, для быстрого сбора и отображения ключевой информации о системе Linux. Она предоставляет моментальный снимок состояния системы, включая информацию о железе, использовании ресурсов и сетевых настройках.

## Возможности

- Отображение имени хоста
- Количество ядер CPU
- Общий и свободный объем оперативной памяти
- Общий и свободный объем дискового пространства
- Средняя нагрузка на систему
- Версия ядра Linux
- Время работы системы
- Информация о swap
- Количество запущенных процессов
- IP-адрес
- Использование CPU

## Требования

- Операционная система Linux
- Компилятор GCC
- Библиотека math (libm)

## Установка

1. Клонируйте репозиторий:

git clone https://github.com/podobaylo/prg-notes.git

2. Перейдите в директорию проекта:

cd prg-notes/linux/inspect-linux

3. Скомпилируйте программу:

gcc -o inspect inspect-linux.c

## Использование

Запустите скомпилированную программу:


./inspect


Вывод будет представлен в формате CSV, удобном для дальнейшей обработки:


HOSTNAME:,example.com,CPU:,4,RAM_TOTAL:,16384,RAM_FREE:,8192,...

## Примеры использования

1. Сохранение вывода в файл:

./inspect > system_info.csv

2. Периодический мониторинг с помощью cron:
Добавьте в crontab строку:

*/5 * * * * /path/to/inspect >> /var/log/system_monitor.log

3. Извлечение конкретных данных:

./inspect | awk -F',' '{print $2","$4","$18}' # Выводит hostname, CPU cores и IP

## Вклад в проект

Приветствуются предложения по улучшению кода, добавлению новых функций или исправлению ошибок. Пожалуйста, создавайте issues или отправляйте pull requests.

## Лицензия

[MIT License](https://opensource.org/licenses/MIT)

## Автор

[prg.in.ua]

---

Надеемся, что этот инструмент будет полезен для системных администраторов, DevOps инженеров и всех, кто работает с системами Linux!

## AI Collaboration

This project was developed in collaboration with an AI language model created by Anthropic. The AI assistant provided guidance, code suggestions, and helped in refining the project structure and documentation. This collaboration showcases the potential of human-AI teamwork in software development.

Key contributions of the AI assistant included:
- Suggesting improvements to the code structure and functionality
- Helping debug and optimize the code
- Assisting in creating a comprehensive README and documentation
- Providing insights on best practices for system information gathering in Linux

While the core ideas and implementation decisions were made by the human developer, the AI played a supportive role throughout the development process, demonstrating how AI can be a valuable tool in modern software development workflows.
