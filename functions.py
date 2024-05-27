import asyncio
import time
import os 
import variables
import re
import random
import threading
import json
import requests
import string
from urllib.parse import unquote
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link
import user
from aiogram.utils.deep_linking import decode_payload

# Sample data
trivia_categories = {
    'trivia_categories': [
        {'id': 9, 'name': 'General Knowledge'},
        {'id': 10, 'name': 'Entertainment: Books'},
        {'id': 11, 'name': 'Entertainment: Film'},
        {'id': 12, 'name': 'Entertainment: Music'},
        {'id': 13, 'name': 'Entertainment: Musicals & Theatres'},
        {'id': 14, 'name': 'Entertainment: Television'},
        {'id': 15, 'name': 'Entertainment: Video Games'},
        {'id': 16, 'name': 'Entertainment: Board Games'},
        {'id': 17, 'name': 'Science & Nature'},
        {'id': 18, 'name': 'Science: Computers'},
        {'id': 19, 'name': 'Science: Mathematics'},
        {'id': 20, 'name': 'Mythology'},
        {'id': 21, 'name': 'Sports'},
        {'id': 22, 'name': 'Geography'},
        {'id': 23, 'name': 'History'},
        {'id': 24, 'name': 'Politics'},
        {'id': 25, 'name': 'Art'},
        {'id': 26, 'name': 'Celebrities'},
        {'id': 27, 'name': 'Animals'},
        {'id': 28, 'name': 'Vehicles'},
        {'id': 29, 'name': 'Entertainment: Comics'},
        {'id': 30, 'name': 'Science: Gadgets'},
        {'id': 31, 'name': 'Entertainment: Japanese Anime & Manga'},
        {'id': 32, 'name': 'Entertainment: Cartoon & Animations'}
    ]
}

def menu(chat_id):
    user = str(chat_id)
    admins = variables.ADMINS
    if user in admins:
        account = KeyboardButton('💼Account')
        playgames = KeyboardButton('🎮Play Games')
        referrals = KeyboardButton('👥Referrals')
        statistic = KeyboardButton('📊Statistics')
        balance = KeyboardButton('💰Balance')
        withdraw = KeyboardButton('💸Withdraw')
        support = KeyboardButton('🤖Support')
        help = KeyboardButton("📚Help")
        send_message = KeyboardButton("Send Message")
        enter_id = KeyboardButton("Enter Id")
        menukeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        menukeyboard.row(account,playgames,referrals)
        menukeyboard.row(statistic,balance,withdraw)
        menukeyboard.row(support,help,send_message)
        return menukeyboard
    else:
        account = KeyboardButton('💼Account')
        playgames = KeyboardButton('🎮Play Games')
        referrals = KeyboardButton('👥Referrals')
        statistic = KeyboardButton('📊Statistics')
        balance = KeyboardButton('💰Balance')
        withdraw = KeyboardButton('💸Withdraw')
        support = KeyboardButton('🤖Support')
        help = KeyboardButton("📚Help")
        menukeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        menukeyboard.row(account,playgames,referrals)
        menukeyboard.row(statistic,balance,withdraw)
        menukeyboard.row(support,help)
        return menukeyboard

async def start_game_function(waitingroom,id,bot):
    try:
        start_time = time.time()
        while len(waitingroom.players_list) < 10 and time.time()-start_time < 15: # it is 30 users are expected to stay in the waiting room for at least 30 seconds
            await asyncio.sleep(2)
            time_elapsed = time.time()-start_time
            waitingroom.timer = 60-int(time_elapsed)
            await waitingroom.display_and_update_msg(id)
            if time_elapsed >= 10:
                variables.pause = True
                print("Room Entering disabled")
            else: # I amm adding the else block just for fun
                print("Entering room is enabled")
                pass 
        
        variables.operate_start = time.time() #This is just for testing the time taken for the operations that are done in the middle of the end of the
        # start_game_function and the begining of the start_voting function
        await waitingroom.start_game(waitingroom)
    except Exception as e:
        await error_handler("This error is comming from the start_game_function in the functions module",e,bot)
