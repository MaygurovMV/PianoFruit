"""Синтезатор.

Генерируте сэмплы нот.
"""
# Импорты сторонних бибилиотек

import pygame.midi

# Блок с pygame
# наши клавиши
key_names = ('a', 's', 'd', 'f', 'g', 'h', 'j')
midi_number = (60, 62, 64, 65, 67, 69, 71)

# Коды клавиш
key_list = list(
    # Примеят функцию ко всем элементам последовательнсти
    map(lambda x: ord(x), key_names)
)

# Состояние клавиш (нажато/не нажато)
key_dict = dict([(key, False) for key in key_list])

if __name__ == '__main__':

    # размер окна pygame
    window_size = 320, 240

    # настраиваем экран
    screen = pygame.display.set_mode(window_size)
    pygame.display.flip()
    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)

    running = True
    while running:
        # обрабатываем события
        for event in pygame.event.get():
            # событие закрытия окна
            if event.type == pygame.QUIT:
                running = False
            # нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    running = False
                # обрабатываем нажатые клавиши по списку key_list
                for (index, key) in enumerate(key_list):
                    if event.key == key:
                        # зажимаем клавишу
                        key_dict[key] = True
            # отпускание клавиш
            if event.type == pygame.KEYUP:
                for (index, key) in enumerate(key_list):
                    if event.key == key:
                        # отпускаем клавишу
                        key_dict[key] = False
        # обрабатываем нажатые клавиши
        for (index, key) in enumerate(key_list):
            # если клавиша нажата
            if key_dict[key]:
                # то выводим звук на устройство
                player.note_on(midi_number[index], 64)

    player.close()
    # pygame.mixer.quit()
    pygame.midi.quit()
    # закрываем окно
    pygame.quit()


