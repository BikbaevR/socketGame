import socket
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаем объект - сокет, AF_INET - ipv4, SOCK_STREAM - tcp
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #выключаем упаковывание группы пакетов (алгоритм Нейгла)
main_socket.bind(("127.0.0.1", 10000))
main_socket.setblocking(0) #не останавливать выполнение программы при подключении клиентов
main_socket.listen(5)
print("Сокет создан")

players_socket = [] #список игроков

while True:
    #проверим есть ли желаеющие войти в игру
    try: #пытаемся подключить клиента
        new_socket, addr = main_socket.accept() #принимаем подключение
        print(f"Подключился: {addr}") #сообщение о подключении клиента
        new_socket.setblocking(0) #не блокрует программу
        players_socket.append(new_socket) #добавляем клиента в список клиентов
    except:
        #print("Нет желающих войти в игру")
        pass

    #считывать команды всех игроков
    for sock in players_socket:
        try: #пробуем получить данные
            data = sock.recv(1024) #прочитать данные из сокета
            data = data.decode("UTF-8") #переводим байты в строки
            print(f"Сервер получил: {data}")
        except:
            pass
    #обработать команды
    #отправить новое состояние игрового поля
    for sock in players_socket:
        try: #пробуем отправить данные
            sock.send(f"Новое состояние игры".encode()) #отправляем данные клиенту
        except:
            print(f"Отключился игрок {sock}")
            players_socket.remove(sock) #если мы не можем отправить данные клиенту - удаляем его
            sock.close() #закрываем его сокет
    time.sleep(0.01) #останавливаем цикл на 1 секунду