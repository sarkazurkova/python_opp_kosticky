from random import randrange
from enum import Enum
from datetime import datetime
import pygame
#from tabulate import tabulate


class Dice:
    @staticmethod
    def roll(max_value=6):
        if max_value < 4 or max_value > 9:
            raise ValueError("Maximální hodnota musí být v rozmezí 4 až 9")
        return randrange(1, max_value + 1)


class Gender(Enum):
    male = 'man'
    female = 'woman'



class Person:
    def __init__(self, nickname: str, gender: Gender):
        self.nickname = nickname
        self.gender = gender
        self._birth = datetime.now()

    def __str__(self):
        return f"Nickname: {self.nickname}, [{self.gender.value}], birth: {self._birth.year}"

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if isinstance(gender, Gender):
            self._gender = gender
        else:
            raise ValueError("Gender není platná hodnota.")

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        if len(nickname) <= 10:
            self._nickname = nickname
        else:
            raise ValueError("Nickname nesmi přesáhnout 10 znaků.")

    def get_seconds_from_birth(self):
        return (datetime.now() - self._birth).total_seconds()


class Player(Person):
    def __init__(self, nickname: str, gender: Gender, state: str = "CZE"):
        super().__init__(nickname, gender)
        self.state = state
        self.count_of_games = 0
        self.wins = 0
        self.score = {'plus': 0, 'minus': 0}
        self.coins = 1000

    def __str__(self):
        return f"| {super().__str__()}, state: {self.state} |"

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, wins):
        if wins >= 0:
            self._wins = wins
        else:
            raise ValueError("Počet výher nesmí být záporné číslo.")

    def win_rate(self):
        return round(self.wins / self.count_of_games * 100, 2) if self.count_of_games > 0 else 0

    def overall_score(self):
        return self.score['plus'], self.score['minus']
       

class Match:
    def __init__ (self, hp: Player, gp: Player):
        self.h_player = hp
        self.g_player = gp
        self._datetime = datetime.now()
        self.hp_points = 0
        self.gp_points = 0
        self._history = []
        self._values = []
        self.n = 0


    def __str__(self):
        return f"Host: {self.h_player.nickname} Guest: {self.g_player.nickname} {self.score()}"

    def __roll(self):
        while True:
            self.hp1 = Dice.roll()
            self.hp2 = Dice.roll()
            if self.hp1 != self.hp2:
                self.gp = Dice.roll()
                break
        if self.hp1 > self.hp2:
            n = self.hp1
            self.hp1 = self.hp2
            self.hp2 = n
        self._values.append(self.give_values())
        print(self.hp1, '|', self.hp2, '||', self.gp)
        return 0 if (self.hp1 < self.gp < self.hp2) else 1
    


    def play(self, bet):
        if self.__roll() == 1:
            self.hp_points += 1
            self.n = 1
            self.g_player.coins -= bet
            print(f"{self.h_player.nickname} získává bod! (Skóre: {self.hp_points} - {self.gp_points})  Your coins: {self.g_player.coins}")
        else:
            self.gp_points += 1
            self.n = 2
            self.g_player.coins += bet
            print(f"{self.g_player.nickname} získává bod! (Skóre: {self.hp_points} - {self.gp_points}) Your coins: {self.h_player.coins}")
        self._history.append(self.score())
        self.h_player.count_of_games += 1
        self.g_player.count_of_games += 1

        self.h_player.score['plus'] += self.hp_points
        self.g_player.score['plus'] += self.gp_points

        self.h_player.score['minus'] += self.gp_points
        self.g_player.score['minus'] += self.hp_points

        if self.hp_points > self.gp_points:
            self.h_player.wins += 1
        else:
            self.g_player.wins += 1

    def score(self):
        return self.hp_points, self.gp_points

    def get_history(self):
        return self._history
    
    def get_hp1(self):
        return self.hp1
    
    def get_hp2(self):
        return self.hp2
    
    def get_gp(self):
        return self.gp
    
    def give_values(self):
        return self.hp1, self.hp2, self.gp
    
    def get_values(self):
        return self._values

    def get_roll(self):
        return self.__roll()

