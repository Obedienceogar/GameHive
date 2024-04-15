# All the modules i will use in this program will be defined here
import copy
import asyncio
import json
import threading
from aiogram import types
from aiogram.utils import exceptions
import random
import functions
import variables
import threading
import time
import string
import Game
import classes


class ElimWaitingRoom:
    def __init__(self,bot):
        self.bot = bot
        self.timer = 30
        self.players_list = []
        self.players_dict = {} # this is a dictinary whose key is the id of each user and the value is the full name of the user 
        self.message_ids = {} # Dictionary to store the message id of message sent to each user for referencing 
        self.category_list = [] # I am initializing this list here so as to avoid an attribute error later in the program
        self.display_msg = None # This variable is initialized here so as to avoid an attribute error later in the program and also to keep track of the
        # message that will be displayed after before the game starts that is the message that will allow users to vote for the category they want 
        # questions to come out from
        self.start_game_timer = 10

    async def start_game(self,elim_waitingroom): # This function starts the game
        self.msg_ids = copy.deepcopy(self.message_ids) 
        self.plyrs_list = copy.deepcopy(self.players_list)
        self.plyrs_dict = copy.deepcopy(self.players_dict)
        self.elim_waitingroom = elim_waitingroom
        variables.elim_pause = True  
        for i in self.players_list:
            variables.elim_vote[int(i)] = False
        variables.elim_contvar = False # this will allow the waiting room to be open to another set of players to play a game in the bot

        if len(self.players_list) < 2:
            reply_keyboard = functions.menu(self.players_list[0])
            await self.bot.send_message(self.players_list[0],"Not enough players\nTry comming back later or play another game",reply_markup=reply_keyboard)
        else:
            self.vote = classes.ElimVote(self.bot,self.message_ids,self.players_list,self.players_dict,self.elim_waitingroom) # Instansiating the voting class
        
        self.reset_attributes()

    async def display_and_update_msg(self,id): # this will display the edited message to all the users
        self.count = 0
        self.text = f"\t\tTimer: {self.timer}(s)\n\n\n"
        for i in self.players_list: # This block of code is responsible for editing the message sent to the user by the bot
            self.count += 1
            self.text += f"{self.count}.\t{self.players_dict[i]}\n\n" # Writes a new message to the text variable
        self.display_msg = self.text
        self.count = 0

        for i in self.players_list:
            try:
                print(self.message_ids)
                await self.bot.edit_message_text(self.display_msg, i, self.message_ids[str(i)])
            except:
                pass

    def reset_attributes(self): # this method will reset the attributes of the waiting room class for the next instantiation
        self.timer = 30
        self.players_list = []
        self.players_dict = {}
        self.message_ids = {} # Dictionary to store the message id of message sent to each user for referencing 
        self.category_list = [] # I am initializing this list here so as to avoid an attribute error later in the program
        self.display_msg = None # This variable is initialized here so as to avoid an attribute error later in the program and also to keep track of the
        # message that will be displayed after before the game starts that is the message that will allow users to vote for the category they want 
        # questions to come out from
        self.start_game_timer = 10

class WaitingRoom:
    def __init__(self,bot):
        self.bot = bot
        self.timer = 30
        self.players_list = []
        self.players_dict = {} # this is a dictinary whose key is the id of each user and the value is the full name of the user 
        self.message_ids = {} # Dictionary to store the message id of message sent to each user for referencing 
        self.category_list = [] # I am initializing this list here so as to avoid an attribute error later in the program
        self.display_msg = None # This variable is initialized here so as to avoid an attribute error later in the program and also to keep track of the
        # message that will be displayed after before the game starts that is the message that will allow users to vote for the category they want 
        # questions to come out from
        self.start_game_timer = 10

    async def start_game(self,waitingroom): # This function starts the game
        self.msg_ids = copy.deepcopy(self.message_ids) 
        self.plyrs_list = copy.deepcopy(self.players_list)
        self.plyrs_dict = copy.deepcopy(self.players_dict)
        self.elim_waitingroom = waitingroom
        variables.pause = True  
        for i in self.players_list:
            variables.vote[int(i)] = False
        variables.elim_contvar = False # this will allow the waiting room to be open to another set of players to play a game in the bot
    
        self.vote = classes.Vote(self.bot,self.message_ids,self.players_list,self.players_dict,self.elim_waitingroom)
        
        self.reset_attributes()

    async def display_and_update_msg(self,id): # this will display the edited message to all the users
        self.count = 0
        self.text = f"\t\tTimer: {self.timer}(s)\n\n\n"
        for i in self.players_list: # This block of code is responsible for editing the message sent to the user by the bot
            self.count += 1
            self.text += f"{self.count}.\t{self.players_dict[i]}\n\n" # Writes a new message to the text variable
        self.display_msg = self.text
        self.count = 0

        for i in self.players_list:
            try:
                print(self.message_ids)
                await self.bot.edit_message_text(self.display_msg, i, self.message_ids[str(i)])
            except:
                pass

    def reset_attributes(self): # this method will reset the attributes of the waiting room class for the next instantiation
        self.timer = 30
        self.players_list = []
        self.players_dict = {}
        self.message_ids = {} # Dictionary to store the message id of message sent to each user for referencing 
        self.category_list = [] # I am initializing this list here so as to avoid an attribute error later in the program
        self.display_msg = None # This variable is initialized here so as to avoid an attribute error later in the program and also to keep track of the
        # message that will be displayed after before the game starts that is the message that will allow users to vote for the category they want 
        # questions to come out from
        self.start_game_timer = 10
        