import socket
import pygame



WIDTH_WINDOW, HEIGHT_WINDOW = 1000, 800 #задаем размер окна

#подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаем объект - сокет, AF_INET - ipv4, SOCK_STREAM - tcp
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #выключаем упаковывание группы пакетов (алгоритм Нейгла)
sock.connect(("127.0.0.1", 10000)) #подключаемся к серверу


#создание окна игры
pygame.init() #инициализируем pygame
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW)) #создаем окно
pygame.display.set_caption("Моя игра")

old_vector = (0, 0) #задаем первоначальное значение вектора

running = True

while running:

    #обработка событий
    for event in pygame.event.get(): #список произошедших событий
        if event.type == pygame.QUIT: #если нажали на закрытие окна
            running = False #останавливаем главный цикл

    #считаем положение мыши игрока
    if pygame.mouse.get_focused(): #находиться ли курсор мыши в окне программы
        pos = pygame.mouse.get_pos() #получаем координаты мыши
        #print(f"{pos}")
        vector = (pos[0] - WIDTH_WINDOW // 2, pos[1] - HEIGHT_WINDOW // 2) #позиция куда нам нужно направить игрока
        #print(f"{vector}")
        if (vector[0]) ** 2 + (vector[1]) ** 2 <= 50 ** 2: #если мышка находиться внутри игрока
            vector = (0, 0) # недвигаем игрока


    #отправляем вектор желаемого направление движения, если он поменялся
        if vector != old_vector:
            old_vector = vector
            message = "<" + str(vector[0]) + ", " + str(vector[1]) + ">"  # форматируем данные
            sock.send(f"{message}".encode()) #отправляем данные на сервер

    #получаем от сервера новое состояние игрового поля
    data = sock.recv(1024) #читаем данные от сервера
    data = data.decode()

    #рисуем новое состояние игрового поля
    #print(f"{data}")
    screen.fill("gray25")
    pygame.draw.circle(screen, (255, 0, 0), (WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2), 50) #рисуем круг в центре экрана
    pygame.display.update() #обновляем UI игрового поля

pygame.quit() #закрываем окно