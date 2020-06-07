"""Фруктовое Пианино."""


# Импорт сторонних библиотек
import json
import re
import sys
import os
import pygame
import serial
from time import time, sleep
# Импорт внутренних библиотек
from gui.gui import GUI
from Synthesizer.synthesizer import Synthesizer


class _Game:
    def __init__(self):
        self._get_config()
        self._gui = GUI()
        self._synth = Synthesizer()

    @staticmethod
    def _ch_dir() -> str:
        """[Изменение дирректории src для pyInstaller для exe в одном файле.]

        :return: Путь до директории с исполняемым файлоом.
        :rtype: str
        """
        if getattr(sys, 'frozen', False):
            os.chdir(sys._MEIPASS)
            bundle_dir = sys.executable.replace('piano_Fruit.exe', '')
        else:
            bundle_dir = ''

        return bundle_dir

    def _get_config(self):
        """Взятие настроек из внешнего файла."""
        bundle_dir = self._ch_dir()
        try:
            with open(bundle_dir + 'settings.json') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            self._set_config()

    def _set_config(self):
        """Установка настроек в внешний файл."""
        bundle_dir = self._ch_dir()
        self.config = {
                "COM":
                {
                        "is_COM_enabled": False,
                        "COM": "COM17",
                        "threshold": 1000
                }
            }
        json.dump(
            self.config,
            open(bundle_dir + 'settings.json', 'w')
        )
        self.running = False

    def start(self):
        """
        Arduino threshold setting and Loop starting
        """
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
        """
        Main cycle
        """
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
                    for note in self._synth.notes:
                        if (event.key ==
                                self._synth.notes[note].key_code):
                            self._synth.handle_key_down(note)

                if event.type == pygame.KEYUP:
                    for note in self._synth.notes:
                        if (event.key ==
                                self._synth.notes[note].key_code):
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
                            '[!]?[A-G]',
                            line,
                            flags=re.ASCII
                        )

                        for note_tag in note_tags:
                            if note_tag[0] != '!':
                                self._synth.handle_key_down(note_tag[0])
                            else:
                                self._synth.handle_key_up(note_tag[1])

                self._gui.update(
                    self._synth.notes
                )
                self._synth.play()

    def quit(self):
        self.running = False
        if self.config['COM']['is_COM_enabled']:
            self._ser.close()
        self._synth.close()
        pygame.quit()


if __name__ == "__main__":

    game = _Game()

    game.start()

    game.quit()
