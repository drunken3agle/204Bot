import numpy as np
import random


class Game:
    """Represents a single 2048 game instance"""

    __map = np.zeros((4, 4), dtype=int)
    __tile_count = 0

    score = 0

    def __init__(self):
        """Sets up initial game state with two random tiles"""

        self.__add_tile()
        self.__add_tile()

        state = True
        while state:
            print(self.score)
            print(self.__map)

            action = input()
            while action not in 'wasd':
                action = input()

            if action == 'w':
                state = self.up()
            elif action == 'a':
                state = self.left()
            elif action == 's':
                state = self.down()
            elif action == 'd':
                state = self.right()

        print('You scored:', self.score)

    def __add_tile(self):
        """Adds new tile to game if there is an empty slot"""

        while self.__tile_count < 16:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if self.__map[row][col] == 0:
                self.__map[row][col] = 4 if random.random() < 0.2 else 2
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
        """Shifts/Merges all tiles one tile the right until no more change is happening and adds one new tile
        :returns True if the game can continue, False otherwise"""

        def __iteration() -> bool:
            """Performs a single shift
            :returns True if something changed, False otherwise"""

            changed = False
            for row in range(4):
                for col in range(3):  # Last column can never be shifted to the right so it is ignored
                    # Perform merge if tile on the right is equal
                    if self.__map[row][col] == self.__map[row][col + 1] and self.__map[row][col] != 0:
                        self.__map[row][col] = 0
                        self.__map[row][col + 1] *= 2
                        self.__tile_count -= 1
                        self.score += self.__map[row][col + 1]
                        changed = True
                    # Move tile if tile on the right is empty (aka. 0)
                    elif self.__map[row][col + 1] == 0 and self.__map[row][col] != 0:
                        self.__map[row][col + 1] = self.__map[row][col]
                        self.__map[row][col] = 0
                        changed = True

            return changed

        while __iteration():  # Loop until no more change
            pass

        self.__add_tile()
        return self.__can_continue()

    def up(self) -> bool:
        """Performs a up-shift by transposing, shifting right and transposing again and
        flipping along the horizontal axis
        :returns True if game can continue, False otherwise"""

        self.__map = np.transpose(self.__map)
        res = self.__shift()
        self.__map = np.transpose(self.__map)
        self.__map = np.flipud(self.__map)

        return res

    def down(self) -> bool:
        """Performs a down-shift by transposing, shifting right and transposing again
        :returns True if game can continue, False otherwise"""

        self.__map = np.transpose(self.__map)
        res = self.__shift()
        self.__map = np.transpose(self.__map)
        return res

    def left(self) -> bool:
        """Performs a left-shift by flipping along the vertical axis, shifting right and flipping again
        :returns True if game can continue, False otherwise"""

        self.__map = np.fliplr(self.__map)
        res = self.__shift()
        self.__map = np.fliplr(self.__map)
        return res

    def right(self) -> bool:
        """Performs a right-shift
        :returns True if game can continue, False otherwise"""

        return self.__shift()


if __name__ == '__main__':
    g = Game()
