"""Simulering av stein saks papir"""
import random
import matplotlib.pyplot as plt

class Spiller:
    """Superklasse for spillere"""
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.num_scissor = 0
        self.num_paper = 0
        self.num_rock = 0
        self.moves = []

    def get_points(self):
        """Returnerer antall poeng"""
        return self.points

    def update_nums(self):
        """Oppdaterer fordeling av tidligere aksjoner"""
        for x in self.moves:
            if x == "Rock":
                self.num_rock += 1
            elif x == "Paper":
                self.num_paper += 1
            else:
                self.num_scissor += 1

    def get_choice(self):
        """Velger aksjon på bakgrunn av antall tidligere aksjoner"""
        print(self.oppgi_navn())
        if max(self.num_rock, self.num_paper, self.num_scissor) == self.num_rock:
            a_1 = Aksjon("Paper")
            return a_1
        elif max(self.num_rock, self.num_paper, self.num_scissor) == self.num_scissor:
            a_2 = Aksjon("Rock")
            return a_2
        else:
            a_3 = Aksjon("Scissor")
            return a_3


    def motta_resultat(self, action1, action2, points):
        """Mottar resultat"""
        return True

    def oppgi_navn(self):
        """Returnerer navn"""
        return self.name

    def random_action(self):
        """Velger tilfeldig aksjon"""
        random_num = random.randint(0, 2)
        if random_num == 0:
            a_1 = Aksjon("Rock")
            return a_1
        elif random_num == 1:
            a_2 = Aksjon("Paper")
            return a_2
        elif random_num == 2:
            a_3 = Aksjon("Scissor")
            return a_3


class Tilfeldig(Spiller):
    """Klasse som velger tilfeldige aksjoner"""

    def __init__(self, name):
        super().__init__(name)

    def motta_resultat(self, action1, action2, points):
        """Mottar resultat"""
        self.points += points

    def velg_aksjon(self):
        """Velger aksjon"""
        return self.random_action()


class Sekvensiell(Spiller):
    """Klasse som velger sekvensielle aksjoner"""

    def __init__(self, name):
        super().__init__(name)
        self.counter = -1

    def motta_resultat(self, action1, action2, points):
        """Mottar resultat"""
        self.points += points


    def velg_aksjon(self):
        """Velger aksjon"""
        if self.counter == 2:
            self.counter = 0
        else:
            self.counter += 1

        if self.counter == 0:
            a_1 = Aksjon("Rock")
            return a_1
        elif self.counter == 1:
            a_2 = Aksjon("Paper")
            return a_2
        elif self.counter == 2:
            a_3 = Aksjon("Scissor")
            return a_3

class MestVanlig(Spiller):
    """Klasse som kontrer motstanders vanligste trekk"""

    def __init__(self, name):
        super().__init__(name)
        self.moves = []
        self.num_rock = 0
        self.num_paper = 0
        self.num_scissor = 0

    def motta_resultat(self, action1, action2, points):
        """Mottar resultat fra gjennomført spill"""
        self.add_result(action2)
        self.points += points

    def add_result(self, move):
        """Legger til ett trekk"""
        self.moves.append(move)

    def get_results(self):
        """Returnerer tidligere trekk"""
        return self.moves

    def velg_aksjon(self):
        """Velger aksjon"""
        self.update_nums()
        if len(self.moves) == 0:
            return self.random_action()
        else:
            if max(self.num_rock, self.num_paper, self.num_scissor) == self.num_rock:
                a_1 = Aksjon("Paper")
                return a_1
            elif max(self.num_rock, self.num_paper, self.num_scissor) == self.num_scissor:
                a_2 = Aksjon("Rock")
                return a_2
            else:
                a_3 = Aksjon("Scissor")
                return a_3

    def update_nums(self):
        self.num_scissor = 0
        self.num_paper = 0
        self.num_rock = 0
        for x in self.moves:
            if x == "Rock":
                self.num_rock += 1
            elif x == "Paper":
                self.num_paper += 1
            else:
                self.num_scissor += 1


class Historiker(Spiller):
    """Klasse som leter etter mønster hos motstander"""
    def __init__(self, name, num):
        super().__init__(name)
        self.moves = []
        self.last_x = []
        self.next_moves = []
        self.new_counter = 0
        self.num = num

    def motta_resultat(self, action1, action2, points):
        """Mottar resultat"""
        self.moves.insert(0, action2)
        self.points += points

    def velg_aksjon(self):
        """Velger aksjon"""
        if not self.moves or len(self.moves) < self.num:
            return self.random_action()
        self.last_x = []
        for i in range(self.num):
            self.last_x.append(self.moves[i])

        self.next_moves = []

        for i in range(len(self.last_x), len(self.moves)):
            if self.moves[i] == self.last_x[0] and len(self.last_x) == 1:
                if (i-1) > (-1):
                    self.next_moves.append(self.moves[i-1])
                else:
                    break

            elif self.moves[i] == self.last_x[0]:
                self.new_counter = i
                for x in range(1, len(self.last_x)):
                    if self.new_counter+1 <= len(self.moves)-1:
                        self.new_counter += 1
                    else:
                        break

                    if self.moves[self.new_counter] != self.last_x[x]:
                        break

                    elif self.moves[self.new_counter] == self.last_x[len(self.last_x)-1]:
                            self.next_moves.append(self.moves[self.new_counter - self.num])

        if not self.next_moves:
            return self.random_action()

        self.num_scissor = 0
        self.num_paper = 0
        self.num_rock = 0
        for x in self.next_moves:
            if x == "Rock":
                self.num_rock += 1
            elif x == "Paper":
                self.num_paper += 1
            else:
                self.num_scissor += 1
        if max(self.num_rock, self.num_paper, self.num_scissor) == self.num_rock:
            a_1 = Aksjon("Paper")
            return a_1
        elif max(self.num_rock, self.num_paper, self.num_scissor) == self.num_scissor:
            a_2 = Aksjon("Rock")
            return a_2
        else:
            a_3 = Aksjon("Scissor")
            return a_3


