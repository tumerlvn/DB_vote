# DB_vote

DB_vote программа для голосования использующая в своей основе децентрализованную схему защищенного создания и хранения баз данных.

## Реализация

Программа реализованна с использованием протокола стираемой подписи Шаума.
```python
def generatekeys(p, g):
    message = random.randint(1, p - 1)  # сообщение
    e = random.randint(1, p - 1)  # закрытый ключ
    d = (g ** e) % p  # открытый ключ
    digitalsign = (message ** e) % p  # подпись
```

В будущих версиях программы будет включена пересылка сообщений между двумя абонентами А и Б, для полноценной реализации протокола подтверждения подлинности подписи и протокола опровержения с участием А (если Б - проверяющий).


### Пример протокола подтверждения Б
```python
def check(z):
    u, v = generate()
    y = ((M ** u) * (g ** v)) % p
    send_to_a(y)
    
    h1, h2 = receive_from_a(h1, h2)

    send_to_a(u, v)
    receive(w)
    
    if prime.eqmod(h1, y * (g ** w), p) and 
       prime.eqmod(h2, (z ** u) * (open_key ** (v + w)), p):
        print("Confirmed")
    else:
        print("Not Confirmed")
```

## Создание базы данных

За создание базы данных отвечает класс DB_Blocks
```python
class DB_Blocks(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # Создает новый блок
        pass

    def new_transaction(self):
        # Добавляет новую информацию о транзакциях
        pass

    @staticmethod
    def sign(block):
        # Подписывает блок
        pass

    @property
    def last_block(self):
        # Возвращает последний блок в цепи
        pass
```