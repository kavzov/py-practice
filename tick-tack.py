"""
Console version of tick-tack toe.
It written not for descovering new trend of artificial intelligence development.
It has intelligence mismatches, and there are many ways to improve it.
But the game written just for Python practice.
"""
import random, time


class Player:
    """ Common class for human and machine classes """
    def __init__(self, name):
        self.name = name
        self.moves = []
        self.sign = ""
        self.win_combs = []


    def make_move(self, game, board):
        pass


    def set_win_combs(self, game, move):
        """ Check after every move win combinations.
            If a combination has moves of different players,
            this comb excluded from game win_combs list and from win_combs of a player that has the comb in his win_combs
            If a comb has a move of only one player, comb included into win_combs of the player.
            If the comb already exists in player win_combs, it does nothing
        """
        opponent = game.opp_player(self)
        win_combs = game.win_combs[:]       # copy necessary because making iteration at list
        for comb in win_combs:              #   and removing items from it (*) at the same time
            if comb in self.win_combs:      #   generates hard detected mistake
                continue
            if move in comb:
                if comb in opponent.win_combs:
                    opponent.win_combs.remove(comb)
                    game.win_combs.remove(comb)       # (*)
                else:
                    self.win_combs.append(comb)


    def pre_win(self, n_matches):
        """ Calculate either player has a prewin situation.
            (Yet it is 1 move till win)
            If it is, return anonymous dict with
            1) 'comb' -- winnig combination
            2) 'moves' -- moves player made in this combination
            n_matches -- number of necessary matches
        """
        def matches(moves, comb):
            """ Recursive function check every move of a player for a match to win comb,
                and place every match move into 'match_moves' list
            """
            nonlocal match_moves

            try:                         # no more player moves
                elem = moves[-1]
            except IndexError:
                return None

            if elem in comb and elem not in match_moves:
                match_moves.append(elem)
            matches(moves[:-1], comb)

        combs = self.win_combs
        moves = self.moves
        match_moves = []                 # it accumalates moves that match the win_comb

        for comb in combs:
            matches(moves, comb)
            # if matches == necess num, return this comb and player moves in this comb
            ## maybe it is enough to return only a move to win 
            if len(match_moves) >= n_matches:       # ''>='' no matter. It was necess for tests. In a real situation enough '==''
                return {'comb': comb, 'moves': match_moves}
            match_moves = []             # clear if num of moves < n_matches for process next comb

# --------- class Player --------- #
# -------------------------------- #


class Human(Player):
    """ Human """
    def make_move(self, game, board):
        """  """
        pos = None
        while pos not in game.moves:
            try:
                pos = int(input("Make your move, {}: ".format(self.name)))
                if pos == 0: quit()
                pos -= 1
            except ValueError:
                continue
        return pos

# --------- class Human --------- #
# ------------------------------- #


class Machine(Player):
    """ Machine """
    def make_move(self, game, board):
        """ Make move of machine player.
            Use simple intelligence
        """
        print("{} making a move...".format(self.name))
        time.sleep(random.random())                           # imitation of machine thinking
        pos = None
        if not self.moves:                                    # if it is first
            if board.center and board.center_is_free(game):   # if it is center and it's free
                if self.probab(75):                           # in 75% cases
                    pos = board.center                        # select center
                    board.center = None
                else:                                         # in 25% cases
                    pos = board.get_free_angle(game)          # select one of angles
            else:                                             # if no center (busy or dim - even)
                pos = board.get_free_angle(game)              # select one of angles
        else:                                                 # if it is second/further move
            pre_win_sit = self.pre_win(board.dim-1)
            if pre_win_sit:                                   # if one move to win, do this move
                pos = list(set(pre_win_sit['comb']) - set(pre_win_sit['moves']))[0]
            else:
                # prevent opponent win
                opponent = game.opp_player(self)
                opp_pre_win = opponent.pre_win(board.dim-1)
                if opp_pre_win:
                    pos = list(set(opp_pre_win['comb']) - set(opp_pre_win['moves']))[0]
                # go for win
                else:
                    rand_win_comb = self.get_win_comb()                # select random win comb
                    pos = self.get_move_from_win_comb(rand_win_comb)   # select move from the comb
        return pos


    def probab(self, prob):
        """ Return True approx in prob% cases """
        prob = 1 - prob/100
        if random.random() > prob:
            return True


    def get_win_comb(self):
        """ Random select a win comb """
        return random.choice(self.win_combs)


    def get_move_from_win_comb(self, win_comb):
        """ return move in win_comb to win """
        estimated_moves = []
        # accumalate moves estimated for win
        for move in win_comb:
            if move not in self.moves:
                estimated_moves.append(move)
        # for move in estimated_moves:
        return random.choice(estimated_moves)