async def elim_start_game_function(waitingroom,id,bot): # this is the start game function for the elimination trivia game
    try:
        start_time = time.time()
        while len(waitingroom.players_list) < 10 and time.time()-start_time < 60:
            await asyncio.sleep(2)
            time_elapsed = time.time()-start_time
            if waitingroom.timer > 1: # I am putting this else block of code there so as to avoid the timer from entering -1 second when counting down
                waitingroom.timer = 60-int(time_elapsed)
            else:
                waitingroom.timer = 0
            await waitingroom.display_and_update_msg(id)
            if time_elapsed >= 45: # once the number of seconds is less than 15 then the waiting room will not anymore user in the waiting room again 
                variables.elim_pause = True
                print("Entering room disabled")
            else: # I amm adding the else block just for fun
                pass 
                print("Entering room enabled")
        
        variables.operate_start = time.time() #This is just for testing the time taken for the operations that are done in the middle of the end of the
        # start_game_function and the begining of the start_voting function
        await waitingroom.start_game(waitingroom)
    except Exception as e:
        await error_handler("This error is comming from the elim_start_game_function in the funcitons module",e,bot)

async def find_max_green_option(options,category_list):
    max_count = 0
    max_option = None
    print(options)
    for option in options.split('\n'):
        if "🙋‍♂️" in option:
            count = option.count("🙋‍♂️")
            if count > max_count:
                max_count = count
                max_option = option
    # Check if a valid option was found
    print(f"option with highest value {max_option}")
    if max_option is not None:
        pattern = r'\d+|\.|🟢'
        # Use a regular expression to extract the main option text
        output_string = re.sub(pattern,'',max_option)
        str(output_string)
        output_string = output_string[:-5]
        output_string = output_string[1:]
        print(f"this is the output string{output_string}jtn")
        return output_string
    else:
        print("I am returning a random category")
        return random.choice(category_list)
    
async def start_voting(votingclass,waitingroom):
    # this part of this code involves allowing other users to enter the waiting room
    variables.pause = False
    variables.contvar = False
    await votingclass.update_msg_for_voting(waitingroom)
    
async def elim_start_voting(votingclass,waitingroom): # this is the start voting function for the elimination trivia game
    # this part of this code involves allowing other users to enter the waiting room
    variables.elim_pause = False
    variables.elim_contvar = False
    await votingclass.update_msg_for_voting(waitingroom)

async def current_users_status (bot): #This gets all the bot's active users status, it checks to see i they are
    # online or offline and then get the total count of online users as well as offline users and writes it 
    # to the data.json file
    data_file_address = variables.data_file_address 
    data = {}
    with open(data_file_address,"r") as f:
        data = json.load(f)

    online_users = 0 # To keep track of online users
    offline_users = 0 # To keep track of offline users
    for i in data['Users']:
        user = await bot.get_chat(i)
        
        if user.status == 'online':
            online_users += 1
        else:
            offline_users += 1
    
    user_status = {"online": f"{online_users}","offline": f"{offline_users}"}
    
    data = {}
    with open(variables.data_file_address,'r') as f:
        data = json.load(f)
    
    data['online_users'] = int(user_status['online'])
    data['offline_users'] = int(user_status['offline'])

    with open(variables.data_file_address,'w') as f:    
        json.dump(data,f,indent=4)

def get_category_id(category_name): # I don't think i need this function again
    for category in trivia_categories.get('trivia_categories', []):
        if category['name'] == category_name:
            print(category['id'])
            return category['id']
    return None  # Return None if the category name is not found
        
def get_questions_number(i,difficulty): # I don't think i need this function again
    id = get_category_id(i)
    response = requests.get(f"https://opentdb.com/api_count.php?category={id}")
    if response.status_code == 200:
        data = response.json()
        print(data)
        if difficulty == "easy":
            return data['category_question_count']['total_easy_question_count']
        elif difficulty == "medium":
            return data['category_question_count']['total_medium_question_count']
        elif difficulty == "hard":
            return data['category_question_count']['total_hard_question_count']
        else:
            pass # i will write this code once i begin the exception handling/error handling of this bot

def get_proxy_list():
    try:
        response = requests.get(variables.API_ENDPOINT_FOR_PROXY)
        if response.status_code == 200:
            proxy_list = response.text.split('\r\n')  # Split the response into a list of proxies
            print("i got the proxy list successfully")
            return proxy_list
        else:
            print(f"Failed to fetch proxy list. Status code: {response.status_code}")
    except Exception as e:
        pass
    return None

