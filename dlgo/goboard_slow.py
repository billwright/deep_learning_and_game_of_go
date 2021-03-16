class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign    # One and only one of these is true
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, stone):
        try:
            self.liberties.remove(stone)
        except KeyError as err:
            pass    # Liberty was already removed

    def add_liberty(self, stone):
        self.liberties.add(stone)

    def merge(self, other_string):
        assert self.color == other_string.color
        combined_stones = self.stones | other_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | other_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self.is_empty(point)

        adjacent_same_color = []
        adjacent_different_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(point):
                continue
            neighbor_string = self.get_go_string(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                adjacent_same_color.append(neighbor_string)
            else:
                adjacent_different_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merge(same_color_string)
        for new_string_point in new_string.stones:
            self.put(new_string_point, new_string)
        for other_color_string in adjacent_different_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_different_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def _remove_string(self, go_string):
        for point in go_string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self.get_go_string(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not go_string:
                    neighbor_string.add_liberty(point)
            self.put(point, None)

    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get_go_string(self, point):
        return self._grid.get(point)

    def get(self, point):
        go_string = self.get_go_string(point)
        if go_string is None:
            return None
        return go_string.color

    def put(self, point, go_string):
        self._grid[point] = go_string

    def is_empty(self, point):
        return self.get(point) is None