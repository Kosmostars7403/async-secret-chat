# Утилита для взаимодействия с подпольным чатом
Проект создан для вывода в топ пожилого игрока в Майнкрафт (жульническим способом).

## Как установить

Для запуска программы у вас уже должен быть установлен Python 3. 

Установите зависимости командой в терминале:

```
$ pip install -r requirements.txt
```

## Использование
Проект представлен двумя скриптами `listen_chat.py` и `write_to_chat.py`.
Оба скрипта принимают аргументы командной строки, но также могут получать значения из переменных окружения.
Создайте файл `.env` в корневом каталоге и заполняйте необходимыми переменными.

### Читать чат и сохранять историю
За это отвечает `listen_chat.py`.

| Переменная | Аргумент | Описание | Значение по умолчанию
|----|----|----|----
|`LISTENING_HOST`| `--host` | Адрес хоста | `minechat.dvmn.org`
|`LISTENING_PORT`| `--port` | Порт хоста | `5000`
|`CHAT_LOG_PATH`| `--history` | Путь к файлу для сохранения истории переписки | `chat_log.txt`

### Написать сообщение в чат
За это отвечает `write_to_chat.py`, он имеет один позиционный обязательный аргумент, - это сообщение.

При первой отправке сообщения в чат - нужно зарегистрироваться, для этого после текста сообщения выберите никнейм.

```
python3 write_to_chat.py bla-bla-bla --username SUPER_PUPER_NICKNAME
```
После этого скрипт запишет полученный токен авторизации в файл `token.txt`, и вам больше не придется думать об авторизации.
Все последующие отправки сообщений будут выглядеть так:
```
python3 write_to_chat.py bla-bla-bla
```
| Переменная | Аргумент | Описание | Значение по умолчанию
|----|----|----|----
|`SENDING_HOST`| `--host` | Адрес хоста | `minechat.dvmn.org`
|`SENDING_PORT`| `--port` | Порт хоста | `5050`
|`MINECHAT_TOKEN`| `--minechat_token` | Токен авторизации | `None`
| - | `--username` | Желаемое имя пользователя для регистрации | ''


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
