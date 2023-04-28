
# Настройка

Поднять весь сервис: docker-compose build && docker-compose up

Адрес прокси: 0.0.0.0:2000



# Использование


Отправить запрос с помощью скрипта из дирректории HW_1: python3 api.py "get_result format"

Отправить запрос с помощью nc: echo -n "get_result format" | nc -u -w1 0.0.0.0 2000

Вместо format следует указывать формат запроса из списка ["NATIVE", "XML", "JSON", "GPB", "APACHE", "YAML", "MSGPACK", "["NATIVE", "XML", "JSON", "GPB", "APACHE", "YAML", "MSGPACK"]
