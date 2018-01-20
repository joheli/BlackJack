import random
import getpass


class Deck(object):
    def __init__(self):

        self.cards0 = []
        self.cards = []

        ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Spades", "Clubs", "Diamonds"]

        for i in ranks:
            for j in suits:
                self.cards0.append(str(i) + " of " + j)

        self.cards = self.cards0

    def dealCard(self):
        cardDrawn = self.cards[random.randint(0, len(self.cards) - 1)]
        self.cards.remove(cardDrawn)
        return (cardDrawn)


class Hand(object):
    def __init__(self):
        self.cards = []
        self.values = []
        self.score = 0
        self.limit = 21
        self.stand = False

    def addCard(self, card):
        # print("adding card " + card)
        self.cards.append(card)
        self.assignValues()

    def assignValues(self):

        if (len(self.cards) > 0):
            self.values = []
            for i in self.cards:
                # print("examining card " + i)
                try:
                    n = int(i[0:2])
                    self.values.append(n)
                except:
                    if i.startswith("J") or i.startswith("Q") or i.startswith("K"):
                        self.values.append(10)
                    else:
                        self.values.append(11)

            self.calculateScore()

            # deal with aces, in case that score is over limit
            while self.values.count(11) > 0 and self.score > self.limit:
                aceIndex = self.values.index(11)
                self.values[aceIndex] = 1
                self.calculateScore()

    def setStand(self, what=True):
        self.stand = what

    def calculateScore(self):
        if (len(self.cards) > 0):
            self.score = sum(self.values)

    def busted(self):
        return (self.score > self.limit)


class Player(object):
    def __init__(self, name=getpass.getuser().capitalize(), human=True, balance=100, scoreLimit=18):
        self.hand = Hand()
        self.human = human

        if human:
            self.name = name
        else:
            self.name = "Computer"

        self.scoreLimit = scoreLimit
        self.balance = balance

    def add(self, amount):
        self.balance += amount

    def remove(self, amount):
        self.balance -= amount

    def broke(self):
        return (self.balance <= 0)

    def newHand(self):
        self.hand = Hand()


class Game(object):
    def __init__(self, initialBet=10):
        self.player1 = Player()
        self.player2 = Player(human=False)
        self.bet = initialBet

    def start(self):
        q = input("Welcome to BlackJack! What is your name? (press enter for '%s'): " % self.player1.name)
        if q:
            self.player1.name = q
        self.newGame()

    def __adjustBet(self):
        while True:
            try:
                b = input("How much would you like to bet? (press enter to leave current value: %d): " % self.bet)

                if b:
                    newB = int(b)
                else:
                    newB = self.bet

                if newB > self.player1.balance:
                    print("%d is over your current balance %d - bet will be set to %d" % (
                        newB, self.player1.balance, self.player1.balance))
                    self.bet = self.player1.balance
                else:
                    self.bet = newB

                break

            except:
                print("I didn't that. Please try again entering an integer!")

    def ask(self):
        a = input("%s, please state your choice (hit, stand): " % self.player1.name)
        if a.capitalize().startswith("H"):
            return (1)
        elif a.capitalize().startswith("S"):
            return (2)
        else:
            return (-1)

    def status(self):
        print("%s: current score %s, cards %s, balance %s" % (
            self.player1.name, self.player1.hand.score, self.player1.hand.cards, self.player1.balance))
        print("%s: current score %s, cards %s, balance %s" % (
            self.player2.name, self.player2.hand.score, self.player2.hand.cards, self.player2.balance))

    def newGame(self):
        print("Let's start a new game!")

        self.deck = Deck()

        self.player1.newHand()
        self.player2.newHand()

        self.__adjustBet()

        self.player1.hand.addCard(self.deck.dealCard())
        self.player2.hand.addCard(self.deck.dealCard())

        self.__gameLoop()

    def changeBet(self, amount):
        self.bet = amount

    def __gameLoop(self):
        while True:
            self.status()
            for p in [self.player1, self.player2]:
                if p.human:
                    while not p.hand.stand:
                        c = self.ask()
                        if c == -1:
                            print("I didn't get that - please try again!")
                            continue
                        else:
                            if c == 1:
                                p.hand.addCard(self.deck.dealCard())
                            else:
                                p.hand.setStand()
                            break
                else:
                    if p.hand.score < p.scoreLimit:
                        p.hand.addCard(self.deck.dealCard())
                    else:
                        p.hand.setStand()

            if self.player1.hand.stand:
                print("%s is standing." % (self.player1.name))

            if self.player2.hand.stand:
                print("%s is standing." % (self.player2.name))

            if self.player1.hand.stand and self.player2.hand.stand:
                print("Both players are standing.")
                if self.player1.hand.score > self.player2.hand.score:
                    print("%s has won!" % (self.player1.name))
                    self.player1.add(self.bet)
                    self.player2.remove(self.bet)
                elif self.player1.hand.score == self.player2.hand.score:
                    print("Both players have the same score. Nobody wins.")
                else:
                    print("%s has won!" % (self.player2.name))
                    self.player2.add(self.bet)
                    self.player1.remove(self.bet)
                self.status()
                break

            if self.player1.hand.busted():
                print("%s is busted!" % (self.player1.name))
                self.player1.remove(self.bet)
                self.player2.add(self.bet)
                self.status()
                break

            if self.player2.hand.busted():
                print("%s is busted!" % (self.player2.name))
                self.player2.remove(self.bet)
                self.player1.add(self.bet)
                self.status()
                break

        print("Round over.")

        ask = input("Do you want to play again, %s? (y/n): " % (self.player1.name))
        if ask.capitalize().startswith("Y"):
            if not self.player1.broke():
                self.newGame()
            else:
                print("%s, be serious. You are BROKE! Get a life!" % self.player1.name)
        else:
            print("Sorry to hear that. See you later!")


g = Game().start()
