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

## Пересылка сообщений между пользователями
За пересылку сообщений отвечает btpeer.py и класс DBMember:
```python
#--------------------------------------------------------------------------
def mainloop( self ):
#--------------------------------------------------------------------------
    self.s = self.makeserversocket( self.serverport )
    self.s.settimeout(5)
    self.__debug( 'Server started: %s (%s:%d)'
            % ( self.myid, self.serverhost, self.serverport ) )

    while not self.shutdown:
        try:
            self.__debug( 'Listening for connections...' )


            clientsock, clientaddr = self.s.accept()
            clientsock.settimeout(None)

            t = threading.Thread( target = self.__handlepeer,
                        args = [ clientsock ] )
            t.start()
        except KeyboardInterrupt:
            print ('KeyboardInterrupt: stopping mainloop')
            self.shutdown = True
            continue
        except:
            if self.debug:
                traceback.print_exc()
                continue

# end while loop
    self.__debug( 'Main loop exiting' )

    self.s.close()

# end mainloop method
```
В данном цикле создается сокет для прослушки входящих сообщений и на основе этого будут строится дальнейшие взаимодействия пользователей сети. Так как в нашей програмной реализации нет "центра", каждый пользователь ведет себя и как сервер (для получения сообщений и обновлений базы данных), и как клиент (для отправки сообщений). Таким образом мы создали p2p сеть.

### Список контактов
С помощью следующих функций возможно добавление контактов в свой доверенный список, пересылка сообщений контакту а также просмотр всех возможных контактов:
```python
def add_contact(self, name, host, port):
    peerid = host + ':' + str(port)
    self.addpeer(peerid=peerid, host=host, port=port)
    self.contacts[name] = peerid


def send_to_contact(self, name, msg, type):
    self.sendtopeer(self.contacts[name], msgtype=type, msgdata=msg, waitreply=False)


def list_contacts(self):
    inc = 1
    for i in self.contacts.keys():
        print('%d: ' % inc + i)
        inc += 1
```

### Голосование
Для реализации голосования и добавления блоков с информацией в базу данных используются следующие функции:
```python
def list_candidates(self):
    inc = 1
    for i in self.__candidates_and_votes.keys():
        votes = self.__candidates_and_votes[i]
        print(f'{inc}: {i} - {votes} votes')
        inc += 1


def vote_for(self, candidate):
    if candidate in self.__candidates_and_votes.keys():
        file_name = os.path.join(self.file_dir, self.hashed_id + datetime.now().strftime('%H%M%S') + '.txt')
        with open(file_name, 'w') as f:
            f.write(candidate)
        self.__candidates_and_votes[candidate] += 1
    else:
        print('No such candidate with that name')
```

### Интерфейс в терминале
Пока что данная програмная реализация децентрализованной базы данных запускается только на персональных компьтерах, но уже доступен интерфейс:
```python
# Перечень всех возможных команд
"/help"

# Добавление нового контакта
"/addcontact"

# Отправка сообщения контакту (поддерживается пересылка текста и файлов)
"/sendto"

# Перечень контактов
"/contacts"

# Проголосовать за данного кандидата
"/votefor"

# Список кандидатов
"/candidates"

# Выход из программы
"/exit"
```