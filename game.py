import numpy as np
import tkinter as tk
import random
import keyboard


class Game:
    """Represents a single 2048 game instance"""

    __map = np.zeros((4, 4), dtype=int)
    __tile_count = 0

    score = 0

    def __init__(self):
        """Sets up initial game state with two random tiles"""

        self.__add_tile()
        self.__add_tile()

    def __add_tile(self):
        """Adds new tile to game if there is an empty slot"""

        while self.__tile_count < 16:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if self.__map[row][col] == 0:
                self.__map[row][col] = 4 if random.random() < 0.1 else 2
                self.__tile_count += 1
                break

    def __can_continue(self) -> bool:
        """Checks if the player can make another move
        :returns True if a move is possible, False otherwise"""

        if self.__tile_count < 16:  # Game can always continue if there is an empty tile
            return True

        for row in range(4):
            for col in range(4):
                # Game can continue if a pair of vertical or horizontal neighbors is equal
                if (row > 0 and self.__map[row - 1][col] == self.__map[row][col]) or \
                   (row < 3 and self.__map[row + 1][col] == self.__map[row][col]) or \
                   (col > 0 and self.__map[row][col - 1] == self.__map[row][col]) or \
                   (col < 3 and self.__map[row][col + 1] == self.__map[row][col]):
                    return True

        return False

    def __shift(self) -> bool:
        """Shifts/Merges all tiles one tile the right until no more change is happening and
        adds one new tile if anything has changed
        :returns True if the game can continue, False otherwise"""

        def __iteration() -> bool:
            """Performs a single shift
            :returns True if something changed, False otherwise"""

            _changed = False
            merge_list = list()
            for row in range(4):
                for col in range(3)[::-1]:  # Last column can never be shifted to the right so it is ignored
                    # Perform merge if tile on the right is equal
                    if self.__map[row][col] == self.__map[row][col + 1] and self.__map[row][col] != 0 and \
                            (row, col) not in merge_list:
                        self.__map[row][col] = 0
                        self.__map[row][col + 1] *= 2
                        self.__tile_count -= 1
                        self.score += self.__map[row][col + 1]
                        _changed = True
                        merge_list.append((row, col))
                    # Move tile if tile on the right is empty (aka. 0)
                    elif self.__map[row][col + 1] == 0 and self.__map[row][col] != 0:
                        self.__map[row][col + 1] = self.__map[row][col]
                        self.__map[row][col] = 0
                        _changed = True

            return _changed

        change_count = 0
        while True:  # Loop until no more change
            changed = __iteration()
            if changed:  # Count changes to check if a tile needs to be added
                change_count += 1
            else:
                break

        if change_count > 0:  # Check if a tile has been moved and add a new tile
            self.__add_tile()

        return self.__can_continue()

    def value_at(self, x: int, y: int) -> int:
        """Returns the value of the tile at position (x, y)
        :param x X coordinate
        :param y Y coordinate
        :returns value of tile at (x, y)
        :raises Index error if index > 3 is passed"""

        if x not in range(4) or y not in range(4):
            raise IndexError()

        return self.__map[x][y]

    def up(self) -> bool:
        """Performs a up-shift by rotating left thrice, shifting right and rotating once more
        :returns True if game can continue, False otherwise"""

        self.__map = np.rot90(self.__map, k=3)
        res = self.__shift()
        self.__map = np.rot90(self.__map)
        return res

    def down(self) -> bool:
        """Performs a down-shift by rotating left once, shifting right and rotating thrice
        :returns True if game can continue, False otherwise"""

        self.__map = np.rot90(self.__map)
        res = self.__shift()
        self.__map = np.rot90(self.__map, k=3)
        return res

    def left(self) -> bool:
        """Performs a left-shift by rotating left twice, shifting right and rotating twice again
        :returns True if game can continue, False otherwise"""

        self.__map = np.rot90(self.__map, k=2)
        res = self.__shift()
        self.__map = np.rot90(self.__map, k=2)
        return res

    def right(self) -> bool:
        """Performs a right-shift
        :returns True if game can continue, False otherwise"""

        return self.__shift()


class Main(tk.Frame):
    """GUI for the game"""

    __game = Game()  # current game instance
    __game_running = True

    def __init__(self, master=None):
        """Initiates a 5x4 grid with the game map in the bottom 4x4 fields and the score in the top right.
        Keyboard capture is also started"""

        super().__init__(master)
        self.master = master
        self.pack()

        self.__tiles = [tk.Label(self) for _ in range(16)]
        self.__scoreboard = tk.Label(self)
        self.__create_window()
        self.__update()

        keyboard.on_press(self.__handle_input, suppress=True)

    def __create_window(self):
        """Sets up the window layout"""

        for x in range(4):
            for y in range(4):
                self.__tiles[4 * x + y].grid(row=x+1, column=y)

        self.__scoreboard.grid(row=0, column=3)

    def __update(self):
        """Updates all 16 tiles and the score with their current values"""

        for x in range(4):
            for y in range(4):
                self.__tiles[4 * x + y]['text'] = self.__game.value_at(x, y)

        self.__scoreboard['text'] = self.__game.score

    def __handle_input(self, key_event: keyboard.KeyboardEvent):
        """Manages the keyboard controls for the game
        WASD or arrow keys can be used for control, escape to end the game
        :param key_event latest key press by the user"""

        if key_event.name in ['w', 'up']:
            self.__game_running = self.__game.up()
        elif key_event.name in ['a', 'left']:
            self.__game_running = self.__game.left()
        elif key_event.name in ['s', 'down']:
            self.__game_running = self.__game.down()
        elif key_event.name in ['d', 'right']:
            self.__game_running = self.__game.right()
        elif key_event.name is 'esc':
            self.__game_running = False

        self.__update()

        if not self.__game_running:
            keyboard.unhook_all()
            self.quit()
            print('You got', self.__game.score, 'points!')


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(master=root)
    app.mainloop()