# --------- class Machine --------- #
# --------------------------------- #


class Board:
    """ Board """
    dim = 3                    # board dimension (3x3, 4x4,..., nxn, n >= 3)
    n_cells = dim ** 2         # total number of cells in board

    def __init__(self):

        self.hLine_sym = "-"
        self.vLine_sym = "|"
        self.cross_sym = "+"

        self.cell_size = 3              # size of single cell (3x3, 5x5,...,nxn, n >= 3, n - odd)
        self.blank_sym = " "

        self.center = self.set_center()
        self.angles = self.set_angles()

        self.values = [self.blank_sym for i in range(self.n_cells)]
        # values = [blank_sym for i in range(n_cells)], in case when 'blank_sym' like static const (not in __init__)
        # doesn't work inside of class -- NameError: name 'blank_sym' is not defined --
        # use of 'self.blank_sym' or 'Board.blank_sym': -- NameError: name 'self' is not defined -- or -- NameError: name 'Board' is not defined --
        # bug of 3+, but it works in 2.7
        # (2017-02-05) full explanation of and how to workaround it at http://stackoverflow.com/questions/13905741/accessing-class-variables-from-a-list-comprehension-in-the-class-definition
        # self.values = (lambda sym=self.blank_sym, num=self.n_cells: [sym for i in range(num)])()    # initital (blank) values of board cells


    def set_center(self):
        """ Return center of board if it is poosible (odd board dimension) """
        if self.dim % 2 != 0:
            return self.n_cells // 2


    def center_is_free(self, game):
        """ Check either the center of board is free or no"""
        if self.center in game.moves:
            return True


    def set_angles(self):
        """ Return all angles indexes of the board """
        angles = [0]                              # left top
        angles += [self.dim - 1]                  # right top
        angles += [self.n_cells - self.dim]       # left bottom
        angles += [self.n_cells - 1]              # right bottom
        return angles


    def get_free_angle(self, game):
        """ Return random free angle """
        free_angles = []

        for angle in self.angles:
            if angle in game.moves:
                free_angles.append(angle)
        print(self.values)
        if free_angles:
            return random.choice(free_angles)


    def draw(self):
        """ Draw full board with values """
        self.draw_horiz_line()
        # draw dim rows
        for row_num in range(self.dim):
            row_start_index = row_num * self.dim
            cell_range = range(row_start_index, row_start_index + self.dim)
            row_values = [self.values[i] for i in cell_range]
            self._draw_board_row(row_values)


    def draw_horiz_line(self):
        """ Draw horizontal line of 'hLine_sym' and 'cross_sym' nodes """
        line = self.cross_sym
        for i in range(self.dim):
            line += self.hLine_sym * self.cell_size
            line += self.cross_sym
        print(line)


    def is_middle(self, num, cell_size):
        """ Check index 'num' for middle positon of cell_size """
        if num == cell_size // 2:
            return True


    def _draw_board_row(self, raw_values):
        """ Draw single row of Board.
            It consists of cell_size lines.
            Line with 'raw_values' is in the vertical middle of row
        """
        for line in range(self.cell_size):
            if self.is_middle(line, self.cell_size):
                self.draw_line(raw_values)
            else:
                self.draw_blank_line()
        self.draw_horiz_line()


    def draw_line(self, line_values):
        """ Draw a line inside of row with values 'line_values' """
        line = self.vLine_sym
        for cell in range(self.dim):
            for point in range(self.cell_size):
                if self.is_middle(point, self.cell_size):    # if point in horizontal middle of cell
                    line += line_values[cell]                 # put value
                else:
                    line += self.blank_sym                    # put blank symbol
            line += self.vLine_sym
        print(line)


    def draw_blank_line(self):
        """ Draw blank line in row
            It is line (draw_line()) with 'blank_sym' values
        """
        blank_line_values = [self.blank_sym for i in range(self.dim)]
        self.draw_line(blank_line_values)

