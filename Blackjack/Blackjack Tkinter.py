#Blackjack by James Mann

#Defines all of the imports needed
from tkinter import *
from tkinter import ttk

import tkinter as tk

#If the user does not have pygame installed, then pygameCheck is not true
#Whenever a sound is played later, if pygame is not installed. the sound will not play and there won't be an error
pygameCheck=True
try:
	import pygame
except ImportError:
	pygameCheck=False

import random
import time

#Window Setup
root=Tk()
root.title("Blackjack Official")

#Quickly defines the player's money to stop errors
playerMoney=0

#Sound Loading
if pygameCheck == True:
	#Music
	pygame.mixer.init()
	pygame.mixer.music.load("casino_music.wav")
	pygame.mixer.music.play(loops=99)
	pygame.mixer.music.set_volume(0.1)

	#Sound Effects
	card = pygame.mixer.Sound("card_draw.wav")
	win = pygame.mixer.Sound("ding.wav")
	win.set_volume(0.5)
	loss = pygame.mixer.Sound("fail.wav")
	equal = pygame.mixer.Sound("draw.wav")

#Regular Subroutines

#When you finish the game, this procedure is run, it removes all of the cards and resets the total
def reset():
	for widget in playerCardFrame.winfo_children():
		widget.destroy()
	player_totalLabel=Label(playerFrame, text="                                                                    ").grid(row=3, column = 0, columnspan=3)	
		
	for widget in cpuCardFrame.winfo_children():
		widget.destroy()
	cpu_totalLabel=Label(cpuFrame, text="                                                                    ").grid(row=3, column = 0, columnspan=3)
	#THe player can now submit their bet again
	submitBet.config(state=NORMAL)

#Draws a random card from the pack and then removes it
def draw():
	selectedCard=random.choice(deck)
	deck.remove(selectedCard)
	return selectedCard

#Finds the value of the card that has been drawn. Integers=The Number. T,J,Q,K=10. Ace =1
def total(card):
	global playerAceCount
	global playerCheck
	if card[0] in ('1','2','3','4','5','6','7','8','9'):
		value=int(card[0])

	#If an Ace is drawn then the number of Aces is increased (during the player's turn) - this is used to convert Aces to 1s
	elif card[0]=='A':
		value=11
		if playerCheck==True:
			playerAceCount=playerAceCount+1
	else:
		value=10
	return value

#Runs at the end of the game and finds out the winner. Also functions as the CPU drawing cards
def winCheck():
	global cpuTotal
	global playerTotal
	global cpuCurrentColumn
	global cpuCard2
	global cpu_totalLabel
	global betAmount
	global playerMoney
	global cpuAceCount

	playerCheck=False

	ccard2=Label(cpuCardFrame, text=cpuCard2).grid(row=0, column=1)
	cpu_totalLabel=Label(cpuFrame, text="The House has a total of: "+str(cpuTotal)).grid(row=3, column = 0, columnspan=3)

	#Cards keep being drawn as long as the value < 17
	while cpuTotal < 17:
		newCard=draw()
		cpuTotal=cpuTotal+total(newCard)
		newCardLabel=Label(cpuCardFrame, text=newCard).grid(row=0, column=cpuCurrentColumn)
		cpuCurrentColumn=cpuCurrentColumn+1
		cpu_totalLabel=Label(cpuFrame, text="The House has a total of: "+str(cpuTotal)).grid(row=3, column = 0, columnspan=3)

		#Checks if the CPU has gone bust, if so, they lose
	if cpuTotal > 21:
		playerMoney=playerMoney+(2*(betAmount))
		if pygameCheck == True:
			#PLays the loss sound
			pygame.mixer.find_channel().play(win)
	else:
		#WIn Condition
		if playerTotal > cpuTotal:
			playerMoney=playerMoney+(2*(betAmount))
			if pygameCheck == True:
				pygame.mixer.find_channel().play(win)

		#Loss Condition
		if playerTotal < cpuTotal:
			playerMoney=playerMoney
			if pygameCheck == True:
				pygame.mixer.find_channel().play(loss)

		#Draw Condition
		if playerTotal == cpuTotal:
			playerMoney=playerMoney+(betAmount)
			if pygameCheck == True:
				pygame.mixer.find_channel().play(equal)

	#Updates the players money based on their payout
	moneyLabel=Label(root, text="Player Money: "+str(playerMoney)).grid(row=0, column=0)		

	#Stops any more buttons from being pressed until the reset key is pressed
	hit.config(state=DISABLED)
	stick.config(state=DISABLED)
	reset.config(state=NORMAL)

