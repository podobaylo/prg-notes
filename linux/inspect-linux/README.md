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

Для максимальной портабельности: 

gcc -static -O2 -o inspect inspect-linux.c -lm -static-libgcc -static-libstdc++ -lrt -lpthread -ldl

## Использование

Запустите скомпилированную программу:


./si


Вывод будет представлен в формате CSV, удобном для дальнейшей обработки:


HOSTNAME:,example.com,CPU:,4,RAM_TOTAL:,16384,RAM_FREE:,8192,...


## Примеры использования

### Локальное использование

1. Сохранение вывода в файл:

./si > system_info.csv

2. Периодический мониторинг с помощью cron:
Добавьте в crontab строку:

*/5 * * * * /path/to/si >> /var/log/system_monitor.log

3. Извлечение конкретных данных:

./inspect | awk -F',' '{print $2","$4","$18}' # Выводит hostname, CPU cores и IP

### Использование с Ansible для инспектирования множества систем

Основная цель этого инструмента - возможность запуска через Ansible для инспектирования множества систем одновременно. Вот пример, как это можно реализовать:

1. Создайте Ansible playbook `inspect_systems.yml`:

```yaml
---
- name: Inspect systems
  hosts: all
  become: yes
  tasks:
    - name: Check if inspect binary exists
      stat:
        path: /usr/local/bin/si
      register: si_binary

    - name: Copy inspect binary if not exists
      copy:
        src: /usr/local/bin/si
        dest: /usr/local/bin/si
        mode: '0755'
      when: not si_binary.stat.exists

    - name: Run inspect
      command: /usr/local/bin/si
      register: inspect_result

    - name: Save results on target host
      copy:
        content: "{{ inventory_hostname }},{{ inspect_result.stdout }}\n"
        dest: "/tmp/{{ inventory_hostname }}_inspect.csv"

    - name: Ensure results directory exists on Ansible controller
      local_action:
        module: file
        path: "/tmp/results"
        state: directory
      run_once: true

    - name: Fetch results from target hosts
      fetch:
        src: "/tmp/{{ inventory_hostname }}_inspect.csv"
        dest: "/tmp/results/"
        flat: yes


```

Запустите playbook:

ansible-playbook -i your_inventory inspect_systems.yml

Объедините результаты в один файл:

cat /path/to/results/*_inspect.csv > all_systems_inspect.csv

( cat /tmp/results/* |awk '{for(i=1;i<=NF;i++) if($i !~ /:$/) printf "%s%s", $i, (i==NF?ORS:OFS)}' OFS=","  )

## Вклад в проект

Приветствуются предложения по улучшению кода, добавлению новых функций или исправлению ошибок. Пожалуйста, создавайте issues или отправляйте pull requests.

## Лицензия

[MIT License](https://opensource.org/licenses/MIT)


---

Надеемся, что этот инструмент будет полезен для системных администраторов, DevOps инженеров и всех, кто работает с системами Linux!

## AI Collaboration
Этот проект был разработан в сотрудничестве с моделью искусственного интеллекта, созданной Anthropic. ИИ-ассистент предоставил руководство, предложения по коду и помог в улучшении структуры проекта и документации. Это сотрудничество демонстрирует потенциал совместной работы человека и ИИ в разработке программного обеспечения.
Ключевые вклады ИИ-ассистента включали:
Предложения по улучшению структуры и функциональности кода
Помощь в отладке и оптимизации кода
Содействие в создании подробного README и документации
Предоставление информации о лучших практиках сбора системной информации в Linux
В то время как основные идеи и решения по реализации принимались человеком-разработчиком, ИИ играл вспомогательную роль на протяжении всего процесса разработки, демонстрируя, как ИИ может быть ценным инструментом в современных рабочих процессах разработки программного обеспечения.
