#####################################
### WELCOME TO YOUR OOP PROJECT #####
#####################################

# For this project you will be using OOP to create a card game. This card game will
# be the card game "War" for two players, you and the computer. If you don't know
# how to play "War" here are the basic rules:
#
# The deck is divided evenly, with each player receiving 26 cards, dealt one at a time,
# face down. Anyone may deal first. Each player places his stack of cards face down,
# in front of him.
#
# The Play:
#
# Each player turns up a card at the same time and the player with the higher card
# takes both cards and puts them, face down, on the bottom of his stack.
#
# If the cards are the same rank, it is War. Each player turns up three cards face
# down and one card face up. The player with the higher cards takes both piles
# (six cards). If the turned-up cards are again the same rank, each player places
# another card face down and turns another card face up. The player with the
# higher card takes all 10 cards, and so on.
#
# There are some more variations on this but we will keep it simple for now.
# Ignore "double" wars
#
# https://en.wikipedia.org/wiki/War_(card_game)

from random import shuffle

class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    def compare(self, card):
        if Deck.RANKS.index(self.rank) == Deck.RANKS.index(card.rank):
            return 0
        if Deck.RANKS.index(self.rank) < Deck.RANKS.index(card.rank):
            return -1
        return 1

    def __str__(self):
        return "{}{}".format(self.suite, self.rank)

class Deck:
    SUITE = 'H D S C'.split()
    RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    def __init__(self):
        self.cards = [Card(suite, rank) for suite in Deck.SUITE for rank in Deck.RANKS]

    def shuffle(self):
        shuffle(self.cards);
        return self;

    def split_in_half(self):
        return (self.cards[0:26], self.cards[26:])

    def __str__(self):
        return str([str(card) for card in self.cards])

class Hand:
    def __init__(self, cards):
        self.cards = cards;

    def add_cards(self, cards):
        self.cards.extend(cards)

    def draw_cards(self, count):
        return [self.cards.pop(0) for i in (range(count))]

    def __str__(self):
        cards_list = [str(card) for card in self.cards]
        cards_str = ' '.join(cards_list)
        return cards_str;

    def __len__(self):
        return self.cards.__len__()

class Player:
    def __init__(self, name, hand):
        self.name = name.capitalize()
        self.hand = hand

    def draw_cards(self, count):
        return (self.hand.draw_cards(count))

    def add_cards(self, cards):
        self.hand.add_cards(cards)

    def num_cards(self):
        return len(self.hand)

    def __str__(self):
        return "{}:\n {}".format(self.name, str(self.hand))

class Game:
    def __init__(self, player_name):
        (split_cards_1, split_cards_2) = Deck().shuffle().split_in_half();
        self.computer = Player("computer", Hand(split_cards_1))
        self.player = Player(player_name, Hand(split_cards_2))
        self.num_consecutive_draws = 0
        self.table_cards = []

    def show_card_count_for_players(self):
        print("Computer has {} cards, you have {} cards, and table has {} cards.\n\n".format(
            self.computer.num_cards(),
            self.player.num_cards(),
            len(self.table_cards)))
        #print(self.computer)
        #print(self.player)

    def calc_num_cards_to_draw(self):
        if self.num_consecutive_draws == 0:
            return 1
        if self.num_consecutive_draws == 1:
            return 3
        return 2

    def game_over(self, num_cards_to_draw, manual):
        if (self.computer.num_cards() < num_cards_to_draw):
            print("Game Over. You won!")
            return True

        if (self.player.num_cards() < num_cards_to_draw):
            print("Game Over. Sorry! Computer won.")
            return True

        if manual:
            return self.stop_playing()

        return False

    def stop_playing(self):
        response = input("Draw card(s)? n to stop: ")
        if response.lower() == "n":
            print("Game Over. You have ended the game.")
            return True

        return False

    def draw_cards(self, num_cards_to_draw):
        if (num_cards_to_draw == 1):
            print("Drawing {} card each.".format(num_cards_to_draw))
        else:
            print("Drawing {} cards each.".format(num_cards_to_draw))

        computer_drawn_cards = self.computer.draw_cards(num_cards_to_draw)
        player_drawn_cards = self.player.draw_cards(num_cards_to_draw)
        return (computer_drawn_cards, player_drawn_cards)

    def show_drawn_cards(self, drawn_cards):
        print("{}: {}".format(self.computer.name, str(drawn_cards[0][-1])))
        print("{}: {}".format(self.player.name, str(drawn_cards[1][-1])))

    def add_to_table_cards(self, drawn_cards):
        self.table_cards.extend(drawn_cards[0])
        self.table_cards.extend(drawn_cards[1])

    def give_table_cards_to_winner(self, winner):
        print("{} won. Adding {} cards to winner's deck.".format(
                    winner.name, len(self.table_cards)))
        shuffle(self.table_cards)
        winner.add_cards(self.table_cards)
        self.end_war()

    def start_war(self):
        print("It's a draw")
        self.num_consecutive_draws += 1

    def end_war(self):
        self.table_cards = []
        self.num_consecutive_draws = 0

    def find_and_reward_winner(self, drawn_cards):
        self.add_to_table_cards(drawn_cards)
        result = drawn_cards[0][-1].compare(drawn_cards[1][-1])
        if (result > 0):
            self.give_table_cards_to_winner(self.computer)
            return
        if (result < 0):
            self.give_table_cards_to_winner(self.player)
            return
        # It's a Draw
        self.start_war() # continues until a winner is decided

    def run(self, manual):
        self.show_card_count_for_players()
        while True:
            num_cards_to_draw = self.calc_num_cards_to_draw()
            if self.game_over(num_cards_to_draw, manual):
                break
            drawn_cards = self.draw_cards(num_cards_to_draw)
            self.show_drawn_cards(drawn_cards)
            self.find_and_reward_winner(drawn_cards)
            self.show_card_count_for_players()

#### GAME #######
print("Welcome to War, let's begin...")
player_name = input("Please enter your name: ").upper()
game = Game(player_name)
game.run(False) # True = progress game manually
