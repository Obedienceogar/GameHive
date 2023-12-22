import asyncio
import time
import functions
from urllib.parse import unquote
import random
import variables
from aiogram import types
import random
import user
import copy
from aiogram.dispatcher import FSMContext

class EliminationTriviaGame():
    """When a user send the wants to play the elimination trivia game this class is instantiated
    cause this class is the one that will be controling the gaming in the bot"""
    def __init__(self,bot,message_ids,players_list,players_dict,category):
        variables.elim_vote = {} # make the vote dictionary that keeps track of the option that users voted for to be empty to avoid confusion when they try to vote again
        self.len_users = len(players_list)
        self.bot = bot 
        self.game_room = variables.user_gaming_room[str(players_list[-1])]
        self.winner = None # this variable will store the user id of the winner
        self.enter_runner_ups = False # This is a flag variable that will allow the bot to record the runner ups in the game
        self.runner_ups = [] ## This list stores the user id's of the runner ups in the game if there are two runner ups then the list will store two id's 
        # and since we will be using the append method to add value to the list we know that the last value in the list is the third runner up and the first 
        # value in the list is the second runner up
        self.players_list = players_list # This is the list of all the players currently playing the game and have not yet been eliminated
        self.users_choice = {'self.a':{},'self.b':{},'self.c':{},'self.d':{}} # This will store the user's choice and will also be used to update the particular user's message to simulate voting
        self.trivia_difficulty = 0 # This is the value that will be passed over to the get_trivia_questions function to retrieve questions based on the difficulty
        self.game_info = functions.get_trivia_questions(functions.get_category_id(category))
        self.opt = ['self.a','self.b','self.c','self.d']
        self.normal_option_and_answer = {'self.a':"",'self.b':"",'self.c':"",'self.d':"",'correct_answer':"",'question':""} # this dictionary contains the correct untainted values for each option in each round this is necessary because the only copy of the options and values for each round is in the
        for i in players_list: # this will initialize the values of the users_choice dicitonary
            variables.elim_users_answered[str(i)] = None # initializes a dictionary to store a boolean value later to check if the users have answered in a given round or not
            for j in range(4):
                self.users_choice[self.opt[j]][str(i)] = str(f"")
        self.update_attributes(initialized=True) # This will call the update_attributes function and update both the normal_option_and_answer dictionary and the users_choice dictionary

        self.players_dict = players_dict # This is a dictionary with it's key as the id of players and its value it the full names of players
        self.message_ids = message_ids # This dictionary contains all the id's of the messages that will be edited to simulate active multiplayer gaming
        self.eliminated_players = [] # This list will keep track of eliminated players
        self.round = 0 # This stores the current round of the game
        self.correct_answer = "" # This will store the correct answer of each round
        self.question = None # This will contain the current question
        self.display_msg = None # This is defined now to avoid an attribute error later but it will be used to store message to be displayed 
        self.timer = 10
        self.user_answered = [] # This list will store the number of people that answered per round, if a user id is not found
        # in this list it is considered that he did not vote and he will be removed
        # initialized
        # users_choice dictinary and there is a probability that the value will be mutilated so it is best to be saved somewhere else for easy retrival and to avoid being mutilated
        self.timer = 15 # This is the time per round
        asyncio.create_task(self.game()) # This will start the game method which is the main method that controls the game
        self.elim_users = [] # This will contain the users that will be eliminated after each round
        
    async def next_round(self): # This will introduce the next round of the game
        for i in self.players_list: # This will loop through the players_list and allow all users to be able to answer the question for the next round
            variables.elim_users_answered[str(i)] = False # Flag to make sure once a user answer a question he can't give another answer again
        self.round += 1
        for i in self.players_list:
            await self.bot.edit_message_text(f"Round {self.round + 1}",i,self.message_ids[str(i)])
        await asyncio.sleep(4)
        self.user_answered = []
        self.timer = 10
        self.update_attributes()
        await self.update_message()
        print(f"This is th correct answer for this round {self.correct_answer}")
    
    async def game(self): # This will keep track of the time and then call the next round method once the timer is up
        while self.players_list and self.return_game_status() == True:
            self.start_time = time.time()
            await asyncio.sleep(2)
            self.time_elapsed = time.time()-self.start_time
            self.timer = self.timer-int(self.time_elapsed) # this updates the timer 
            await self.update_message() # this calls the update_message() method to edit the message to reflect changes in time and print the message to the user
            print(f"i am close to the self.timer\nthe self.timer value is {self.timer}")
            if self.timer <= 0:
                await self.analyze_round() # This will be responsible for determining if a player will be eliminated or not

                if self.elim_users != []:
                    self.elim_users_msg = "The following user(s) have been eliminated\n"
                    await asyncio.sleep(4)
                    for i in self.elim_users:# This will construct the eliminated users message to be outputed to the remaining users of the game
                        self.elim_users_msg += f"\n{self.players_dict[str(i)]}"
                    # This will output the users that have been eliminated to the remaining users in the game
                    for i in self.players_list:
                        await self.bot.edit_message_text(self.elim_users_msg.strip(),i,self.message_ids[str(i)])
                        await asyncio.sleep(5)
                        self.elim_users = [] #This will empty the elim users attribute
                else:
                    pass

                if len(self.players_list) == 1: # This block of code brings out the winner of each game
                    self.winner = self.players_list[0]
                    break
                else:
                    pass

                await self.next_round()                    
            else:
                pass 
        
        await self.end_game()
        
    async def remove_user(self,id,reason): # This will remove a user from the players_list and put in the eliminated_players list and then alert 
        # The user that he has been eliminated
        self.menu_keyboard = functions.menu(id)
        print(f"I am talking from the remove_user functionin the game class and i am telling you \n That this are the\
number of players in the game {self.players_list}")
        self.index_position = self.players_list.index(str(id))
        self.popped_value = self.players_list.pop(self.index_position)
        self.eliminated_players.append(self.popped_value) # This will remove the user when the method remove_user is called
        if reason == "Wrong answer":
            await self.bot.edit_message_text("You provided a wrong answer\nYou have been eliminated",str(id),self.message_ids[str(id)])
            await self.bot.send_message(id,"🏡",reply_markup=self.menu_keyboard)
        elif reason == "Delay":
            await self.bot.edit_message_text("You've been eliminated because you delayed in answering",str(id),self.message_ids[str(id)])
            await self.bot.send_message(id,"🏡",reply_markup=self.menu_keyboard)
        else:
            pass

    async def update_message(self):
        self.msg = f"\t\tTimer:\t\t{self.timer}\n\nRound {self.round + 1}\t\t"
        self.msg += f"\n\nQuestion: {self.normal_option_and_answer['question']}\n\n\n"
        self.options = ['self.a','self.b','self.c','self.d']
        self.letters = ['A','B','C','D']
        for j in self.players_list:
            try:
                for i, option_value in enumerate(self.options):
                    self.msg += f"{self.letters[i]}.\t{str(self.users_choice[option_value][str(j)])}\n\n"

                await self.bot.edit_message_text(self.msg,j,self.message_ids[str(j)],reply_markup=self.generate_markup_keyboard())
                self.msg = f"\t\tTimer:\t\t{self.timer}\n\nRound {self.round + 1}\t\t" # This resets the self.msg variable to it's original state for the next loop
                self.msg += f"\n\nQuestion: {self.normal_option_and_answer['question']}\n\n\n"
            except Exception as e:
                print(f"There was an error in the update_function\nThe error was {e}")
    
    async def end_game(self):
        # First of all pay all winners and alert them of their payment
        if self.winner == None: # if there are no winners then this block of code will run because if they are no winners
            # in the game then the
            for i in self.eliminated_players[:]:
                self.menu_keyboard = functions.menu(i)
                self.user = user.User(i)
                self.temp_balance = functions.elimination_construct_amount_to_be_paid(self.len_users,winner=False,no_winner=True)
                self.user.increase_balance(self.temp_balance)
                self.user.increase_games_played(i) # This wlll add one to the total number of games played by the user
                await self.bot.send_message(str(i),f"You've been given ${self.temp_balance} for participating in a game")
                await functions.referrals_function(i,self.bot) # this function is responsible for taking care of everythin relating to the referral system
           
        else: # incase there are no winners in the game then no error will come out when the end_game function is called
            self.menu_keyboard = functions.menu(self.winner)
            print("else block ran for the end game method")
            print(f"this are the total number of users in the game {self.players_list}")
            print(f"this is the winner of the game {self.winner}") 
            self.user = user.User(str(self.winner))
            self.temp_balance = functions.elimination_construct_amount_to_be_paid(self.len_users,winner=True,no_winner=False) # This is a variable that will store the amount to be paid to the user i am doing this so i don't call the function that generate how much a user will be paid twice                
            self.user.increase_balance(self.temp_balance)
            self.user.increase_games_played(self.winner) # this will add one to the number of games played by the user
            await self.bot.edit_message_text(f"Congrats you came first in your last game\nYour balance has been increased by ${self.temp_balance}",str(self.winner),self.message_ids[self.winner])
            await asyncio.sleep(5)
            await functions.referrals_function(self.winner,self.bot) # this function is responsible for taking care of everythin relating to the referral system
            
            for i in self.eliminated_players: # now remaining users should be credited
                print("for loop in the else block in the end game() method ran")
                self.user = user.User(i)
                self.temp_balance = functions.elimination_construct_amount_to_be_paid(self.len_users,winner=False,no_winner=False)
                self.user.increase_balance(self.temp_balance)
                self.user.increase_games_played(i) # this will add one to the total number of games played by the user
                await self.bot.send_message(str(i),f"You've been given ${self.temp_balance} for participating in a game")
                await functions.referrals_function(i,self.bot) # this function is responsible for taking care of everythin relating to the referral system
        # retrieve the game dictioary so as to delete the game class in the key's value
        del variables.gaming_room[self.game_room] # This will delete the gaming instance
        
    def update_attributes(self,initialized=False): # This will update all the main neccessary attributes required for the game to function like the options attribues and the question attributes
        # using the exec function and a for loop wasn't too effective for me to use and assign each option values so i am using this method
        # where all the options both incorect andn correct are stored in one list and then randomly they are picked and assigned to the different options
        # after which they are removed from the optins_list to avoid assigning one item to two or more options attribute
        if initialized == True:
            self.dictionary = self.game_info[0]
        else:
            self.dictionary = self.game_info[self.round]
        self.options_values_list = self.dictionary['incorrect_answers'] # This list will contain all the options item
        self.options_values_list.append(self.dictionary['correct_answer'])
        self.options = ['self.a','self.b','self.c','self.d']
        for i in range(4):
            self.choice =  random.choice(self.options_values_list) # This will store the random item picked from the list
            self.normal_option_and_answer[self.options[i]] = self.choice
            self.options_values_list.remove(self.choice)
            
        for i in self.players_list:
            for j in self.options:
                self.users_choice[j][str(i)] = self.normal_option_and_answer[j]

        self.question = self.dictionary['question']
        self.correct_answer = self.dictionary['correct_answer'] # This will set the correct_answer attribute to the correct answer so that lalater in the main part of the program whent the person 
        # taps on any inline keyboard button the inline keyboard will compare the variable with the argument it recieved from the callback_data 
        self.normal_option_and_answer['correct_answer'] = self.dictionary['correct_answer']
        self.normal_option_and_answer['question'] = self.dictionary['question']
        print(f"New correct_answer = {self.normal_option_and_answer['correct_answer'].lower()}")
        print(self.normal_option_and_answer)
        print(f"This is the correc_answer: {self.correct_answer}")
    def generate_markup_keyboard(self):
        self.keyboard = types.InlineKeyboardMarkup()
        
        self.callback_data_options = ['self.a','self.b','self.c','self.d'] # This list will be used to get the value of the option picked by the user from the users_choice variable dictionary

        self.letters = ['A','B','C','D']
        
        for i in range(4):
            self.keyboard.row(types.InlineKeyboardButton(text=self.letters[i],callback_data=f"answerelim:{self.normal_option_and_answer[self.callback_data_options[i]]}"))

        return self.keyboard          
        
    def return_game_status(self): # This will contain necessary conditions to end the game
        if len(self.players_list) > 1:
            return True
        elif len(self.players_list) == 1:
            self.winner = self.players_list[0] # this index position will grab the player id that is still in the game that is the winner
            return False # Game ends when this function return false to the gaming loop
    
    async def highlight_users_option(self,option,id): # This will collect the option from the user check the attribute that has that 
        # value and then append a green emoji to signify the users choice
        id = str(id)
        if option.lower() == self.normal_option_and_answer['self.a'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.a'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.b'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.b'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.c'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.c'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.d'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.d'][id] = str(new_string)
        else:
            print(f"i did not work\nI was passed this argument{option}\n i am the highlight bla bla bla funciton")

    async def analyze_round(self): # This function will be responsible for analyzing each round, determining fi a user should be eliminated
        # First of all check if a user answsered in a particular round by checking the user_choice dictionary with the users
        # id and then check if there is the green emoji at the end, if there is a green emoji that mean s the user had answered
        # A question if not that means the user did not answer which mean he delayed then the user will be removed from the game
        # on the basis of delay 
        for i in self.players_list[:]: # will be accessing the list of all players in the game to determine if the user should be eliminated
            print(f"Current iter {i}")
            for j in self.opt: # loop through self.options variable per each player that the previous loop temporary variable gets
                print(f"Current option iter {j}")
                self.flag = self.users_choice[j][i].endswith("🟢")
                if variables.elim_users_answered[i] == True: # This block of code will run if the user selected an option
                    if self.flag == True: # if the self.flag variable is equal to True that means that the user answered the question in the current round
                        print(f"I am from the self.flag block not the else block")
                        self.temp_option = self.users_choice[j][i] # This will store the option selected by the user since j is the temproary variable that contains the option selected by the user
                        if self.temp_option[:-1].strip().lower() == self.normal_option_and_answer['correct_answer'].lower():
                            pass # if a user should get the corrrect answer then no action will be taken against the user thereby making the user to remain in the game
                        else: # that means the user failed
                            await self.remove_user(i,reason="Wrong answer") # The user will be removed from the game on account of wrong answer
                    else:# This block of code will run if the current option evaluated does not have the green emoji at the end of the string
                        pass
                else:# if this block of code runs that means the user did not answer any questions
                    print(f"I am from the else block not the self.flag block")
                    await self.remove_user(i,reason="Delay")
                    break

class TriviaGame():
    """When a user send the wants to play the elimination trivia game this class is instantiated
    cause this class is the one that will be controling the gaming in the bot"""
    def __init__(self,bot,message_ids,players_list,players_dict,category):
        variables.elim_vote = {} # make the vote dictionary that keeps track of the option that users voted for to be empty to avoid confusion when they try to vote again
        self.len_users = len(players_list)
        self.bot = bot 
        self.game_room = variables.user_gaming_room[str(players_list[-1])]
        self.winner = None # this variable will store the user id of the winner
        self.enter_runner_ups = False # This is a flag variable that will allow the bot to record the runner ups in the game
        self.runner_ups = [] ## This list stores the user id's of the runner ups in the game if there are two runner ups then the list will store two id's 
        # and since we will be using the append method to add value to the list we know that the last value in the list is the third runner up and the first 
        # value in the list is the second runner up
        self.players_list = players_list # This is the list of all the players currently playing the game and have not yet been eliminated
        self.users_choice = {'self.a':{},'self.b':{},'self.c':{},'self.d':{}} # This will store the user's choice and will also be used to update the particular user's message to simulate voting
        self.trivia_difficulty = 0 # This is the value that will be passed over to the get_trivia_questions function to retrieve questions based on the difficulty
        self.game_info = functions.get_trivia_questions(functions.get_category_id(category))
        self.opt = ['self.a','self.b','self.c','self.d']
        self.normal_option_and_answer = {'self.a':"",'self.b':"",'self.c':"",'self.d':"",'correct_answer':"",'question':""} # this dictionary contains the correct untainted values for each option in each round this is necessary because the only copy of the options and values for each round is in the
        for i in players_list: # this will initialize the values of the users_choice dicitonary
            variables.users_answered[str(i)] = None # initializes a dictionary to store a boolean value later to check if the users have answered in a given round or not
            for j in range(4):
                self.users_choice[self.opt[j]][str(i)] = str(f"")
        self.update_attributes(initialized=True) # This will call the update_attributes function and update both the normal_option_and_answer dictionary and the users_choice dictionary

        self.players_dict = players_dict # This is a dictionary with it's key as the id of players and its value it the full names of players
        self.message_ids = message_ids # This dictionary contains all the id's of the messages that will be edited to simulate active multiplayer gaming
        self.eliminated_players = [] # This list will keep track of eliminated players
        self.round = 0 # This stores the current round of the game
        self.correct_answer = "" # This will store the correct answer of each round
        self.question = None # This will contain the current question
        self.display_msg = None # This is defined now to avoid an attribute error later but it will be used to store message to be displayed 
        self.timer = 10
        self.user_answered = [] # This list will store the number of people that answered per round, if a user id is not found
        # in this list it is considered that he did not vote and he will be removed
        # initialized
        # users_choice dictinary and there is a probability that the value will be mutilated so it is best to be saved somewhere else for easy retrival and to avoid being mutilated
        self.timer = 15 # This is the time per round
        print("About to start game function")
        asyncio.create_task(self.game()) # This will start the game method which is the main method that controls the game
        print("Game function successfully started")
        self.elim_users = [] # This will contain the users that will be eliminated after each round
        self.income_per_round = 0.0005 # This is the amount of money that will be given to each user after the user has gotten one question correctly
        
    async def next_round(self): # This will introduce the next round of the game
        for i in self.players_list: # This will loop through the players_list and allow all users to be able to answer the question for the next round
            variables.users_answered[str(i)] = False # Flag to make sure once a user answer a question he can't give another answer again
        self.round += 1
        for i in self.players_list:
            await self.bot.edit_message_text(f"Round {self.round + 1}",i,self.message_ids[str(i)])
        await asyncio.sleep(4)
        self.user_answered = []
        self.timer = 10
        self.update_attributes()
        print('About to execute the self.update_message() method')
        await self.update_message()
        print("Execution of the self.update_message method done")
        print(f"This is th correct answer for this round {self.correct_answer}")
    
    async def game(self): # This will keep track of the time and then call the next round method once the timer is up
        while self.players_list:
            self.start_time = time.time()
            await asyncio.sleep(2)
            self.time_elapsed = time.time()-self.start_time
            self.timer = self.timer-int(self.time_elapsed) # this updates the timer 
            await self.update_message() # this calls the update_message() method to edit the message to reflect changes in time and print the message to the user
            if self.timer <= 0:
                await self.analyze_round() # This will be responsible for determining if a player will be eliminated or not

                if self.elim_users != []:
                    self.elim_users_msg = "The following user(s) have been eliminated\n"
                    await asyncio.sleep(4)
                    for i in self.elim_users:# This will construct the eliminated users message to be outputed to the remaining users of the game
                        self.elim_users_msg += f"\n{self.players_dict[str(i)]}"
                    # This will output the users that have been eliminated to the remaining users in the game
                    for i in self.players_list:
                        await self.bot.edit_message_text(self.elim_users_msg.strip(),i,self.message_ids[str(i)])
                        await asyncio.sleep(5)
                        self.elim_users = [] #This will empty the elim users attribute
                else:
                    pass
                # Since in thsi game each user is played per each question gotten correctly by the user so the user's balance has to be 
                # increased before the next round of the game
                for i in self.players_list[:]: # by the time this loop is to be executed all the user's in the self.players_list must have answered the last question
                    # Successfully so as to remain in the self.players_list so we will only be incrementing the balance of real players
                    self.user = user.User(i)
                    self.user.increase_balance(self.income_per_round) # this will increase the user's balance with the income per round attribute in the trivia game class
                    await self.bot.edit_message_text(f"Correct ${self.income_per_round} has been added to your bot balance",i,self.message_ids[str(i)])
                    await asyncio.sleep(3)

                await self.next_round()                    
            else:
                pass 
        
        await self.end_game()
        
    async def remove_user(self,id,reason): # This will remove a user from the players_list and put in the eliminated_players list and then alert 
        # The user that he has been eliminated
        self.menu_keyboard = functions.menu(id)
        self.eliminated_players.append(self.players_list.pop(self.players_list.index(str(id)))) # This will remove the user when the method remove_user is called
        if reason == "Wrong answer":
            await self.bot.edit_message_text("You provided a wrong answer\nYou have been eliminated",str(id),self.message_ids[str(id)])
            await self.bot.send_message(id,"🏡",reply_markup=self.menu_keyboard)
        elif reason == "Delay":
            await self.bot.edit_message_text("You've been eliminated cause you delayed in answering",str(id),self.message_ids[str(id)])
            await self.bot.send_message(id,"🏡",reply_markup=self.menu_keyboard)
        else:
            pass

    async def update_message(self):
        self.msg = f"\t\tTimer:\t\t{self.timer}\n\nRound {self.round + 1}\t\t"
        self.msg += f"\n\nQuestion: {self.normal_option_and_answer['question']}\n\n\n"
        self.options = ['self.a','self.b','self.c','self.d']
        self.letters = ['A','B','C','D']
        print(f"Hello i am from the update_message function and i am here to report that this are the total numbaer of players in this game {self.players_list}")
        for j in self.players_list:
            try:
                for i, option_value in enumerate(self.options):
                    self.msg += f"{self.letters[i]}.\t{str(self.users_choice[option_value][str(j)])}\n\n"

                await self.bot.edit_message_text(self.msg,j,self.message_ids[str(j)],reply_markup=self.generate_markup_keyboard())
                self.msg = f"\t\tTimer:\t\t{self.timer}\n\nRound {self.round + 1}\t\t" # This resets the self.msg variable to it's original state for the next loop
                self.msg += f"\n\nQuestion: {self.normal_option_and_answer['question']}\n\n\n"
            except Exception as e:
                print(f"There was an error in the update_function\nThe error was {e}")
    
    async def end_game(self):
        # We'll just do some cleanup here only
        del variables.gaming_room[self.game_room] # This will delete the gaming instance
        
    def update_attributes(self,initialized=False): # This will update all the main neccessary attributes required for the game to function like the options attribues and the question attributes
        # using the exec function and a for loop wasn't too effective for me to use and assign each option values so i am using this method
        # where all the options both incorect andn correct are stored in one list and then randomly they are picked and assigned to the different options
        # after which they are removed from the optins_list to avoid assigning one item to two or more options attribute
        if initialized == True:
            self.dictionary = self.game_info[0]
        else:
            self.dictionary = self.game_info[self.round]
        self.options_values_list = self.dictionary['incorrect_answers'] # This list will contain all the options item
        self.options_values_list.append(self.dictionary['correct_answer'])
        self.options = ['self.a','self.b','self.c','self.d']
        for i in range(4):
            self.choice =  random.choice(self.options_values_list) # This will store the random item picked from the list
            self.normal_option_and_answer[self.options[i]] = self.choice
            self.options_values_list.remove(self.choice)
            
        for i in self.players_list:
            for j in self.options:
                self.users_choice[j][str(i)] = self.normal_option_and_answer[j]

        self.question = self.dictionary['question']
        self.correct_answer = self.dictionary['correct_answer'] # This will set the correct_answer attribute to the correct answer so that lalater in the main part of the program whent the person 
        # taps on any inline keyboard button the inline keyboard will compare the variable with the argument it recieved from the callback_data 
        self.normal_option_and_answer['correct_answer'] = self.dictionary['correct_answer']
        self.normal_option_and_answer['question'] = self.dictionary['question']
        print(f"New correct_answer = {self.normal_option_and_answer['correct_answer'].lower()}")
        print(self.normal_option_and_answer)
        print(f"This is the correc_answer: {self.correct_answer}")
    def generate_markup_keyboard(self):
        self.keyboard = types.InlineKeyboardMarkup()
        
        self.callback_data_options = ['self.a','self.b','self.c','self.d'] # This list will be used to get the value of the option picked by the user from the users_choice variable dictionary

        self.letters = ['A','B','C','D']
        
        for i in range(4):
            self.keyboard.row(types.InlineKeyboardButton(text=self.letters[i],callback_data=f"Answer:{self.normal_option_and_answer[self.callback_data_options[i]]}"))

        return self.keyboard          
    
    async def highlight_users_option(self,option,id): # This will collect the option from the user check the attribute that has that 
        # value and then append a green emoji to signify the users choice
        id = str(id)
        if option.lower() == self.normal_option_and_answer['self.a'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.a'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.b'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.b'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.c'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.c'][id] = str(new_string)
        elif option.lower() == self.normal_option_and_answer['self.d'].lower():
            new_string = f"{option.title()} 🟢"
            self.users_choice['self.d'][id] = str(new_string)
        else:
            print(f"i did not work\nI was passed this argument{option}\n i am the highlight bla bla bla funciton")
        
    async def analyze_round(self): # This function will be responsible for analyzing each round, determining fi a user should be eliminated
        # First of all check if a user answsered in a particular round by checking the user_choice dictionary with the users
        # id and then check if there is the green emoji at the end, if there is a green emoji that mean s the user had answered
        # A question if not that means the user did not answer which mean he delayed then the user will be removed from the game
        # on the basis of delay 
        for i in self.players_list[:]: # will be accessing the list of all players in the game to determine if the user should be eliminated
            print(f"Current iter {i}")
            for j in self.opt: # loop through self.options variable per each player that the previous loop temporary variable gets
                print(f"Current option iter {j}")
                self.flag = self.users_choice[j][i].endswith("🟢")
                if variables.users_answered[i] == True: # This block of code will run if the user selected an option
                    if self.flag == True: # if the self.flag variable is equal to True that means that the user answered the question in the current round
                        print(f"I am from the self.flag block not the else block\nyessna")
                        print("i am talking to you")
                        self.temp_option = self.users_choice[j][i] # This will store the option selected by the user since j is the temproary variable that contains the option selected by the user
                        print(f"This is the option selected by the user {self.temp_option}")
                        print(f"And this is the correct_answer {self.normal_option_and_answer['correct_answer']}")
                        if self.temp_option[:-1].strip().lower() == self.normal_option_and_answer['correct_answer'].lower():
                            pass # if a user should get the corrrect answer then no action will be taken against the user thereby making the user to remain in the game
                        else: # that means the user failed
                            await self.remove_user(i,reason="Wrong answer") # The user will be removed from the game on account of wrong answer
                    else:# This block of code will run if the current option evaluated does not have the green emoji at the end of the string
                        pass
                else:# if this block of code runs that means the user did not answer any questions
                    print(f"I am from the else block not the self.flag block")
                    await self.remove_user(i,reason="Delay")
                    break

    