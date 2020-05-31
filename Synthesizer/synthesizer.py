"""Синтезатор."""

# Импорты сторонних библиотек
import pygame.midi


class Synthesizer:
    """Класс Сиетезатора."""

    def __init__(self):
        """Конструктор класса."""
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
        self.key_state = {
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

    def close(self):
        """Отключение синтезатора."""
        self._player.close()

    def handle_key_down(self, note):
        """Обработчик нажатий клавиш.

        :param note: нота
        :type note: str
        """
        for key in self.key_state:
            if note == key:
                self.key_state[key]['pressed'] = True
                self.key_state[key]['duration'] = pygame.midi.time()

    def handle_key_up(self, note):
        """Обработчик отжатий клавиш.

        :param note: Нота
        :type note: str
        """
        for key in self.key_state:
            if note == key:
                self.key_state[key]['pressed'] = False
                self.key_state[key]['duration'] = (
                    pygame.midi.time() - self.key_state[key]['duration'])

                # if self.key_state[key]['duration'] > 127:
                #     self.key_state[key]['duration'] = 127

    def play(self):
        """Воспроизведение музыки."""
        # Формирование пакета для воспроизведения
        data = []
        for key in self.key_state.values():
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

        for key in self.key_state.values():
            key['duration'] = 0
            # key['pressed'] = False


if __name__ == '__main__':
    piano = Synthesizer()
    piano.start()
    piano.quit()
