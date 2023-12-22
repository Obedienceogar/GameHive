# This script is going to contain a user class and an admin class which will inherit from the user class to make it easy to create
# Telegram bots

# All libraries to be used in this program will be included below
import json
import variables

class User():
    def __init__(self,id,referby=None):
        self.data_file_address = variables.data_file_address # Thsi is the address where the json file for storing the user's data is located 

        self.id = str(id) # Thsi is the telegram user's id 
        # Initialize the dictionary to load all the users information 
        self.referby = referby # This will store the user referrer's id
        self.data = {}
        with open(self.data_file_address,"r") as f:
            self.data = json.load(f)
        self.all_users = self.data['users']
        self.active_users = self.data['active_users']
        # This part of the if code will run if the class is initialized and the user's id is found in the active_user list
        # In the data.json file
        if self.id in self.data['active_users']: 
            self.wallet = self.data['wallet'][self.id]
            self.valid_referral_list = self.data['valid_referral_list'][self.id]
            self.referby = self.data['referby'][self.id]
            self.balance = self.data['balance'][self.id]
            self.games_played = self.data['games_played'][self.id]
            self.unverified_referrals = self.data['unverified_referrals'][self.id]
            self.total_user_withdrawals = self.data['total_user_withdrawals'][self.id]
            self.total_earnings = self.data['total_earnings'][self.id]
            self.total_withdrawals = self.data['total_withdrawals']
            self.verifed = self.data['verified'][self.id]
        
        # This elif block of code will run if the class is initialized and the user's id is found in the inactive_user list
        # In the data.json file
        elif self.id in self.data['banned_users']:
            self.wallet = self.data['wallet'][self.id]
            self.valid_referral_list = self.data['valid_referral_list'][self.id]
            self.referby = self.data['referby'][self.id]
            self.balance = self.data['balance'][self.id]
            self.games_played = self.data['games_played'][self.id]
            self.unverified_referrals = self.data['unverified_referrals'][self.id]
            self.total_user_withdrawals = self.data['total_user_withdrawals'][self.id]
            self.total_earnings = self.data['total_earnings'][self.id]
            self.total_withdrawals = self.data['total_withdrawals']
            self.verified = self.data['verified'][self.id]

        # With the help of this block of code i have been able to tackle the referral problem i have been having
        # With this block of code if a user starts the bot and the user id has been found in the inactive_user list the user
        # referby data will not be touched but all other attributes will be overwritten and saved with a new value making it 
        # it possible for the first person that refers the user to be the only true and valid referrer without his position
        # To be taken
        elif self.id in self.data['inactive_users']:
            self.data['wallet'][self.id] = None
            self.data['valid_referral_list'][self.id] = []
            self.data['balance'][self.id] = float(0)
            self.data['games_played'][self.id] = 0
            self.data['unverified_referrals'][self.id] = []
            self.data['total_user_withdrawals'][self.id] = float(0)
            self.data['total_earnings'][self.id] = float(0)
            self.data['verified'][self.id] = False
            
            with open(self.data_file_address,"w") as f: # This will automatically write the users data to the data.json file
                json.dump(self.data,f,indent=4)
        # This else block of code will run if the the above conditions are not fuffilled. This else block will only run if the
        # class is intialized and the user is a new user 
        else:
            self.data['wallet'][self.id] = None
            self.data['valid_referral_list'][self.id] = []
            self.data['referby'][self.id] = referby
            self.data['balance'][self.id] = float(0)
            self.data['games_played'][self.id] = 0
            self.data['unverified_referrals'][self.id] = []
            self.data['total_user_withdrawals'][self.id] = float(0)
            self.data['total_earnings'][self.id] = float(0)
            self.data['verified'][self.id] = False
            with open(self.data_file_address,"w") as f: # This will automatically write the users data to the data.json file
                json.dump(self.data,f,indent=4)
   
    def check_user(self):
        self.data_check_user = self.return_data()

        # Use the data returned by the return_data funcion to check for the user's status
        for i in self.data_check_user['active_users']:
            if i == self.id:
                return 1
            else:
                pass
        for i in self.data_check_user['inactive_users']:
            if i == self.id:
                return 3
            else:
                pass
        for i in self.data_check_user['banned_users']:
            if i == self.id:
                return 2
            else:
                pass
        for i in self.data_check_user['users']:
            if i == self.id:
                return 0
            else: 
                return 4 # This will signify the user is a new user of the bot
        # The return type signifies who the user is for e.g if the function returns 0 it means the telegram user is a user of the bot
        # If the return type is 1 it means the telegram user is an active user that is someone who has already started the bot and is using it
        # If the return type is 2 it means the telegram user is a banned user
        # If it returns 4 it means the user is a new user 
        # With this now i can use an else statement in the main.py to handle new users who send the /start command or any text
        # or return type 4 can be userd by the main.py to know that the user is a new user
        
    def return_data(self): # This method returns the entire data.json file or the dictionary file for a specific user
        self.data_file = {}
        with open(self.data_file_address,'r') as f:
            self.data_file = json.load(f)
        
        return self.data_file

    def add_user(self,user=None,active_user=None,inactive_users=None): # This method adds to the user list or the active user list or the banned list
        if user == True:
            self.data_file = {}
            with open(self.data_file_address,'r') as f:
                self.data_file = json.load(f)
            if self.id not in self.data_file['users']:
                self.data_file['users'].append(self.id)
            with open(self.data_file_address,'w') as f:
                json.dump(self.data_file,f,indent=4)
        if active_user == True:
            self.data_file = {}
            with open(self.data_file_address,'r') as f:
                self.data_file = json.load(f)
            if self.id not in self.data_file['active_users']:
                self.data_file['active_users'].append(self.id)
            with open(self.data_file_address,'w') as f:
                json.dump(self.data_file,f,indent=4)
        if inactive_users == True:
            self.data_file = {}
            with open(self.data_file_address,'r') as f:
                self.data_file = json.load(f)
            if self.id not in self.data_file['inactive_users']:
                self.data_file['inactive_users'].append(self.id)
            with open(self.data_file_address,'w') as f:
                json.dump(self.data_file,f,indent=4)

    def officiate_user(self): # this method will remove the user from the inactive_user list and adds the user to the active_user list
        self.data_file = {}
        with open(self.data_file_address,'r') as f:
            self.data_file = json.load(f)
        if self.id in self.data_file['inactive_users']:
            self.data_file['inactive_users'].remove(self.id)
        if self.id not in self.data_file['active_users']:
            self.data_file['active_users'].append(self.id)
        with open(self.data_file_address,'w') as f:
            json.dump(self.data_file,f,indent=4)
    
    def ban_user(self): # This method will be used to ban the user
        self.data_file = {}
        with open(self.data_file_address,'r') as f:
            self.data_file = json.load(f)
        self.data_file['banned_users'].append(self.id)
        self.data_file['active_users'].remove(self.id)
        with open(self.data_file_address,'w') as f:
            json.dump(self.data_file,f,indent=4)
    
    def increment_referrers_referrals(self,referby): # I will be using this method to update the user's referrer referals list
        # If it's a bit confusing then take 10 seconds have a deep breath and read the above comment gently then you should 
        # understand
        self.file = {}
        with open(self.data_file_address,'r') as f:
            self.file = json.load(f)
        if self.id in self.file['unverified_referrals'][str(referby)]:
            pass
        else:
            self.file['unverified_referrals'][str(referby)].append(self.id) # This does the main trick of adding to the referrers referrals list
        # with the id of the telegram user that was being reffered 
        # Take my advice from the first comment section take a deep breath for at least 10 seconds and then read the above 
        # comment again if you do not understand
        with open(self.data_file_address,'w') as f:
            json.dump(self.file,f,indent=4)
    
    def increase_bot_withdrawals(self,value):# This function will be able to increase the total number of withdrawals in usd the 
        # Bot has processed since inception
        self.user_data_file = {}
        with open(self.data_file_address,'r') as f:
            self.user_data_file = json.load(f)
        self.user_data_file['total_withdrawals'] += float(value)
        self.user_data_file['total_user_withdrawals'][self.id] += float(value) # This will increment the total number of
        with open(self.data_file_address,'w') as f:
            json.dump(self.user_data_file,f,indent=4)
            
    def increase_balance(self,value): # This method will increase the users balance 
        self.user_data_file = {}
        with open(self.data_file_address,'r') as f:
            self.user_data_file = json.load(f)
        self.balance += float(value)
        self.user_data_file['balance'][self.id] += float(value)
        with open(self.data_file_address,'w') as f:
            json.dump(self.user_data_file,f,indent=4)
    
    def increase_games_played(self,userid): # this method will increase the numbers of games the user has played by one since when
        # the user plays a game once all the time so the number of games the user has played should be incremented by one
        self.user_data_file = {}
        with open(self.data_file_address,'r') as f:
            self.user_data_file = json.load(f)
        self.games_played += 1
        self.user_data_file['games_played'][userid] += 1
        with open(self.data_file_address,'w') as f:
            json.dump(self.user_data_file,f,indent=4)
        
    def evaluate_user_status(self):# This method will evaluate a user's account, checking if he has played at least
        # 5 games if the user has played 5 games it will then return a True Value if the amount of games the user has played
        # is not equal to five then the it will return a boolean False value
        print(f"{self.id} played this number of games {self.games_played}")
        if self.games_played <= 5:
            return False
        else:
            return True
        
    def update_ref_referrals(self,ref): # this method will be used to increase a particular user's referral
        self.user_data_file = {}
        with open(self.data_file_address,'r') as f:
            self.user_data_file = json.load(f)
        self.user_data_file['valid_referral_list'][ref].append(self.user_data_file['unverified_referrals'][ref].pop(self.user_data_file['unverified_referrals'][ref].index(self.id))) # this line of code will append the current user to the list of valid referrals of the referrer by going to the list that stores the total number 
        # of unverified referrals that a user has collecting the id of the user referral that has just verified his account by playing 5 games then getting the index position of the id in the referrer's unverified_referrals list and then returning it to the pop method which then removes it from the unverified_users list and put it
        # in the valid_referral_list
        with open(self.data_file_address,'w') as f:
            json.dump(self.user_data_file,f,indent=4)
    
    def get_games_played(self): # this method will returns the number of games the user has played so far
        return self.games_played # this will return the total number of games the user has called when called

    def total_referrals(self): # this method will return the total number of referrals the bot has 
        return len(self.unverified_referrals) + len(self.valid_referral_list)