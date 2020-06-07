"""Синтезатор."""

# Импорты сторонних библиотек
import pygame.midi


class Note:
    """Note Container."""

    def __init__(self, *, name: str, key: str, midi_number: int):
        self.name = name
        self.key = key.lower()
        self.key_code = ord(key)
        self.midiNumber = midi_number
        self.pressed = False
        self.duration = 0

    def press(self):
        if self.pressed is False:
            self.pressed = True
            self.duration = pygame.midi.time()
        else:
            self.pressed = False
            self.duration = pygame.midi.time() - self.duration

    def __repr__(self):
        return f'Note "{self.name}". Pressing by key "{self.key}". Has midiNumber: {self.midiNumber}'


class Notes:
    def __init__(self, *notes):
        self._notes_names = {note.name: note for note in notes}  # Use note.key if using note's key instead note's name

    def key_down(self, note_name: str):
        """Обработчик нажатий клавиш.
        :param note_name: Нота
        """
        # self._notes_names[key_pressed].pressed = True
        # self._notes_names[key_pressed].duration = pygame.midi.time()

        self[note_name].press()

    def key_up(self, note_name: str):
        """Обработчик отжатий клавиш.
        :param note_name: Нота
        """

        self[note_name].press()

    def reset(self):
        """
        Resets all notes
        """
        for note in self:
            note.duration = 0

    def __getitem__(self, note_name: str) -> Note:
        """
        Return note based on name. Use indices (e.g Notes['A'])
        :param note_name:
        :return: Note
        """
        # note_name = note_name.lower()
        if self._notes_names.get(note_name.name, False):
            return self._notes_names[note_name.name]
        else:
            raise KeyError

    def __setitem__(self, key, value):
        """Установка дополнительных нот. Не поддерживается.

        Setting is not available (encapsulation bitch!)
        P.S. Just an example. You may delete this method
        """
        raise KeyError

    def __iter__(self) -> iter:
        """Return iterator of notes.

        :return:
        """
        return iter(self._notes_names.values())


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

        # Настройка нот
        self.notes = Notes(
            Note(name='C', key='a', midi_number=60),
            Note(name='D', key='s', midi_number=62),
            Note(name='E', key='d', midi_number=64),
            Note(name='F', key='f', midi_number=65),
            Note(name='G', key='g', midi_number=67),
            Note(name='A', key='h', midi_number=69),
            Note(name='B', key='j', midi_number=71)
        )

    def close(self):
        """Отключение синтезатора."""
        self._player.close()

    def handle_key_down(self, note):
        """Обработчик нажатий клавиш.

        :param note: нота
        :type note: str
        """
        self.notes.key_down(note)

    def handle_key_up(self, note):
        """Обработчик отжатий клавиш.

        :param note: Нота
        :type note: str
        """
        self.notes.key_up(note)

    def play(self):
        """Воспроизведение музыки."""
        # Формирование пакета для воспроизведения
        data = []
        for note in self.notes:
            if note.pressed and note.duration != 0:
                data.append(
                    (
                        (
                            0x90,
                            note.midiNumber,
                            64
                        ),
                        0
                    )
                )
        self._player.write(data)

        self.notes.reset()
            # key['pressed'] = False


if __name__ == '__main__':
    piano = Synthesizer()
    piano.start()
    piano.quit()