def get_trivia_questions(category,proxy=None):
    print(f"3Category questions are gotten from {category}")
    result = []
    for i in range(3):
        amount = 10
        BASE_URL = 'https://opentdb.com/api.php'
        params = {
            'amount': 10,  # Change the number of questions as needed
            'type': 'multiple',  # Multiple-choice questions
            'encode': 'url3986', # Encoding type
            'category': get_category_id(category),  # Fixed the typo here
            'difficulty': variables.trivia_difficulty[i]
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()  
            for i, question_data in enumerate(data['results'], start=1):
                question = unquote(question_data['question'])  # Decode the question
                correct_answer = unquote(question_data['correct_answer'])
                incorrect_answers = [unquote(ans) for ans in question_data['incorrect_answers']]  # Decode incorrect answers
                result.append({'question': question, 'correct_answer': correct_answer, 'incorrect_answers': incorrect_answers})
                random.shuffle(result)
            if result == []:
                print("Wahala for get_trivia_questions")
                
                print(data)
                
                time.sleep(5)

                get_trivia_questions(category)
            else:
                pass
        elif response.status_code == 429:
            print("Error code 429")
            proxy_lists = get_proxy_list()
        else:
            print(f"This is the data gotten from the opentdb retrieval {response.json()}")
            # You can add error handling here in the future
            return None
    return result 


def random_alphabet_string(length):
    alphabet = string.ascii_letters
    result = ''.join(random.choice(alphabet) for _ in range(length))
    return result

def get_category_id(category_name):
    count = 0
    for category in trivia_categories['trivia_categories']:
        if category['name'] == category_name:
            return trivia_categories['trivia_categories'][count]['id']
        count += 1
    return None  # Return None if the category name is not found 

def rule(users):
    if users == 1:
        rule = f"Rules\n\n1.\tThere are 15 questions for you to answer, you win once you get all questions correct\
\n\n2.\tYou have 30 seconds to provide an answer for each question, answer before your time runs out or else you get \
eliminated\n\n3.\tOnce you've selected an answer you will have to wait untill the timer countsdown before moving to the next question\
\n\n\n\n<b><i>Note: You still get paid even though you lose</i></b>"
        return rule
    elif users == 2:
        rule = f"🎮 Rules 🎮\n\n1. Once one player gets eliminated, the other player left wins the game 🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users ==3:
        rule = f"🎮 Rules 🎮\n\n1. The last player left in the game wins the game 🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 4:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 5:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 6:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 7:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 8:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    elif users == 9:
        rule = f"Rules 🎮\n\n1. Once the number of players left in the game becomes two, the game automatically ends and both players will be selected as the winners 🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out or else you get eliminated ⌛\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down ⏲️ before moving to the next question 📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose 💰</i></b>"
        return rule
    else:
        rule = f"🎮 Rules 🎮\n\n1. Once the number of players left in the game becomes three, the game automatically ends. The last three players will be selected as the winners. 🥇🥇🥇\n\n\
2. You have 30 seconds ⏳ to provide an answer for each question. Answer before your time runs out, or else you get eliminated. ⌛❌\n\n\
3. Once you've selected an answer, you will have to wait until the timer counts down before moving to the next question. ⏲️📋\n\n\
\n\n\n<b><i>Note: You still get paid even though you lose. 💰👍</i></b>"
        return rule

def elimination_construct_amount_to_be_paid(number_of_players,winner=False,no_winner=True): 
    total_money = float(variables.STRUCTURE_PRICE * float(number_of_players)) # this is the total money to be shared between all the players
    if no_winner == True: # This block of code will run if the no_winner argument value remains the same 
        print("1st block of code run that contains variables.structure_price")
        return variables.STRUCTURE_PRICE # The variable.STRUCTURE_PRICE is a constant in the variables python external file
        # That keeps how much a user brings to the table in a particular game and it is based on the variables.STRUCTURE_PRICE
        # that each user gets what he is going home with at the end of the game
    else: # this block of code will run if the no_winer argument is given another value appart from True
        if winner == True: # when the winner parameter is set to true this block of code will run and then return the winner price
            if number_of_players == 2:
                price = float((70/100)*total_money)
                print("2nd block of code ran that contains 70/100")
                return price
            elif number_of_players == 3:
                print("third block of code ran that contains 50/100 for winner == true")
                price = float((65/100)*total_money)
                return price
            else:
                price = float((60/100)*total_money)
                return price
        else:
            if number_of_players == 2:
                print("block of code that contains 30/100 ran")
                remaining_money = float((30/100)*total_money)
                return remaining_money
            elif number_of_players == 3:
                print("block of code that contains 50/100 which is the second 50/100 in occurrance ran")
                remaining_money = float((35/100)*total_money)/float(number_of_players-1) # this variable stores the remaining amount of money to be distributed to the remaining users of the game that are not winners
                # in the above variable since the winner takes
                return remaining_money
            else:
                remaining_money = float((40/100)*total_money)/float(number_of_players-1) # it is minus one because we are only calculating the money to pay to the other players not the winner
                return remaining_money

async def referrals_function(user_id,bot): # this function will take care of everything referral in the bot
    try:
        """this function will check to see if the total number of games played by an unverified referals is equal to five
        and then increment the referals referrer total verified referrals to 1 and then credits his account for the successful
        referral"""
        usr = user.User(user_id) # Instantiates the class
        if usr.evaluate_user_status:
            if usr.verifed: # this block of code will run if the user is already a verified user of the bot
                pass
            else:
                if usr.get_games_played() == 5: # this code runs once in a life time when the user has played up to 5 times then this code will run and then do all the necessary referral stuffs
                    ref_id = usr.referby
                    usr.update_ref_referrals(ref_id)
                    client = await bot.get_chat(user_id)
                    ref_link = await get_start_link(str(ref_id), encode=True)
                    full_name = client.first_name + " " + client.last_name if client.last_name else client.first_name
                    await bot.send_message(ref_id,f"🌟 {full_name} has been verified and you've recieved 💵{variables.per_refer}.\n\
    💥 Keep referring and earn much more!\n\
    {ref_link}")
                    menu_keyboard = menu(str(user_id))
                    await bot.send_message(str(user_id), "🏡",reply_markup=menu_keyboard,protect_content=True)         
                else: # if the number of games the user has played is less than 5 or more than 5 then this block of code will run and then nothing will happen becuase it just passes
                    pass # Nothing happens
        else:
            pass # i will work on this block of code later
    except Exception as e:
        await error_handler("Referrals function in the function module",e,bot)

def return_available_games():
    triviagames = KeyboardButton("🎯 Trivia games 🎯")
    cancelbutton = KeyboardButton('❌cancel')
    available_games_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    available_games_keyboard.row(triviagames,cancelbutton)
    return available_games_keyboard

def encode_message_py(plaindigits):
    digitreciprocals = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i',9:'j'}
    encrypted = ""
    for i in str(plaindigits):
        encrypted +=  digitreciprocals[int(i)]
    
    return encrypted

# Manual decode message in Python
def decode_message_py(encoded_message):
    alphabetreciprocal = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
    decoded = ''
    for char in encoded_message.lower():
        decoded += str(alphabetreciprocal[char])  # construct the decode
    return decoded

# this function will be responsible for evaluating the parameters passed to the bot link to know what it is either
# it is the referral id parameter or it is a game key parameter
def eval_parameter(parameter):
    try:
        message = str(decode_payload(parameter))
        return message
    except:
        return None # if there is any error then this block of code will run making the function to return none
    # which will not change anything because if the block of code in the try block did not run that means it is not
    # a referral id that is the parameter given to the bot but a game code then if it is a game code that means 
    # a none value can be returned and nothing will go wrong because when the user class is constructed the default
    # value for a referrer is none

async def send_dictionary(bot):
    try:
        data = {} #This is the dictionary where all the json information will be loaded to
        with open(variables.data_file_address,'r') as f:
            data = json.loads(f.read())
        data_json = json.dumps(data, indent=4)
        file = open("json.txt", "w")
        file.write(str(data_json))
        file.close()  
        with open("json.txt","rb") as f:
            await bot.send_document(variables.ERROR_ADMIN,document=f)
        await bot.send_message(variables.ERROR_ADMIN, "😔🙏 Sorry, I'm sending you the JSON file in text format. I'm really sorry. 📄📩")
    except Exception as e:
        await bot.send_message(variables.ERROR_ADMIN,f"This error message is comming from the send_dictionary function\nError: {e}")


async def error_handler(codeblock,error,bot,user_id=None):
    if None:
        pass
    else:
        await bot.send_message(variables.ERROR_ADMIN,f"Error generated from: {codeblock}\n\nError: {error}\n\nCaused by: {user_id}",protect_content=True)

