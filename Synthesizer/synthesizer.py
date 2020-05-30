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
        self._player.set_instrument(
            instrument_id=1
        )
        self._data = []

        # Настройка состояний клавиш
        self._key_state = {
            'C': {
                'key': 'a',
                'keyCode': ord('a'),
                'midiNumber': 60,
                'pressed': False,
                'duration': 0
            },
            'D': {
                'key': 's',
                'keyCode': ord('s'),
                'note': 'D',
                'midiNumber': 62,
                'pressed': False,
                'duration': 0
            },
            'E': {
                'key': 'd',
                'keyCode': ord('d'),
                'midiNumber': 64,
                'pressed': False,
                'duration': 0
            },
            'F': {
                'key': 'f',
                'keyCode': ord('f'),
                'note': 'F',
                'midiNumber': 65,
                'pressed': False,
                'duration': 0
            },
            'G': {
                'key': 'g',
                'keyCode': ord('g'),
                'note': 'G',
                'midiNumber': 67,
                'pressed': False,
                'duration': 0
            },
            'A': {
                'key': ' h',
                'keyCode': ord('h'),
                'note': 'A',
                'midiNumber': 69,
                'pressed': False,
                'duration': 0
            },
            'B': {
                'key': 'j',
                'keyCode': ord('j'),
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
        self.quit()
        # return None

    def quit(self):
        """Отключение синтезатора."""
        self.running = False

        self._player.close()

        pygame.quit()
        # return None

    def _loop(self):
        while self.running:
            if self._ser.in_waiting > 0:
                # Считываем строку из COM порта
                line = str(self._ser.readline())

                # Ищем в строке A или !A
                note_tags = re.findall('[!]?[A-F]', line, flags=re.ASCII)

                for note_tag in note_tags:
                    if note_tag[0] != '!':
                        self._handle_key_down(note_tag[0])
                    else:
                        self._handle_key_up(note_tag[1])
                for event in pygame.event.get():
                    # Обработка выхода
                    if event.type == pygame.QUIT:
                        self.running = False

                #     # Обработка нажатий и отпускания TODO Доделать нажатия
                #     по клавишам
                #     if event.type == pygame.KEYDOWN:
                #         self._handle_key_down(event.unicode.upper)
                #     elif event.type == pygame.KEYUP:
                #         self._handle_key_up(event.unicode.upper)

                # Обработка музыки
                self._play_music()

        # return None

    def _handle_key_down(self, note):
        for key in self._key_state:
            if note == key:
                self._key_state[key]['pressed'] = True
                self._key_state[key]['duration'] = pygame.midi.time()

        # return None

    def _handle_key_up(self, note):
        for key in self._key_state:
            if note == self._key_state[key]['keyCode']:
                self._key_state[key]['pressed'] = False

                self._key_state[key]['duration'] = (
                        pygame.midi.time() - self._key_state[key]['duration'])

                if self._key_state[key]['duration'] > 127:
                    self._key_state[key]['duration'] = 127
        # return None

    def _play_music(self):

        # Формирование пакета для воспроизведения
        for key in self._key_state.values():
            if key['pressed'] and key['duration'] != 0:
                self._data.append(
                    (
                        (
                            0x90,
                            key['midiNumber'],
                            64
                        ),
                        0
                    )
                )

        self._player.write(self._data)
        self._data = []

        for key in self._key_state.values():
            key['duration'] = 0
            key['pressed'] = False
        # return None


if __name__ == '__main__':

    piano = Synthesizer()
    piano.start()
