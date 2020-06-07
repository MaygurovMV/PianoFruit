"""Фруктовое Пианино."""


# Импорт сторонних библиотек
import configparser
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
        self.running = True
        self._get_config()
        self._gui = GUI()
        self._synth = Synthesizer()

    @staticmethod
    def _ch_dir() -> str:
        """Изменение дирректории src для pyInstaller для exe в одном файле.

        :return: Путь до директории с исполняемым файлом.
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
        config = configparser.ConfigParser()

        if len(config.read(bundle_dir + 'settings.ini',
                           encoding='utf8')) != 0:
            self.config = config
        else:
            self._set_config()

    def _set_config(self):
        """Установка настроек в внешний файл."""
        bundle_dir = self._ch_dir()
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        config['COM'] = {
            '# Доступен ли COM порт': None,
            'is_COM_enabled': False,
            '\n# Номер COM порта.\n' +
            '# Для поиска номера воспользуйтесь диспетчером устройств': None,
            'COM': 'COM17',
            '\n# Порог для считывания нажатий \n' +
            '# От 0 - ловит ничего, до 1023 - ловит все': None,
            'threshold': 1000
        }
        self.config = config

        with open(bundle_dir + 'settings.ini', 'w',
                  encoding='utf8') as config_file:
            config.write(config_file)
        self.running = False

    def start(self):
        """Arduino threshold setting and Loop starting."""
        if self.config['COM'].getboolean('is_COM_enabled'):
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
        """Start main cycle."""
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
                                note.key_code):
                            self._synth.handle_key_down(note.name)

                if event.type == pygame.KEYUP:
                    for note in self._synth.notes:
                        if (event.key ==
                                note.key_code):
                            self._synth.handle_key_up(note.name)

            if self.running:
                if self.config['COM'].getboolean('is_COM_enabled'):
                    # Работа  COM портом
                    if self._ser.in_waiting > 0:
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
        if self.config['COM'].getboolean('is_COM_enabled'):
            self._ser.close()
        self._synth.close()
        pygame.quit()


if __name__ == "__main__":

    game = _Game()

    game.start()

    game.quit()
