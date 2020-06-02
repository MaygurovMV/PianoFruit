"""Фруктовое Пианино."""

import json
import re
from os.path import exists

# Импорт сторонних библиотек
import pygame
import serial
from time import time, sleep
# Импорт внутренних библиотек
from gui.gui import GUI
from Synthesizer.synthesizer import Synthesizer


def serial_write(ser, phrase):
    ser.write(phrase.encode('utf8'))
    start_time = time()
    try:
        while True:
            data = ser.readline().decode('utf8')
            if data != '':
                return data
            sleep(0.01)
            if time() - start_time > 2:
                return 'Time out'
    except KeyboardInterrupt:
        print('прервано пользователем')


class _Game:
    def __init__(self):
        self._gui = GUI()

        with open('settings.json') as config_file:
            self.config = json.load(config_file)

        self._synth = Synthesizer()

        self.running = False

    def start(self):
        self.running = True

        if self.config['COM']['is_COM_enabled']:
            # Подготовка COM порта
            self._ser = serial.Serial(
                port=self.config['COM']['COM'],
                baudrate=9600
            )
            # Ожидание загрузки bootloader-а
            pygame.time.wait(1700)

            self._ser.write(
                (str(self.config['COM']['threshold'])).encode('utf-8')
            )

            print('threshold = ', self._ser.readline())

        self._clock = pygame.time.Clock()

        # Старт петли
        self._loop()

    def _loop(self):
        while self.running:
            self._clock.tick(30)
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == pygame.QUIT:
                    self.quit()

                # Работа с клавишами
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('q'):
                        self.quit()

                    # Обработка нажатий и отпускания.
                    for note in self._synth.key_state:
                        if (event.key ==
                                self._synth.key_state[note]['key_code']):
                            self._synth.handle_key_down(note)

                if event.type == pygame.KEYUP:
                    for note in self._synth.key_state:
                        if (event.key ==
                                self._synth.key_state[note]['key_code']):
                            self._synth.handle_key_up(note)

            if self.running:
                if self.config['COM']['is_COM_enabled']:
                    # Работа  COM портом
                    if self._ser.in_waiting > 0:
                        # if self._ser.
                        # Считываем строку из COM порта
                        line = str(self._ser.readline())

                        # Ищем в строке A или !A
                        note_tags = re.findall(
                            '[!]?[A-F]',
                            line,
                            flags=re.ASCII
                        )

                        for note_tag in note_tags:
                            if note_tag[0] != '!':
                                self._synth.handle_key_down(note_tag[0])
                            else:
                                self._synth.handle_key_up(note_tag[1])

                self._gui.update(
                    self._synth.key_state
                )
                self._synth.play()

    def quit(self):
        self.running = False
        if self.config['COM']['is_COM_enabled']:
            self._ser.close()
        self._synth.close()
        pygame.quit()


game = _Game()

game.start()

game.quit()
