"""Графический интерфейс пользователя."""
import pygame
import pygame.freetype


class GUI:
    """Графический интерфейс пользователя."""

    def __init__(self):
        """Конструктор класса."""
        pygame.init()
        # Подготовка окна
        self.window_size = (1920 * 3 // 5, 1080 * 3 // 5)
        self._screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Фруктовое пианино")

        self._font = pygame.freetype.SysFont(
            'Comic Sans MS',
            size=26,
        )
        # Загрузка картинки клавиатуры
        keyboard_image = pygame.image.load(
            'gui\\src\\images\\Keyboard.png').convert_alpha()
        self._keyboard_image = {
            'image': keyboard_image,
            'pos': (245, 216)
        }

        left_key = pygame.image.load(
            'gui\\src\\images\\Left key.png').convert_alpha()
        midle_key = pygame.image.load(
            'gui\\src\\images\\Midle key.png').convert_alpha()
        right_key = pygame.image.load(
            'gui\\src\\images\\Right key.png').convert_alpha()

        # Словарь изображений клавиш
        self._key_images = {
            'C': {
                'key_up': left_key.copy(),
                'key_down': self._recolor(
                    left_key.copy(),
                    pygame.Color(255, 0, 0, 100)
                ),
                'text': 'До',
                'text_size': 30,
                'pos': (249, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            },
            'D': {
                'key_up': midle_key.copy(),
                'key_down': self._recolor(
                    midle_key.copy(),
                    pygame.Color(0, 255, 0, 100)
                ),
                'text': 'Ре',
                'text_size': 30,
                'pos': (343, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            },
            'E': {
                'key_up': right_key.copy(),
                'key_down': self._recolor(
                    right_key.copy(),
                    pygame.Color(0, 0, 255, 100)
                ),
                'text': 'Ми',
                'text_size': 30,
                'pos': (437, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            },
            'F': {
                'key_up': left_key.copy(),
                'key_down': self._recolor(
                    left_key.copy(),
                    pygame.Color(0, 255, 255, 100)
                ),
                'text': 'Фа',
                'text_size': 30,
                'pos': (531, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            },
            'G': {
                'key_up': midle_key.copy(),
                'key_down': self._recolor(
                    midle_key.copy(),
                    pygame.Color(255, 0, 255, 100)
                ),
                'text': 'Соль',
                'text_size': 30,
                'pos': (622, 220),
                'pos_text': (-(622 - 634), 500 - 220)
            },
            'A': {
                'key_up': midle_key.copy(),
                'key_down': self._recolor(
                    midle_key.copy(),
                    pygame.Color(255, 255, 0, 100)
                ),
                'text': 'Ля',
                'text_size': 30,
                'pos': (716, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            },
            'B': {
                'key_up': right_key.copy(),
                'key_down': self._recolor(
                    right_key.copy(),
                    pygame.Color(255, 47, 0, 100)
                ),
                'text': 'Си',
                'text_size': 30,
                'pos': (811, 220),
                'pos_text': (-(249 - 275), 500 - 220)
            }
        }
        # Рендер теста поверх клавиш
        for note, note_data in self._key_images.items():
            self._keyboard_image.update(
                {
                    note:
                        {
                            'key_up': self._font.render_to(
                                note_data['key_up'],
                                note_data['pos_text'],
                                note_data['text'],
                                size=note_data['text_size']
                            ).copy(),

                            'key_down': self._font.render_to(
                                note_data['key_down'],
                                note_data['pos_text'],
                                note_data['text'],
                                size=note_data['text_size']
                            ).copy(),
                        }
                }
            )

    # def _rescale(self, obj, scale):
    #     """Масштабирование объектов.

    #     :param obj: Объект для масштабирования.
    #     :type obj: Surface
    #     :return: Объект после масштабирования
    #     :rtype: Surface
    #     """
    #     return pygame.transform.scale(
    #         obj,
    #         (
    #             round(obj.get_width() * scale),
    #             round(obj.get_height() * scale),
    #         )
    #     )

    def _recolor(self, surface, color):
        pxarray = pygame.PixelArray(surface)
        width, height = pxarray.shape
        for i in range(width):
            for j in range(height):
                if pxarray[i, j] == surface.map_rgb((255, 255, 255)):
                    pxarray[i, j] = color

        return pxarray.make_surface()

    def update(self, key_state):
        """Обновление GUI."""
        self._screen.fill((255, 255, 255))
        self._screen.blit(
            self._keyboard_image['image'],
            self._keyboard_image['pos']
        )

        for note in key_state:
            if note.pressed:
                self._screen.blit(
                    self._key_images[note.name]['key_down'],
                    self._key_images[note.name]['pos']
                )
            else:
                self._screen.blit(
                    self._key_images[note.name]['key_up'],
                    self._key_images[note.name]['pos']
                )

        pygame.display.flip()


if __name__ == "__main__":
    pass
