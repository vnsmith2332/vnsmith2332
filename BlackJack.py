import random

class Card(): #create Card member class
    def __init__ (self, suit, face, value):
        self.suit = suit
        self.face = face
        self.value = value
        
    def __str__ (self): #create string for cards
         return self.face + " of " + self.suit
         
class DeckOfCards(): #create deck of cards class
    def __init__ (self):
        self.deck = [] #empty list for deck
        self.suits = ["Hearts", "Spades", "Clubs", "Diamonds"] #list of suits
        self.face = ["2", "3", "4","5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.card_idx = 0
        
        for suit in self.suits: # 4 suits * 13 faces = 52 cards
            for i in range(len(self.face)):
                self.deck.append(Card(suit, self.face[i], self.values[i]))
    
    def shuffle_deck (self, cards): # function to shuffle
        random.shuffle(self.deck)
        
    def get_deck (self): #getter function to print deck 
        for card in self.deck:
            print(card.face, "of", card.suit, end=", ")
            
    def get_card (self): #create an index that is used to access a card w/in deck
        self.card_idx += 1
        return self.card_idx - 1
        
def main():
    print("Welcome! Let's play some Black Jack")
    print()
    deck = DeckOfCards()
    keep_playing = ""
    while keep_playing.lower() != "n": #loop to play multiple games
        
        print("Deck before shuffle:")
        deck.get_deck() #show unshuffled deck
        print()
        deck.shuffle_deck(deck) #shuffle deck
        print()
        print("Deck after shuffle:")
        deck.get_deck() #show shuffled deck
        print()
        print()
        
        player_cards = []
        values = []
        deck.card_idx = 0 #reset index to draw top 2 cards
        for i in range(2): #draw two cards
            card = deck.deck[deck.get_card()]
            values.append(card.value) #store values
            player_cards.append(card) #store cards
        
        for i in range(len(player_cards)):
            print("Card ", i+1, ": ", player_cards[i], sep="") #show first two cards
        
        print()
        print("Your score:", sum(values)) #tell player their score
        print()
        
        while True: #loop for infinite number of hits
        
            if sum(values) == 21 and len(player_cards) == 2: #automatic win if player got a "natural"
                break
            else:
                pass
            hit = input("Would you like a hit? (y/n): ")
            
            if hit.lower() == "y": #if they want a hit...
                card = deck.deck[deck.get_card()]
                values.append(card.value) #store value
                player_cards.append(card) #store card
                
                face_indexes = [player_cards[i].face for i in range(len(player_cards))] #list of faces to check for aces
    
                for i in range(len(player_cards)): #show all cards
                    print("Card ", i+1, ": ", player_cards[i], sep="")
                    
                print("Your score:", sum(values)) #show the score
                
                if sum(values) > 21: #if they bust...
                    for i in range(len(player_cards)):
                        if face_indexes[i] == "Ace": #check for aces + change values
                            values[i] = 1
                    
                    if sum(values) > 21: #after checking for aces, if still over 21...
                        break
                    else:
                        print("Your Aces are now worth 1. Your score:", sum(values)) #new score
                        
                elif sum(values) <= 21 and len(values) == 5: #check five card charlie
                    break
                
                else:
                    pass
                
            elif hit.lower() == "n": #end hit loop
                break
            
            else: #have to say yes or no
                print("Yes or no?!? You're holding up the game!")
        
        dealer_score = random.randint(17,23) #generate dealer score
        print("Dealer score", dealer_score) #show dealer score
        
        if len(values) == 5 and sum(values) <= 21: #conditions for winning/losing w/messages
            print("That's a five card charlie! You win!")
        elif len(values) == 2 and sum(values) == 21:
            print("That's a Blackjack! You win!")
        elif sum(values) > 21:
            print("You busted! That's a loss!")
        elif sum(values) <= 21 and dealer_score > 21:
            print("You win! The dealer busted!")
        elif sum(values) <= dealer_score:
            print("You lose! The dealer got a higher score!")
        else:
            print("You win! Your score was higher than the dealer's!")
            
        print()    
        keep_playing = input("Would you like to play again? (y/n)") #end game?
        
    print()
    print("Thanks for playing!") #end game message

if __name__ == "__main__":
    main()
    
    