class Aksjon:
    """Klasse for å velge aksjon"""
    def __init__(self, action):
        self.action = action

    def __gt__(self, other):
        if self.action == "Rock" and other.action == "Scissor":
            return True
        elif self.action == "Paper" and other.action == "Rock":
            return True
        elif self.action == "Scissor" and other.action == "Paper":
            return True
        return False

    def __eq__(self, other):
        if self.action == other.action:
            return True
        return False


class EnkeltSpill:
    """Spiller enkelt spill"""

    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.first_action = ""
        self.second_action = ""
        self.winner = ""

    def gjennomfoer_spill(self):
        """Gjennomfører enkelt spill"""
        self.action1 = self.spiller1.velg_aksjon()
        self.action2 = self.spiller2.velg_aksjon()

        if self.action1 > self.action2:
            self.spiller1.motta_resultat(self.action1.action, self.action2.action, 1)
            self.spiller2.motta_resultat(self.action2.action, self.action1.action, 0)
            self.winner = self.spiller1.oppgi_navn()
            self.first_action = self.action1.action
            self.second_action = self.action2.action
        elif self.action2 > self.action1:
            self.spiller1.motta_resultat(self.action1.action, self.action2.action, 0)
            self.spiller2.motta_resultat(self.action2.action, self.action1.action, 1)
            self.winner = self.spiller2.oppgi_navn()
            self.first_action = self.action1.action
            self.second_action = self.action2.action
        else:
            self.spiller1.motta_resultat(self.action1.action, self.action2.action, 0.5)
            self.spiller2.motta_resultat(self.action2.action, self.action1.action, 0.5)
            self.winner = "Draw"
            self.first_action = self.action1.action
            self.second_action = self.action2.action

        print(self.spiller1.oppgi_navn() + ": " + self.action1.action + ", " +
              self.spiller2.oppgi_navn() + ": " + self.action2.action
              + " -> " + self.winner + " vinner")

    def __str__(self):
        return self.winner + " " + self.first_action + " " + self.second_action


class MangeSpill(EnkeltSpill):
    """Klasse for å spille flere spill"""

    def __init__(self, spiller1, spiller2, antall_spill):
        super().__init__(spiller1, spiller2)
        self.antall_spill = antall_spill
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.points_lst = []

    def arranger_turnering(self):
        """Turnering for mange spill"""
        for i in range(self.antall_spill):
            self.gjennomfoer_spill()
            self.points_lst.append(self.spiller1.get_points()/(i+1))
        print()
        print(self.spiller1.oppgi_navn()+":", self.spiller1.get_points(), self.spiller2.oppgi_navn()+":",
              self.spiller2.get_points())
        print("Det ble spilt " + str(int(self.spiller1.get_points() + self.spiller2.get_points())) + " kamper.")
        plt.plot(self.points_lst)
        plt.ylabel(self.spiller1.oppgi_navn() + " win %")
        plt.xlabel("Antall kamper")
        plt.show()


class Lagspill:

    def __init__(self):
        self.player1 = None
        self.player2 = None

    def lag_spill(self):
        while True:
            print("Velkommen til Stein, Saks, Papir!")
            self.player1_name = input("Velg første spiller: [t,s,m,h] ")
            if self.player1_name == "t":
                self.player1 = Tilfeldig("Tilfeldig")
            elif self.player1_name == "s":
                self.player1 = Sekvensiell("Sekvensiell")
            elif self.player1_name == "m":
                self.player1 = MestVanlig("Mest vanlig")
            elif self.player1_name == "h":
                self.remember1 = input("Hvor mange skal Historiker huske? ")
                while not self.remember1.isnumeric():
                    print("Ikke et tall, prøv igjen.")
                    self.remember1 = input("Hvor mange skal Historiker huske? ")
                self.player1 = Historiker("Historiker", int(self.remember1))
            else:
                print("Feil input")
                continue

            self.player2_name = input("Velg andre spiller: [t,s,m,h ")

            if self.player2_name == "t":
                self.player2 = Tilfeldig("Tilfeldig")
            elif self.player2_name == "s":
                self.player2 = Sekvensiell("Sekvensiell")
            elif self.player2_name == "m":
                self.player2 = MestVanlig("Mest vanlig")
            elif self.player2_name == "h":
                self.remember2 = input("Hvor mange skal Historiker huske? ")
                while not self.remember2.isnumeric():
                    print("Ikke et tall, prøv igjen.")
                    self.remember2 = input("Hvor mange skal Historiker huske? ")
                self.player2 = Historiker("Historiker", int(self.remember2))
            else:
                print("Feil input")
                continue
            self.antall_spill = input("Hvor mange spill? ")
            while not self.antall_spill.isnumeric():
                print("Ikke et tall.")
                self.antall_spill = input("Hvor mange spill? ")
            MANG = MangeSpill(self.player1, self.player2, int(self.antall_spill))
            MANG.arranger_turnering()
            self.new_game = input("Nytt spill? [y/n] ")
            if self.new_game == "n":
                break
                