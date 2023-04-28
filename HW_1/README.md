
# Настройка

1) Склонировать репозиторий

2) Поднять весь сервис из дирректории HW_1:
```
docker-compose build && docker-compose up
```

3) Адрес прокси:
```
0.0.0.0:2000
```



# Использование


Отправить запрос с помощью скрипта из дирректории HW_1: 
```
python3 api.py "get_result format"
```

Отправить запрос с помощью nc:

```
nc -u 0.0.0.0 2000
get_result format
```

Вместо format следует указывать формат запроса из списка ["NATIVE", "XML", "JSON", "GPB", "APACHE", "YAML", "MSGPACK", "ALL"]

# Примеры работы

Через скрипт:

```
➜  HW_1 git:(main) ✗ python3 api.py "get_result all"
MSGPACK - 3.8973049995547626ms - 132 - 4.156062999754795ms
GPB - 9.30353700005071ms - 103 - 6.711875999826589ms
JSON - 16.26486399982241ms - 199 - 12.436961000275915ms
APACHE - 24.220186999627913ms - 86 - 22.781472000133363ms
NATIVE - 8.288953000374022ms - 199 - 58.2334249993437ms
XML - 1806.784665000123ms - 470 - 194.98867499987682ms
YAML - 1052.6762030003738ms - 180 - 2094.732927000223ms

➜  HW_1 git:(main) ✗ python3 api.py "get_result JSON"
JSON - 13.949780999610084ms - 199 - 8.039866999752121ms

➜  HW_1 git:(main) ✗ python3 api.py "get_result INVALIDFORMAT"
Invalid format!
```

Через nc:

```
➜  HW_1 git:(main) ✗ nc -u 0.0.0.0 2000
get_result all
GPB - 10.166234000280383ms - 103 - 8.680709000145725ms
MSGPACK - 3.907107000486576ms - 132 - 3.9856250004959293ms
JSON - 23.02798599976086ms - 199 - 8.483737000460678ms
APACHE - 26.52500800013513ms - 86 - 23.976016999768035ms
NATIVE - 8.947221999733301ms - 199 - 80.73275100014143ms
XML - 1778.570450999723ms - 470 - 201.6793350003354ms
YAML - 1033.911886000169ms - 180 - 2068.575878000047ms
get_result json
JSON - 17.713712999466225ms - 199 - 8.77499699981854ms
get_result invalid      
Invalid format!
```