# --------- class Board --------- #
# --------------------------------#


class Game:
    """ Game """
    def __init__(self):
        self.signs = ('x', 'o')
        self.moves = [i for i in range(Board.n_cells)]    # available players moves. It will be popped once per move.
        self.players = []
        self.win_combs = []
        self.get_win_combs(Board.dim, Board.n_cells)

    def get_win_combs(self, dim, n_cells):
        """ Calculates winning combinations """
        # horizontal combs
        for i in range(0, n_cells, dim):
            comb = []
            for j in range(dim):
                comb.append(i)
                i += 1
            self.win_combs.append(comb)

        # vertival combs
        for i in range(dim):
            comb = []
            for j in range(dim):
                comb.append(i)
                i += dim
            self.win_combs.append(comb)

        # diag \
        comb = [(dim+1)*i for i in range(dim)]
        self.win_combs.append(comb)

        # diag /
        comb = [(dim-1)*(i+1) for i in range(dim)]
        self.win_combs.append(comb)


    def set_que(self, players):
        """ Purpose to select who will make first move.
            Default game.players == [man, comp].
            If comp will first, swap players.
        """
        first_player = None
     
        print("Who will first?")
        print("Human - 1")
        print("Machine - 2")

        while first_player not in (1, 2):
            try:
                first_player = int(input("Input 1 or 2: "))
            except ValueError:
                continue
        if first_player == 2:
            self.swap_que(players)


    def swap_que(self, players):
        """ Swap players in player list.
            It is need for calculate current player - player[0]
        """
        players.reverse()


    def set_signs(self, man, comp):
        """ Purpose to select sign for the 1st player. Auto for 2nd. """
        human_choice = machine_choice = None

        print("Select your sign:")
        print("\"x\" - 1")
        print("\"o\" - 2")

        while human_choice not in (0, 1):
            try:
                human_choice = int(input("Input 1 or 2: "))
                human_choice -= 1
            except ValueError:
                continue

        machine_choice = 0 if human_choice == 1 else 1

        man.sign = self.signs[human_choice]
        comp.sign = self.signs[machine_choice]


    def cur_player(self, players):
        """ Return player who did the move """
        return players[0]


    def opp_player (self, player):
        """ Return opposite player """
        for person in self.players:
            if person != player:
                return person
        

    def make_move(self, board, player):
        """ Call make_move of current player and handle the move """
        move = player.make_move(self, board)
        self.move_handle(move, board, player)


    def move_handle(self, move, board, player):
        """ Hadles move: remove from game.moves,
            add to player list of moves, add player sign to common moves list
        """
        self.moves.remove(move)              # remove move from available moves
        board.values[move] = player.sign     # add player sign to list of moves
        player.moves.append(move)            # add num of move of current player to his moves list
        player.set_win_combs(self, move)


    def comb_in_seq(self, comb, seq):
        """ Check for full entry of game win comb 'comb' in player moves 'seq' """
        for elem in comb:                     # if one of elements of win comb not in player moves 'seq' (not full entry)
            if elem not in seq:               # it is not full entry
                return False
        return True


    def has_winner(self, moves):
        """ Check for winner """
        for comb in self.win_combs:             # if one of game win comb has full entry at player moves
            if self.comb_in_seq(comb, moves):   # the game has a winner
                return True


    def draw(self):
        """ Check for a game draw """
        if not self.win_combs:                  # if no more win combinations
            return True                         # it is draw situation


    def finish(self, board, msg):
        """ Last step of the game -- draw final view of the board and print message """
        board.draw()
        print(msg)


# --------- class Game --------- #
# -------------------------------#


def main():

    game = Game()
    man = Human("Man")
    comp = Machine("Comp")
    game.players = [man, comp]
    board = Board()

    game.set_que(game.players)
    game.set_signs(man, comp)

    board.draw()

    fin_msg = ""
    while True:
        cur_player = game.cur_player(game.players)
        game.make_move(board, cur_player)
        if game.has_winner(cur_player.moves):
            fin_msg = "{} is Winner!!!".format(cur_player.name)
            break
        elif game.draw():
            fin_msg = "Draw!"
            break
        else:
            game.swap_que(game.players)
            board.draw()

    game.finish(board, fin_msg)


if __name__ == "__main__":
    main()