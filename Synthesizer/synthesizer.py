"""Синтезатор.

Генерируте сэмплы нот.
"""
# Импорты сторонних бибилиотек
# import numpy as np
import pygame
import time
import pygame.midi
from pathlib import Path
from mingus.containers.note import Note
from mingus.midi import midi_file_out

# myself = Path(__file__).resolve()

midi_file_out.write_Note(
    file=Path(__file__).resolve().parents[1] / 'src/audio/noteA.midi',
    note=Note('A')
)


# # Громкость
# VOLUME = 0.010

# # Частота дискретизации
# SAMPLE_RATE = 44100

# # 16-ти битный звук
# S_16BIT = 2 ** 16

# FREQ_ARRAY = np.array(
#     [
#         261.63,  # До - C
#         293.66,  # Ре - D
#         329.63,  # Ми - E
#         349.23,  # Фа - F
#         392.00,  # Соль -G
#         440.00,  # Ля - A
#         493.88  # Си - B
#     ]
# )

# DURATION_TONE = 1 / 4


# def generate_sample(freq, duration, volume):
#     """Генератор сэмплов.

#     Arguments:
#         freq {[type]} -- [description]
#         duration {[type]} -- [description]
#         volume {[type]} -- [description]
#     """
#     # Амплитуда
#     # amplitude = np.round(S_16BIT * volume)
#     amplitude = np.round(S_16BIT * volume)
#     # Длительность генерируемого звука в сэмплах
#     total_samples = np.round(SAMPLE_RATE * duration)

#     # Частоте дискретизации (пересчитанная)
#     w = 2.0 * np.pi * freq / SAMPLE_RATE

#     # Массив сэмплов
#     k = np.arange(0, total_samples)

#     # Массив значений функции (с округлением)
#     return np.round(amplitude * np.sin(k * w))


# def generate_tones(duration, volume):
#     """Функция генерации нот.

#     Arguments:
#         duration {[type]} -- Длительность, с.
#     """
#     tones = []
#     for freq in FREQ_ARRAY:
#         # np.array нужен для преобразования данных под формат 16 бит
#         # (dtype=np.int16)
#         tone = np.array(
#             generate_sample(freq, duration, volume),
#             dtype=np.int16
#         )
#         tones.append(tone)

#     return tones


# if __name__ == '__main__':
#     tones = generate_tones(DURATION_TONE, VOLUME)

#     p = pa.PyAudio()

#     stream = p.open(
#         format=p.get_format_from_width(width=2),
#         channels=2,
#         rate=SAMPLE_RATE,
#         output=True
#     )

#     stream.start_stream()
#     stream.write(tones[1])

#     stream.close()
#     p.terminate()

# pygame.mixer.init()
# noteA = pygame.mixer.Sound('noteA.midi')
pygame.midi.init()
player = pygame.midi.Output(device_id=0)
player.set_instrument(0)
player.note_on(64, 64, 1)
time.sleep(1)
player.note_on(64, 64, 1)
pygame.midi.quit()

# Блок с pygame
# наши клавиши
key_names = ['a', 's', 'd', 'f', 'g', 'h', 'j']

# Коды клавиш
key_list = list(
    # Примеят функцию ко всем элементам последовательнсти
    map(lambda x: ord(x), key_names)
)

# Состояние клавиш (нажато/не нажато)
key_dict = dict([(key, False) for key in key_list])

if __name__ == '__main__':

    # tones = generate_tones(DURATION_TONE, VOLUME)

    # инициализируем
    # p = pa.PyAudio()
 
    # Создаём поток для вывода
    # stream = p.open(format=p.get_format_from_width(width=2),
                    # channels=2, rate=SAMPLE_RATE, output=True)

    # размер окна pygame
    window_size = 320, 240

    # настраиваем экран
    screen = pygame.display.set_mode(window_size)
    pygame.display.flip()

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
                pygame.mixer.music.play()

    pygame.mixer.quit()
    # закрываем окно
    pygame.quit()


