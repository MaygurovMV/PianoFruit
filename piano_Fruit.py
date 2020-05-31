"""Фруктовое Пианино."""

# Импорт сторонних библиотек
import pygame
# from serial.tools.list_ports import comports
import serial
import re

# Импорт внутренних библиотек
from gui.gui import GUI
from Synthesizer.synthesizer import Synthesizer


class _Game:
    def __init__(self):
        self._gui = GUI()
        self.is_COM_enabled = False
        self._synth = Synthesizer()

        self.running = False

    def start(self):
        self.running = True

        if self.is_COM_enabled:
            # Подготовка COM порта
            self._ser = serial.Serial(port='COM17', baudrate=9600)

            # Считывание установленного порога
            # self.threshold = int(
            #     re.search(
            #         "d{, 4}",
            #         str(self._ser.readline()),
            #         flags=re.ASCII))

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
                if self.is_COM_enabled:
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
                                self._synth._handle_key_up(note_tag[1])

                self._gui.update(
                    self._synth.key_state
                )
                self._synth.play()

    def quit(self):
        self.running = False
        if self.is_COM_enabled:
            self._ser.close()
        self._synth.close()
        pygame.quit()


game = _Game()

game.start()

game.quit()