#Bust Check procedure
def bustCheck(total):

	global hit
	global reset
	global playerTotal
	global playerAceCount

	#If the player is over 21 AND has an Ace, their score is reduced by 10
	#The number of aces the player has is reduced by 1 to stop an infinite loop of resetting
	if total > 21:
		if playerAceCount >= 1:
			playerTotal=playerTotal-10
			player_totalLabel=Label(playerFrame, text=("The Player has a total of: "+str(playerTotal))).grid(row=3, column = 0, columnspan=3)
			playerAceCount=playerAceCount-1
		else:
			#Ends the game and plays a loss sound if the player busts
			hit.configure(state=DISABLED)
			stick.configure(state=DISABLED)
			player_totalLabel=Label(playerFrame, text=("The Player has a total of: "+str(playerTotal))+", BUST!").grid(row=3, column = 0, columnspan=3)
			reset.config(state=NORMAL)
			if pygameCheck == True:
				pygame.mixer.find_channel().play(loss)

	#If the player has not bust, carry on the game
	else:
		return

#Button Commands that allow the game to work

#Main Program
def main():

	#Variables
	global deck
	#Deck of Cards
	deck=['A♦','2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','T♦','J♦','Q♦','K♦',
		'A♣','2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','T♣','J♣','Q♣','K♣',
		'A♥','2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','T♥','J♥','Q♥','K♥',
		'A♠','2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','T♠','J♠','Q♠','K♠']
	global playerTotal
	global cpuTotal
	global currentColumn
	global cpuCurrentColumn
	global playerCard1
	global playerCard2
	global cpuCard2
	global playerAceCount
	global playerCheck

	playerAceCount=0
	playerTotal=0
	cpuTotal=0
	currentColumn=2
	cpuCurrentColumn=2
	playerCheck=True

	#Buttons enabled or disabled as appropriate
	hit.configure(state=NORMAL)
	stick.configure(state=NORMAL)
	reset.config(state=DISABLED)
	submitBet.config(state=DISABLED)

	#PLays the card draw sound if Python is installed
	if pygameCheck == True:
		pygame.mixer.find_channel().play(card)

	#Player Hand
	playerCard1=draw()
	playerCard2=draw()

	playerTotal=playerTotal+total(playerCard1)
	playerTotal=playerTotal+total(playerCard2)

	#Stops CPU Aces affecting the playerAceTotal variable
	playerCheck=False

	#CPU Hand
	cpuCard1=draw()
	cpuCard2=draw()

	cpuTotal=cpuTotal+total(cpuCard1)
	cpu_totalLabel=Label(cpuFrame, text="The House has a total of: "+str(cpuTotal)).grid(row=3, column = 0, columnspan=3)
	cpuTotal=cpuTotal+total(cpuCard2)

	playerCheck=True

	#Card Display

	pcard1=Label(playerCardFrame, text=playerCard1).grid(row=0, column=0)
	pcard2=Label(playerCardFrame, text=playerCard2).grid(row=0, column=1)

	ccard1=Label(cpuCardFrame, text=cpuCard1).grid(row=0, column=0)

	player_totalLabel=Label(playerFrame, text="The Player has a total of: "+str(playerTotal)).grid(row=3, column = 0, columnspan=3)

	#Checks if the player has bust from the first two cards (this happens with double Aces)
	bustCheck(playerTotal)

	#Quick Early Win Check
	if playerTotal == 21:
		winCheck()

#Submitting the bet
def submit():

	global playerMoney
	global betAmount
	global playerCheck

	#Takes the bet amount from the entry field
	betAmount=bet.get()

	#Makes sure that the user has entered an integer. If they haven't, the code will not get past this point
	try:
		betAmount=int(betAmount)
	except ValueError:
		print("Error")

	#Validates that the bet is a positive integer, if it is, the main function is called		
	if betAmount > 0:
		if betAmount <= playerMoney:
			playerMoney=playerMoney-betAmount
			moneyLabel=Label(root, text="Player Money: "+str(playerMoney)).grid(row=0, column=0)
			main()
		else:
			return

#Draws a new card to the hand
def hit():

	#Draws a new card and then adds it to the total, then updates the total label
	global playerTotal
	global currentColumn
	newCard=draw()
	playerTotal=playerTotal+total(newCard)
	player_totalLabel=Label(playerFrame, text="The Player has a total of: "+str(playerTotal)).grid(row=3, column = 0, columnspan=3)

	#Adds the card to the list of cards
	newCardLabel=Label(playerCardFrame, text=newCard).grid(row=0, column=currentColumn)
	#Makes sure that the cards are aligned
	currentColumn=currentColumn+1

	#Draw Sound
	if pygameCheck == True:
		pygame.mixer.find_channel().play(card)

	#Runs to see if the player has bust	
	bustCheck(playerTotal)

#Player Area

