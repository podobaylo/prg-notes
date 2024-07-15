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

### Локальное использование

1. Сохранение вывода в файл:

./inspect > system_info.csv
text

2. Периодический мониторинг с помощью cron:
Добавьте в crontab строку:

*/5 * * * * /path/to/inspect >> /var/log/system_monitor.log
text

3. Извлечение конкретных данных:

./inspect | awk -F',' '{print $2","$4","$18}' # Выводит hostname, CPU cores и IP
text

### Использование с Ansible для инспектирования множества систем

Основная цель этого инструмента - возможность запуска через Ansible для инспектирования множества систем одновременно. Вот пример, как это можно реализовать:

1. Создайте Ansible playbook `inspect_systems.yml`:

```yaml
---
- name: Inspect systems
  hosts: all
  become: yes
  tasks:
    - name: Copy inspect binary
      copy:
        src: /path/to/inspect
        dest: /tmp/inspect
        mode: '0755'

    - name: Run inspect
      command: /tmp/inspect
      register: inspect_result

    - name: Collect results
      local_action:
        module: copy
        content: "{{ inventory_hostname }},{{ inspect_result.stdout }}"
        dest: "/path/to/results/{{ inventory_hostname }}_inspect.csv"

    - name: Remove inspect binary
      file:
        path: /tmp/inspect
        state: absent

Запустите playbook:
text
ansible-playbook -i your_inventory inspect_systems.yml

Объедините результаты в один файл:
text
cat /path/to/results/*_inspect.csv > all_systems_inspect.csv


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
