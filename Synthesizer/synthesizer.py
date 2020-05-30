"""Синтезатор."""

import re

import pygame.midi
import serial

# Импорты сторонних библиотек
# from serial.tools.list_ports import comports


class Synthesizer:
    """Класс Сиетезатора."""

    def __init__(self):
        """Конструктор класса."""
        # Подготовка окна
        self.window_size = (320, 240)
        self._screen = pygame.display.set_mode(self.window_size)

        # Подготовка COM порта
        self._ser = serial.Serial(
            port='COM17',
            baudrate=9600
        )
        # Считывание установленного порога
        # self.threshold = int(
        #     re.search("d{, 4}", str(self._ser.readline()), flags=re.ASCII))

        # Подготовка миди плеера
        pygame.midi.init()
        self._player = pygame.midi.Output(
            device_id=pygame.midi.get_default_output_id()
        )

        # Установка инструмента
        # 1 - фортепиано
        self._player.set_instrument(
            instrument_id=1
        )

        # Настройка состояний клавиш
        self._KEY_STATE = {
            'C': {
                'key': 'a',
                'key_code': ord('a'),
                'midiNumber': 60,
                'pressed': False,
                'duration': 0
            },
            'D': {
                'key': 's',
                'key_code': ord('s'),
                'note': 'D',
                'midiNumber': 62,
                'pressed': False,
                'duration': 0
            },
            'E': {
                'key': 'd',
                'key_code': ord('d'),
                'midiNumber': 64,
                'pressed': False,
                'duration': 0
            },
            'F': {
                'key': 'f',
                'key_code': ord('f'),
                'note': 'F',
                'midiNumber': 65,
                'pressed': False,
                'duration': 0
            },
            'G': {
                'key': 'g',
                'key_code': ord('g'),
                'note': 'G',
                'midiNumber': 67,
                'pressed': False,
                'duration': 0
            },
            'A': {
                'key': 'h',
                'key_code': ord('h'),
                'note': 'A',
                'midiNumber': 69,
                'pressed': False,
                'duration': 0
            },
            'B': {
                'key': 'j',
                'key_code': ord('j'),
                'note': 'B',
                'midiNumber': 71,
                'pressed': False,
                'duration': 0
            }
        }
        self.running = False

    def start(self):
        """Старт синтезатора."""
        self.running = True
        self._loop()

    def quit(self):
        """Отключение синтезатора."""
        self.running = False

        self._player.close()

        pygame.quit()

    def _loop(self):
        while self.running:
            # Работа  COM портом
            if self._ser.in_waiting > 0:
                # if self._ser.
                # Считываем строку из COM порта
                line = str(self._ser.readline())

                # Ищем в строке A или !A
                note_tags = re.findall('[!]?[A-F]', line, flags=re.ASCII)

                for note_tag in note_tags:
                    if note_tag[0] != '!':
                        self._handle_key_down(note_tag[0])
                    # else:
                        # self._handle_key_up(note_tag[1])
            # Работа с клавишами
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == pygame.QUIT:
                    self.running = False

            #     # Обработка нажатий и отпускания TODO Доделать нажатия
            #     по клавишам
                if event.type == pygame.KEYDOWN:
                    if event.unicode == 'q':
                        self.quit()

                    for note in self._KEY_STATE:
                        if event.unicode == self._KEY_STATE[note]['key']:
                            self._handle_key_down(note)
                # elif event.type == pygame.KEYUP:
                    # self._handle_key_up(event.unicode.upper)

            # Обработка музыки
            self._play_music()

    def _handle_key_down(self, note):
        for key in self._KEY_STATE:
            if note == key:
                self._KEY_STATE[key]['pressed'] = True
                self._KEY_STATE[key]['duration'] = pygame.midi.time()

    # def _handle_key_up(self, note):
    #     for key in self._KEY_STATE:
    #         if note == self._KEY_STATE[key]['key_code']:
    #             self._KEY_STATE[key]['pressed'] = False

    #             self._KEY_STATE[key]['duration'] = (
    #                 pygame.midi.time() - self._KEY_STATE[key]['duration'])

    #             if self._KEY_STATE[key]['duration'] > 127:
    #                 self._KEY_STATE[key]['duration'] = 127

    def _play_music(self):
        """Воспроизведение музыки."""
        # Ппрверка, что не произошел выход из программы.
        if not self.running:
            return
        else:
            # Формирование пакета для воспроизведения
            data = []
            for key in self._KEY_STATE.values():
                if key['pressed'] and key['duration'] != 0:
                    data.append(
                        (
                            (
                                0x90,
                                key['midiNumber'],
                                64
                            ),
                            0
                        )
                    )

            self._player.write(data)

            for key in self._KEY_STATE.values():
                key['duration'] = 0
                key['pressed'] = False


if __name__ == '__main__':
    piano = Synthesizer()
    piano.start()
    piano.quit()
