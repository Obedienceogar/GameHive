# All modules to be used in this program will be defined here
import random
import threading
import variables
import functions
import asyncio
import time
import copy
import Game
 
class ElimVote(): # This class will enable users to vote for the category they want the trivia questions to be taken from
    def __init__(self,bot,message_ids,players_list,players_dict,elim_waitingroom):
        self.bot = bot
        self.display_msg = None
        self.message_ids =copy.deepcopy(message_ids)
        self.players_list = copy.deepcopy(players_list)
        self.players_dict = copy.deepcopy(players_dict)
        self.display_text = None
        self.list_for_category = random.sample(variables.categories,5)
        print(f"This are the categories to be voted for {self.list_for_category}")
        self.category_list = self.list_for_category
        variables.elim_pause = False
        variables.elim_contvar = False
        self.elim_waitingroom = elim_waitingroom
        asyncio.create_task(self.update_msg_for_voting(self.elim_waitingroom))
        for i in players_list: # this will make the variables.vote variable to be false so the user can vote after the user vote the variable will be set to true
            variables.elim_vote[i] = False
        
    async def update_msg_for_voting(self,waitingroom): #This method will update the message for the voting message
        self.start_time = time.time()
        while waitingroom.start_game_timer > 1:
            await asyncio.sleep(2)
            time_elapsed = time.time()-self.start_time
            waitingroom.start_game_timer = 10 - int(time_elapsed) # i don't even understand what i did here again but as far as the code is working well i don't think i am going to disturnb this block of code until it is time to optimize the bot
            self.rewrite_msg_for_voting(waitingroom)
            print(f"These are the message ids: {self.message_ids}")
            print("about to update message")
            print(f"this are the players list {self.players_list}")
            for i in self.players_list:
                print(f"updating message for {i}")
                await self.bot.edit_message_text(self.display_msg,i,self.message_ids[str(i)],reply_markup=variables.elim_choice_button)
                print(f"updating message for {i} is finished")
        self.category = await functions.find_max_green_option(self.display_msg,self.category_list)
        print(self.category)
        self.category = self.category[:-3].strip()
        game_key = functions.random_alphabet_string(10)
        for i in self.players_list: # This will loop through get all the player list id and store the game object created in the user_gaming_room
            # dictionary for them
            variables.user_gaming_room[str(i)] = game_key    
            await self.bot.edit_message_text(variables.knockout_trivia_game_rule,i,self.message_ids[str(i)])        
        
        await asyncio.sleep(10) #pauses the bot for 10 seconds so the bot's game rule can bes shown to all the users
        variables.gaming_room[game_key] = Game.EliminationTriviaGame(self.bot,self.message_ids,self.players_list,self.players_dict,self.category)


    def rewrite_msg_for_voting(self,waitingroom):
        self.display_text = f"\t\t⏱️ Timer: ⏱️: {waitingroom.start_game_timer}(s)\n\n🗳️ Vote for the category you want questions to be drawn from in the trivia game! 🎯 \n\n\n"
        self.count = 1

        for i in self.category_list: # This loop will run 5 times in other to get 5 catetgories for the user to choose
            self.display_text += f"{self.count}.\t{i}\n\n"
            self.count += 1      
        self.display_msg = self.display_text
    
    def reset_attributes(self): # This will reset all the main attributes of this class
        self.display_msg = None
        self.message_ids = None
        self.players_list = None
        self.players_dict = None
        self.display_text = None

class Vote(): # This class will enable users to vote for the category they want the trivia questions to be taken from
    def __init__(self,bot,message_ids,players_list,players_dict,waitingroom):
        self.bot = bot
        self.display_msg = None
        self.message_ids =copy.deepcopy(message_ids)
        self.players_list = copy.deepcopy(players_list)
        self.players_dict = copy.deepcopy(players_dict)
        self.display_text = None
        self.list_for_category = random.sample(variables.categories,5)
        print(f"This are the categories to be voted for {self.list_for_category}")
        self.category_list = self.list_for_category
        variables.pause = False
        variables.contvar = False
        self.waitingroom = waitingroom
        asyncio.create_task(self.update_msg_for_voting(self.waitingroom))
        for i in players_list: # this will make the variables.vote variable to be false so the user can vote after the user vote the variable will be set to true
            variables.vote[i] = False
        
    async def update_msg_for_voting(self,waitingroom): #This method will update the message for the voting message
        self.start_time = time.time()
        while waitingroom.start_game_timer > 1:
            await asyncio.sleep(2)
            time_elapsed = time.time()-self.start_time
            waitingroom.start_game_timer = 10 - int(time_elapsed)
            self.rewrite_msg_for_voting(waitingroom)
            print(f"These are the message ids: {self.message_ids}")
            print("about to update message")
            print(f"this are the players list {self.players_list}")
            for i in self.players_list:
                print(f"this is the message id's for the game {self.message_ids}")
                print(f"this are the numbers of players in the game {self.players_list}")
                print(f"updating message for {i}")
                await self.bot.edit_message_text(self.display_msg,i,self.message_ids[str(i)],reply_markup=variables.choice_button)
                print(f"updating message for {i} is finished")
        self.category = await functions.find_max_green_option(self.display_msg,self.category_list)
        game_key = functions.random_alphabet_string(10)
        print(f"1category questions are gotten from {self.category}")
        for i in self.players_list: # This will loop through get all the player list id and store the game object created in the user_gaming_room
            # dictionary for them
            variables.user_gaming_room[str(i)] = game_key 
            await self.bot.edit_message_text(variables.quickfire_trivia_game_rule,i,self.message_ids[str(i)])
        
        await asyncio.sleep(10)           
        variables.gaming_room[game_key] = Game.TriviaGame(self.bot,self.message_ids,self.players_list,self.players_dict,self.category)

    def rewrite_msg_for_voting(self,waitingroom):
        self.display_text = f"\t\t⏱️ Timer: ⏱️: {waitingroom.start_game_timer}(s)\n\n🗳️ Questions will be coming from all categories, but still vote for the category you want more questions to be drawn from in the game! 🎯 \n\n\n"
        self.count = 1

        for i in self.category_list: # This loop will run 5 times in other to get 5 catetgories for the user to choose
            self.display_text += f"{self.count}.\t{i}\n\n"
            self.count += 1      
        self.display_msg = self.display_text
    
    def reset_attributes(self): # This will reset all the main attributes of this class
        self.display_msg = None
        self.message_ids = None
        self.players_list = None
        self.players_dict = None
        self.display_text = None