#Sets up the two main play areas, the sizes are different to account for size changing later
playerFrame=LabelFrame(root, text="Player Hand", padx=100, pady=100, bg='#89b1cc')
playerFrame.grid(row=1, column=0)
cpuFrame=LabelFrame(root, text="CPU Hand", padx=200, pady=114, bg="#f5756e")
cpuFrame.grid(row=1, column=1)

#Sets up where the cards are displayed, this is inside of the respective frame
playerCardFrame=LabelFrame(playerFrame, text="Player Cards", padx=30, pady=5)
playerCardFrame.grid(row=0, column=0)
cpuCardFrame=LabelFrame(cpuFrame, text="House Cards", padx=30, pady=5)
cpuCardFrame.grid(row=0, column=0)

#Login

#Used for existing users
def getName():
	global playerMoney
	global username
	#Takes the name from the entry field and opens the file of that name, reads the contents and then sets the player's money to that value
	username=nameEntry.get()
	file=open(username+".txt", "r")
	playerMoney=file.read()
	#Converts it back to an integer
	playerMoney=int(playerMoney)
	moneyLabel=Label(root, text="Player Money: "+str(playerMoney))
	moneyLabel.grid(row=0, column=0)
	file.close()
	#Runs the init function
	init()

#Used for new users
def newName():
	global playerMoney
	global username
	#Reads the name from the entry field and creates a new text file of the same name
	username=nameEntry.get()
	if username=="":
		return
	file=open(username+".txt", 'w')
	file.close()
	#Sets the player's money to the default value - 500
	playerMoney=500
	moneyLabel=Label(root, text="Player Money: "+str(playerMoney))
	moneyLabel.grid(row=0, column=0)
	#Runs the init function
	init()

#Initialize Procedure
def init():
	#Makes sure all the buttons are in the correct state
	existButton.config(state=DISABLED)
	newButton.config(state=DISABLED)
	hit.config(state=NORMAL)
	stick.config(state=NORMAL)
	submitBet.config(state=NORMAL)

#Quits the game
def quitGame():
	global username
	#Saves the player's current money to their text file
	file=open(username+".txt", "w")
	file.write(str(playerMoney))
	file.close()
	root.quit()

#Sets up the login area
loginFrame=LabelFrame(root, text="Login")
loginFrame.grid(row=5, column=0)

#Buttons and labels that make up the login area
nameLabel=Label(loginFrame, text="Enter the Name of Your Account To Play: ")
nameLabel.grid(row=0, column=0)

nameEntry=Entry(loginFrame)
nameEntry.grid(row=0, column=1)

existButton=Button(loginFrame, text="Existing User", command=getName)
existButton.grid(row=0, column=2)

newButton=Button(loginFrame, text="New User", command=newName)
newButton.grid(row=0, column=3)

explanationLabel=Label(loginFrame, text="Type in your name and then press one of the buttons to sign ins")
explanationLabel.grid(row=1, column=0, columnspan=4)

#Buttons that the player uses
exitGame=Button(root, text="Save and Exit", command=quitGame)
exitGame.grid(row=0, column=2)

moneyLabel=Label(root, text="Player Money: "+str(playerMoney))
moneyLabel.grid(row=0, column=0)

bet=Entry(playerFrame)
bet.grid(row=2, column=0)

submitBet=Button(playerFrame, text="Submit Bet", command=submit, state=DISABLED)
submitBet.grid(row=2, column=1)

hit=Button(playerFrame, text="Hit!", command=hit, state=DISABLED)
hit.grid(row=2, column=2)

stick=Button(playerFrame, text="Stick!", command=winCheck, state=DISABLED)
stick.grid(row=2, column=3)

reset=Button(playerFrame, text="Reset", command=reset, state=DISABLED)
reset.grid(row=2, column=4)

#Volume Bar Setup

#Sets the volume based on the position of the volume bar
def volume(x):
	pygame.mixer.music.set_volume(slider.get())

#Sets up the slider
volumeFrame=LabelFrame(root, text="Volume")
volumeFrame.grid(row=1, column=2)
#THe initial value is 0.1 and the volume is between 0 and 0.2
slider=ttk.Scale(volumeFrame, from_=0.2, to=0, orient=VERTICAL, value=0.1, command=volume, length=200)
slider.grid(row=3, column=0)

#Explanation Area
gameExplanationFrame=LabelFrame(root, text="Explanation of the Game")
gameExplanationFrame.grid(row=4, column=0)

gameExplanation=Label(gameExplanationFrame, text="Welcome to Blackjack! Once you sign in enter your bet in the entry field and press submit.\nOnce your cards have been dealt either press Hit! to receive a new card or Stick!\nPress Reset to start a new game\nDo not leave the game without quitting!")#
gameExplanation.grid(row=0, column=0)

#Runs the game
root.mainloop()