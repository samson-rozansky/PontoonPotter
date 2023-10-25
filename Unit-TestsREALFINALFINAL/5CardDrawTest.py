import random
import os
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def value(self):
        if self.rank in ['K', 'Q', 'J']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Player:
    def __init__(self, name, balance):
        self.name = name
        self.hand = []
        self.score = 0
        self.balance = balance
        self.surrender = False
        self.robot = False
        self.bankID = random.random()
    def add_card(self, card):
        self.hand.append(card)
    
    def clear_hand(self):
        self.hand = []
    
    def calculate_hand_value(self):
        total_value = sum(card.value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == 'A')
        
        while total_value > 21 and num_aces:
            total_value -= 10
            num_aces -= 1
        
        return total_value

# Main function for Pontoon game
def pontoon():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3','4']
    deck = [Card(rank, suit) for rank in ranks for suit in suits] 
    
    players = [Player(input(f"Enter name for player {i + 1}: "), float(input(f"Enter initial balance for player {i + 1}: $"))) for i in range(int(input("Enter the number of players: ")))]
    
    while True:
        deck = [Card(rank, suit) for rank in ranks for suit in suits] 
        # Reset hands and bets for each round
        for player in players:
            player.clear_hand()
            bet = float(input(f"{player.name}, your current balance is ${player.balance}. Enter your bet: $"))
            while bet <= 0 or bet > player.balance:
                bet = float(input("Invalid bet. Please enter a valid bet: $"))
            player.bet = bet
        
        # Shuffle and deal initial cards to players
        random.shuffle(deck)
        for player in players:
            player.add_card(deck.pop())
            player.add_card(deck.pop())
        # Player's turn
        for player in players:
            while True:
                os.system('cls')
                print(f"\n{player.name}'s turn:")
                print("Your hand: " + ', '.join(f"{card.rank} of {card.suit}" for card in player.hand))
                print("Hand value: " + str(player.calculate_hand_value()))
                
                if player.calculate_hand_value() == 21:
                    print("Pontoon! You win!")
                    # player.balance += player.bet * 1.5
                    break
                if player.calculate_hand_value() > 21:
                    print("Busted! Your hand value is over 21.")
                    break
                if len(player.hand)==5:
                    print("5 Cards, you win!")
                    player.balance += player.bet
                    break
                
                if len(player.hand) == 2 and player.hand[0].rank == player.hand[1].rank:
                    choice = input("Choose your action (h: Hit, s: Stand, d: Double Down, su: Surrender, sp: Split): ").lower()
                else:
                    choice = input("Choose your action (h: Hit, s: Stand, d: Double Down, su: Surrender): ").lower()
                
                if choice == 'h':
                    player.add_card(deck.pop())
                elif choice == 'd':
                    if len(player.hand) == 2:
                        player.bet *= 2
                        newCard = deck.pop()
                        print(f"{newCard.rank} of {newCard.suit}")
                        player.add_card(newCard)
                        
                    else:
                        print("Invalid option for doubling down.")
                elif choice == 's':
                    break
                elif choice == 'su':
                    print(f"{player.name} surrendered. Half of your bet will be returned.")
                    player.balance -= player.bet / 2
                    player.surrender = True
                    break
                elif choice == 'sp':
                    if len(player.hand) == 2 and player.hand[0].rank == player.hand[1].rank:
                        newPlayer = Player(player.name,-1)
                        newPlayer.bankID = player.bankID
                        newPlayer.bet = player.bet
                        newPlayer.robot = True
                        newPlayer.hand = [player.hand[1],deck.pop()]
                        player.hand = [player.hand[0],deck.pop()]
                        players.append(newPlayer)
                        # new_hand = Card(player.hand.pop().rank, player.hand[0].suit)
                        # player.add_card(new_hand)
                        # new_hand = Card(deck.pop().rank, deck.pop().suit)
                        # player.add_card(new_hand)
                        # print(f"Your hands after split: {player.hand[0].rank} of {player.hand[0].suit}, {player.hand[1].rank} of {player.hand[1].suit}")
                    else:
                        print("Invalid option for splitting.")
                else:
                    print("Invalid choice. Please enter a valid option.")
        
        # Dealer's turn
        dealer = Player("Dealer", 0)
        dealer.add_card(deck.pop())
        dealer.add_card(deck.pop())
        
        print("\nDealer's turn:")
        print("Dealer's hand: " + ', '.join(f"{card.rank} of {card.suit}" for card in dealer.hand))
        
        while dealer.calculate_hand_value() < 17:
            dealer.add_card(deck.pop())
        print("Dealer's hand: " + ', '.join(f"{card.rank} of {card.suit}" for card in dealer.hand))
        def splitCheck(player,deltaBank):
            done = False
            for i in range(len(players)):
                if(players[i].bankID == player.bankID):
                    players[i].balance += deltaBank
                    done = True
            

        # Determine the winner and update player balances
        for player in players:
            print(f"\n{player.name}'s hand value: " + str(player.calculate_hand_value()))
            if player.calculate_hand_value() == 21 or player.surrender or len(player.hand)==5:
                player.surrender = False
                if(player.robot and player.calculate_hand_value()==21):
                   splitCheck(player,player.bet*3/2)
                if(player.robot and len(player.hand)==5):
                   splitCheck(player,player.bet)  
                if(not player.robot and player.calculate_hand_value()==21):
                    print("Pontoon! You win!")
                    player.balance += player.bet * 1.5
                continue
            elif player.calculate_hand_value() > 21:
                print(f"{player.name} busts! Dealer wins!")
                if(player.robot):
                   splitCheck(player,player.bet*(-1))
                player.balance -= player.bet
            elif dealer.calculate_hand_value() > 21 or player.calculate_hand_value() > dealer.calculate_hand_value():
                print(f"{player.name} wins!")
                if(player.robot):
                   splitCheck(player,player.bet) 
                player.balance += player.bet
            elif player.calculate_hand_value() == dealer.calculate_hand_value():
                print(f"{player.name} ties with the dealer!")
                if(player.robot):
                   splitCheck(player,player.bet*(-1)) 
                player.balance -= player.bet
            else:
                print(f"{player.name} loses!")
                if(player.robot):
                   splitCheck(player,player.bet*(-1)) 
                player.balance -= player.bet
        
        # Display updated balances
        print("\nUpdated Balances:")
        robots = []
        for i in range(len(players)):
            if(players[i].robot):
                robots.append(i)
        for i in robots[::-1]:
            players.pop(i)
        for player in players:
            print(f"{player.name}: ${player.balance:.2f}")
        
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break

# Run the game
pontoon()
