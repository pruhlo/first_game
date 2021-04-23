import random


class Health:

    def __init__(self):
        self.__health = 100

    def _check_soundness(self): # set up level health from 0 till 100
        if self.__health > 100:
            self.__health = 100
            return self.__health
        elif self.__health <= 0:
            self.__health = 0
            return self.__health
        else:
            return self.__health

    @property
    def soundness(self): # get health level value
        return self.__health

    @soundness.setter
    def set_soundness(self, value): # set up health level value
        self.__health += value
        return self._check_soundness()


class Personage(Health):

    def __init__(self, name):
        Health.__init__(self)
        self.name = name

    @staticmethod
    def _dict_action(): # fighting power of the hero and description in the keys
        dict_action = {}
        dict_action["regain health"] = random.randint(18, 25)
        dict_action['slight brunt'] = random.randint(-25, -18)
        dict_action["severe brunt"] = random.randint(-35, -10)
        return dict_action

    def action(self, spin=False): # the choice of the hero's activity and set up unfair play
        dict_action = self._dict_action()
        if spin == False:
            return random.choice(list(dict_action.items()))
        else:
            del dict_action["severe brunt"]
            del dict_action['slight brunt']
            return random.choice(list(dict_action.items()))

    def display_personage(self): # return health level value of string to console
        count_live_cell = int(self.soundness/10)
        count_lost_live_cell = 10 - count_live_cell
        BOLD = '\033[1m'
        RED = '\033[91m'
        END = '\033[0m'
        BLUE = '\033[34m'
        live_cell = '\u2588'+' '
        lost_live_cell = f'{RED}\u2588{END} '
        health_table = count_live_cell*live_cell + count_lost_live_cell*lost_live_cell
        return f' {BOLD} {BLUE} {self.name} {END} {health_table} {self.soundness}%'


class GameDisplay:

    def __init__(self, player, computer):
        self.player = player
        self.computer = computer
        self.list_objects = [self.player, self.computer]
        
    @staticmethod
    def dead(health):
        if health <= 0:
            print('GAME OVER')
            quit()
        else:
            pass

    def batle(self, player):#describes the turn-based logic of the game
        new_list = self.list_objects.copy() # create copy list with personages for future del one 
        for obj in new_list:
            self.dead(obj.soundness) # check to end the game
        if player == self.computer and self.computer.soundness <= 35: # improve computer to unfair play
            kind, value = player.action(spin=True)
        else:
            kind, value = player.action()
        new_list.remove(player) # remove the active player
        new_list[0].set_soundness = value # set the damage to the inactive player
        # displaying player status in the console
        if value < 0:
            print('\033[7m' + player.name + ' attack with '+ kind + ' at '+ str(value) + '%'+'\033[0m')
        else:
            print('\033[7m' + player.name + ' tried to deal damage, but failed. '+ new_list[0].name +' health restored'+'\033[0m')
        print(self.display_status())
        new_list.clear()
    
    def random_choice(self):
        return random.choice(self.list_objects)

    def display_status(self): # return health level value of string to console
        BOLD = '\033[1m'
        GREEN = '\033[32m'
        END = '\033[0m'
        player = self.player.display_personage()
        computer = self.computer.display_personage()
        return f"""{player}{BOLD}{GREEN}  VS{END}{computer}"""


if __name__ == '__main__':
    players_name = ['Godzilla', 'Alien', 'Predator', 'King Kong']
    robots_name = ['Terminator T-800', 'C-3PO', 'R2-D2', 'Robocop', 'WALL-E']
    player = Personage(random.choice(players_name))
    computer = Personage(random.choice(robots_name))
    game = GameDisplay(player, computer)
    print(game.display_status())
    game_mode = input('If you want automatic game mode press 1 and Enter, else anykey:  ')
    while True:
        if game_mode == '1':
            game.batle(game.random_choice())
        else:
            input('Press Enter to execute the move ')
            game.batle(game.random_choice())
