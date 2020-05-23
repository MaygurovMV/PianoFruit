"""Синтезатор.

"""
# Импорты сторонних библиотек

import pygame.midi


class PianoFruit:

    def __init__(self):
        # Подготовка окна
        self.window_size = (320, 240)
        self._screen = pygame.display.set_mode(self.window_size)

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
            'a': {
                'keyCode': ord('a'),
                'note': 'C',
                'midiNumber': 60,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            's': {
                'keyCode': ord('s'),
                'note': 'D',
                'midiNumber': 62,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            'd': {
                'keyCode': ord('d'),
                'note': 'E',
                'midiNumber': 64,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            'f': {
                'keyCode': ord('f'),
                'note': 'F',
                'midiNumber': 65,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            'g': {
                'keyCode': ord('g'),
                'note': 'G',
                'midiNumber': 67,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            'h': {
                'keyCode': ord('h'),
                'note': 'A',
                'midiNumber': 69,
                'pressed': False,
                'playable': False,
                'duration': 0
            },
            'j': {
                'keyCode': ord('j'),
                'note': 'B',
                'midiNumber': 71,
                'pressed': False,
                'playable': False,
                'duration': 0
            }
        }
        self.running = False

    def start(self):
        self.running = True
        self._loop()
        self.stop()
        return None

    def stop(self):
        self.running = False

        self._player.close()

        pygame.quit()
        return None

    def _loop(self):
        while self.running:
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == pygame.QUIT:
                    self.running = False

                # Обработка нажатий и отпускания
                if event.type == pygame.KEYDOWN:
                    self._handle_key_down(event)
                elif event.type == pygame.KEYUP:
                    self._handle_key_up(event)

                # TODO Обработка музыки
            self._play_music()

        return None

    def _handle_key_down(self, event):
        for key in self._key_state:
            if event.dict['unicode'] == key:
                self._key_state[key]['pressed'] = True
                self._key_state[key]['playable'] = True
                self._key_state[key]['duration'] = pygame.midi.time()

        return None

    def _handle_key_up(self, event):
        for key in self._key_state:
            if event.key == self._key_state[key]['keyCode']:
                self._key_state[key]['pressed'] = False
                self._key_state[key]['duration'] = pygame.midi.time() - self._key_state[key]['duration']
                if self._key_state[key]['duration'] > 127:
                    self._key_state[key]['duration'] = 127
        return None

    def _play_music(self):
        music_playable = True

        # for key in self._key_state.values():
            # if key['playable'] == True:
            #     music_playable = False

        for key in self._key_state.values():
            if not key['pressed'] and key['duration'] != 0:
                self._data.append(
                    (
                        (
                            0x90,
                            key['midiNumber'],
                            64
                            # key['duration']
                        ),
                        0
                        # pygame.midi.time()
                    )
                )

        self._player.write(self._data)
        self._data = []
        return None


if __name__ == '__main__':

    piano = PianoFruit()
    piano.start()
    # # размер окна pygame
    # window_size = 320, 240
    #
    # # настраиваем экран
    # screen = pygame.display.set_mode(window_size)
    # # pygame.display.flip()
    # pygame.midi.init()
    # player = pygame.midi.Output(0)
    # player.set_instrument(0)
    #
    # running = True
    # while running:
    #     # обрабатываем события
    #     for event in pygame.event.get():
    #         # событие закрытия окна
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #         if event.type == pygame.KEYDOWN:
    #             if event.dict['unicode'] == 'q':
    #                 running = False
    #
    # player.close()
    # # pygame.mixer.quit()
    # pygame.midi.quit()
    # # закрываем окно
    # pygame.quit()


