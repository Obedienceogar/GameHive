# All libraries to be used in this program will be included below

import asyncio
import aiogram
import requests
import time
import json
import webbrowser
import random
import variables
import functions
import threading
import Waitingroom
from user import User
from aiogram import types
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import Optional
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Functions to be used in this program
async def menu(chat_id):
    menu_keyboard = functions.menu(str(chat_id))
    await bot.send_message(str(chat_id), "🏡",reply_markup=menu_keyboard,protect_content=True)


# All variables to be used in this program
yes_button = KeyboardButton('✅Yes')
no_button = KeyboardButton('❌No')
choicekeyboardbutton = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(yes_button,no_button)
bot = Bot(token="6666381112:AAGajJ-IhZvWrwkcaiEDVxaRxsqlUNF_iYw") # This initializes the bot
mem = MemoryStorage()
dp = Dispatcher(bot,storage=mem)
data_location = variables.data_file_address
# This is the location of the Json file
OWNER_ID = str(1376299836)
per_refer = 0.02

#This class will be used for the storage of information in the bot
class States(StatesGroup):
    elim_game = State()
    pass

waiting_room = Waitingroom.WaitingRoom(bot)
elim_waiting_room = Waitingroom.ElimWaitingRoom(bot)

@dp.message_handler(state='*',commands =['start','cancel','trivia_game','elim_trivia_game']) #This is a message handler that handles commands in the bot
async def commands(message: types.Message,state: FSMContext):
    user = User(message.chat.id,str(decode_payload(message.get_args()))) #This stores the user's id
    command = message.get_command() # This variable gets the command sent by the user's
    print(command)
    print(str(decode_payload(message.get_args())))
    global waiting_room
    user_status = user.check_user() # This calls the check_user function and it returns and int to signify the user status a 0 to mean the 
    # Telegram user has previously started the bot therefore a user. A 1 to signify that the telegram user has already started the bot and 
    # has started using the bot and a 2 to signify that the telegram user has been previously banned from the bot
    if command == "/start" and user_status == 2: # The User has been banned
        await message.answer("Apologies, but 🚫 your account is currently under ban. 😔",protect_content=True) # I will complete this part of
        # code later

        # But just so you know this part of the code will will deal with banned users and i made this block of code the first condition the 
        # Bot should look for because of the order of analyzation of conditions in python so my code runs the way i want it to

    elif command == "/start" and user_status == 1: # The user is an active user if the user_status has a value of 1 
        await message.answer("🎉 Welcome back, our highly esteemed user! 🙌 I've missed you so much.\n\
😊 There are some exciting games you can play and even win fantastic prizes.\n\
🎮🏆 So, please, feel free to dive right in and have a blast! 🎈🥳",protect_content=True)
        # I will write the remaining code here later 
        # But typically what the remaining code will do is to return the home menu of the bot to the user
        await menu(str(message.chat.id))
    elif command == "/start" and user_status == 0: # This means that the user has previously started the bot but has not become a full user of
        # Of the bot
        await message.answer("👋 Welcome back, user! 🌟 I've been eagerly anticipating your return.\n\
 😊 Are you all set to dive back into the world of the bot and join us fully? 🤖🚀",reply_markup=choicekeyboardbutton)

        # I will work on the remaining code later 
        # But basically what the remaining code will be doing is to guide the user to becomming an active user by introducing itself
        # And finally adding the user to the active_user list ot show that the user is now an active user of the bot since he has been 
        # Propery introduced to the bot
        # I hope what i'm saying makes sense to you if it dosen't just know that the difference between the active user and the normall user
        # Is that the active_user has been known the bot properly because the bot has completed the introductory proccess with it while
        # a user is one who did not complete the introductory process with the bot 
        # While the introductory process is the first few messages the bot sends tto the user when the user starts the bot for the first time
    else: # This block of code will only run if the user is a new user or if a different command was sent to the bot
        # So bassically this will introduce the user to the bot and add the user to the active user list
        referby = user.referby # this will grab the referrer id of a user
        if user_status == 1:
            pass
        else:
            await message.answer(variables.start_message,parse_mode="HTML",reply_markup=choicekeyboardbutton,protect_content=True)
            user.add_user(inactive_users=True)
            if referby == "":
                pass
            elif referby == str(message.chat.id):
                pass
            elif referby and user_status == 4:
                user.increment_referrers_referrals(str(referby))
                await bot.send_message(referby,f"🏧 Exciting news! A new referral has just joined the bot using your link.\n\
🤝 You'll receive {per_refer} USD once your 🏧 referral account is verified. 💸💼",protect_content=True)
    
    
    # This part of the code will handle other commands like the /trivia game command
    if command == "/triviaclash": # For now this is the only condition to be fullfiled before the trivia game starts
        print(f"Variables.pause vf value is {variables.pause}")
        if variables.pause == True: # This block of code will make any user that sends the /trivia game command while there are users in a waiting room
            # Whose time is less thatn 7 seconds to wait so they will be no obstructions
            await asyncio.sleep(7)
            print("Asyncio.sleep has finished running that is why you are seeing this message right now")
        else:
            pass
        if variables.contvar == False:
            variables.contvar = True
            msg = await bot.send_message(message.chat.id,"Creating gaming room") 
            if str(message.chat.id) in waiting_room.players_list:
                pass
            else:
                waiting_room.players_list.append(str(message.chat.id)) # Stringify the user's id and store it in the players list
                waiting_room.players_dict[str(message.chat.id)] = message.chat.full_name  
            await msg.edit_text("Game room created")
            await asyncio.sleep(2)
            waiting_room.message_ids[str(message.chat.id)] = msg.message_id # this will store the message id of the joining gaming room message sent to 
            # the user from the bot as the message will later be overwritten with the message of the waiting room
            await functions.start_game_function(waiting_room,message.chat.id)
        else:
            msg_user = await bot.send_message(message.chat.id,"Joining gaming room")
            if str(message.chat.id) in waiting_room.players_list:
                pass # this is to make sure that a user that is already in the waiting room can't enter the room again
            else:
                waiting_room.players_list.append(str(message.chat.id)) # Stringify the user's id and store it in the players list
                waiting_room.players_dict[str(message.chat.id)] = message.chat.full_name  
            await msg_user.edit_text("Joined")
            await asyncio.sleep(2)
            waiting_room.message_ids[str(message.chat.id)] = msg_user.message_id # this will store the message id of the joining gaming room message sent to 
            # the user from the bot as the message will later be overwritten with the message of the waiting room
    elif command == "/triviathon": # This block of code will run once the command /elim_trivia_game is sent to the bot
        if variables.elim_pause == True: # This block of code will make any user that sends the /trivia game command while there are users in a waiting room
            # Whose time is less thatn 2 seconds to wait so they will be no obstructions
            await asyncio.sleep(10)
        else:
            pass
        if variables.elim_contvar == False:
            variables.elim_contvar = True
            msg = await bot.send_message(message.chat.id,"Creating gaming room") 
            if str(message.chat.id) in elim_waiting_room.players_list:
                pass
            else:
                elim_waiting_room.players_list.append(str(message.chat.id)) # Stringify the user's id and store it in the players list
                elim_waiting_room.players_dict[str(message.chat.id)] = message.chat.full_name  
            await msg.edit_text("Game room created")
            await asyncio.sleep(2)
            elim_waiting_room.message_ids[str(message.chat.id)] = msg.message_id # this will store the message id of the joining gaming room message sent to 
            # the user from the bot as the message will later be overwritten with the message of the waiting room
            await functions.elim_start_game_function(elim_waiting_room,message.chat.id)
        else:
            msg_user = await bot.send_message(message.chat.id,"Joining gaming room")
            if str(message.chat.id) in elim_waiting_room.players_list:
                pass # this is to make sure that a user that is already in the waiting room can't enter the room again
            else:
                elim_waiting_room.players_list.append(str(message.chat.id)) # Stringify the user's id and store it in the players list
                elim_waiting_room.players_dict[str(message.chat.id)] = message.chat.full_name  
            await msg_user.edit_text("Joined")
            await asyncio.sleep(2)
            elim_waiting_room.message_ids[str(message.chat.id)] = msg_user.message_id # this will store the message id of the joining gaming room message sent to 
            # the user from the bot as the message will later be overwritten with the message of the waiting room
    if command == "/menu":
        await menu(message.chat.id) # This will return the home menu to any user that sends the /menu command
@dp.message_handler() #This is a message handler that handles all text sent to the bot by the user
async def kb_operations(message: types.Message):
    user = User(str(message.chat.id))
    user_status = user.check_user()
    if message.text == "✅Yes":
        # I know i did not really put a lot of code to work on users that have been banned but i will do that later as the bot grows
        if user_status == 2: # This block of code will run if the user is a banned user
            await message.answer("Apologies, but 🚫 your account is currently under ban. 😔",protect_content=True)
        elif user_status == 1: # this block of code will run if the user is an active user
            # I will just returnreturn the menu to the user
            await menu(str(message.chat.id))
        else: # This block of code will run if the user is an inactive user
            await message.answer("Great! 🚀 I'll be providing you with a detailed breakdown of the functions and purposes of every button within this bot. 🤖📚 Stay tuned for a comprehensive guide! 😊📝",protect_content=True)
            await asyncio.sleep(2)
            await message.answer(variables.help_message,parse_mode="HTML",protect_content=True)
            user.add_user(user=True)
            user.officiate_user() # when we officiate a user the user will now be known as an active user to the bot
            await menu(message.chat.id)                      
    
    elif message.text =="❌No":
        if user_status == 2: # This block of code will run if the user is a banned user
            await message.answer("Apologies, but 🚫 your account is currently under ban. 😔",protect_content=True)
        elif user_status == 1: # This block of code will run if the user is an active user
            # I will just return the menu to the user
            await menu(str(message.chat.id))
        else:
            yes_button = KeyboardButton("Yes✅")
            no_button = KeyboardButton("No❌")
            choicekeyboardbutton = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).row(yes_button,no_button)
            await message.answer("Would you like to stay in the loop and receive updates\
when we host giveaways for our users? 🎉🎁",reply_markup=choicekeyboardbutton,protect_content=True)

    elif message.text == "Yes✅":
        user.add_user(user=True,inactive_users=True) # This will use the add_user method to add the user's information to both the user's list and
        # the active_user list
        await message.answer("Would you like to stay in the loop and receive updates when we host giveaways for our users? 🎉🎁",protect_content=True)
        await message.answer("I'll be here waiting for you whenever you're ready to join our welcoming community. 🤗🌟",protect_content=True)
    elif message.text == "No❌":
        await message.answer("I'll be here waiting for you whenever you're ready to join our welcoming community. 🤗🌟",protect_content=True)

    elif message.text == "💼Account": # This gives the user a general overview of his account when this block of code is run
        if user_status == 1: # This block of code will only run if the user is an active user of the bot
            balance_user = user.balance # The currency the bot is working with is usd so the user's balance
            # should always be taken to be the total amount of usd the user has
            referrals = len(user.referrals)
            ref_link = await get_start_link(str(message.chat.id), encode=True)
            valid_referrals = len(user.valid_referral_list)
            games_played = user.games_played
            accmsg = f"👮<b>Your Account Details</b>\n\n\
🧮 <b>Account Balance:</b> {balance_user}\n\n\
👥 <b>Referral Link:</b> {ref_link}\n\n\
👫 <b>Valid Referrals:</b> {valid_referrals}\n\n\
🚫 <b>Invalid Referrals:</b> {referrals}\n\n\
🎮 <b>Games Played:</b> {games_played}\n\n\
👤 <b>Your Name:</b> {message.chat.full_name}\n\n\
<i>Thank you for being a part of our community! If you have any questions or need assistance, feel free to ask.</i>\
"
            await bot.send_message(message.chat.id,accmsg,parse_mode="HTML",protect_content=True)
            await menu(message.chat.id)
        else:
            await message.answer("⚡️ You are not a user! ⚡️\n\n🙋‍♂️ Please use the /start command to become one. 🤖",protect_content=True)
    elif message.text == "🎮Play Games": # This block of code will allow the user to play games in the bot
        await bot.send_message(message.chat.id,"",protect_content=True,reply_markup=functions.return_available_games())

    elif message.text == "Trivia Games":
        messg = "Available trivia games"
        triviathon = InlineKeyboardButton(text="Triviathon",callback_data='play_games_triviathon')
        triviaclash = InlineKeyboardButton(text="Trivaclash",callback_data="play_games_triviaclash")
        game_options_markup = InlineKeyboardMarkup().add(triviathon).add(triviaclash)
        await bot.send_message(message.chat.id,messg,protect_content=True,reply_markup=game_options_markup)

    elif message.text == "Triviathon":
        pass # I will do something in this  block of code later
    
    elif message.text == "Trivia clash":
        pass # I will do something to this block of code later
    
    elif message.text == "👥Referrals": # This block of code will allow the user to see his referral link and referrals stat
        if user_status == 1:
            user = User(str(message.chat.id))
            totalinvites = user.total_referrals()
            ref_link = await get_start_link(str(message.chat.id), encode=True)
            totalverifiedusers = len(user.valid_referral_list)
            ref_msg = f"🌟 <b>Your Referral Details</b>\n\n\
👥 <b>Referral Link:</b> {ref_link}\n\n\
👫 <b>Valid Referrals:</b> {totalverifiedusers}\n\n\
🚫 <b>Unverified Referrals:</b> {totalinvites}\n\n\
<i>Share your referral link with friends to earn more rewards and grow our community!</i>\
"
            await bot.send_message(message.chat.id,ref_msg,parse_mode="HTML",protect_content=False)
            await menu(message.chat.id)
        else:
            await message.answer("⚡️ You are not a user! ⚡️\n\n🙋‍♂️ Please use the /start command to become one. 🤖",protect_content=True)
    elif message.text == "📊Statistics": # This block of code will allow the user see the bot's statistics
        if str(message.chat.id) == OWNER_ID:
            total_bot_members = len(user.active_users)
            start_users = len(user.all_users) #This variable stores all the user id of the users that have started the bot
            active_users = len(user.active_users)
            start_msg = f"📊 Total members : {total_bot_members} Users\n\nTotal bot active users : {active_users}\n\n🥊\
Total Bot Users: {start_users}"
            await bot.send_message(message.chat.id, start_msg,protect_content=True)
            await menu(message.chat.id)
        elif user_status == 1:
            total_bot_members = len(user.all_users)
            games_played = user.get_games_played()
            active_users = len(user.active_users)
            start_msg = f"📊 <b>Bot Statistics</b>\n\n\
👥 <b>Total Bot Users:</b> {total_bot_members}\n\n\
🌟 <b>Total Active Users:</b> {active_users}\n\n\
💸 <b>Total Bot Withdrawals:</b>{user.total_withdrawals}\n\n\
<b>Total Games Played:</b>{games_played}\n\n\
📈 <b>Recent Activity:</b> User engagement is on the rise! 🚀\n\n\
<i>Thank you for being part of our growing community. Your participation makes a difference!</i>\
"# I'll add this one later when my bot's is now online 24/7 📅 <b>Weekly New Users:</b> 350\
            await bot.send_message(message.chat.id, start_msg,parse_mode="HTML",protect_content=True)
            await menu(message.chat.id)
        else:
            await message.answer("⚡️ You are not a user! ⚡️\n\n🙋‍♂️ Please use the /start command to become one.",protect_content=True)
    
    elif message.text == "💰Balance": # This block of code will allow the user to see his bot balance
        if user_status == 1:
            user_balance = user.balance
            balance_msg = f"🌐 <b>Bot Balance and Financial Summary</b>\n\n\
💰 <b>Your Current Bot Balance:</b> ${user_balance}\n\n\
📊 <b>Income Summary:</b>\n\n\
   - Total Earnings: ${user.total_earnings}\n\n\
   - Total Withdrawals: ${user.total_user_withdrawals}\n\n\
<i>Here is a detailed summary of the bot's finances. If you have any questions or need assistance with withdrawals or deposits, feel free to ask.</i>\
"
            await bot.send_message(message.chat.id, balance_msg,parse_mode="HTML",protect_content=True)
            await menu(str(message.chat.id))
        else:
            await message.answer("⚡️ You are a user! ⚡️\n\n🙋‍♂️ Please use the /start command to use the main menu.",protect_content=True)
    elif message.text == "💸Withdraw": # This block of code will allow the user to perform a withdrawal of his bot balance
        if user_status ==1:
            await message.answer("💸 Minimum withdrawal amount: $1 USD",protect_content=True)
            await menu(str(message.chat.id))
        else: 
            await message.answer("⚡️ You are a user! ⚡️\n\n🙋‍♂️ Please use the /start command to use the main menu.",protect_content=True)
    elif message.text == "🤖Support": # This block of code will allow the user contact the admin for support for any issues he is facing
        # in his bot
        # I will do something about this block of code later but for now is a pass
        await message.answer("Feel free to type in any questions or concerns you have about the bot, and I'll do my best to assist you! 🤖💬",parse_mode="HTML",protect_content=True)
    elif message.text == "📚Help": # This block of code will send a message that will guide the user through the bot
        await message.answer(variables.help_message,protect_content=True,parse_mode="HTML")  
#This block of code will be handling all the callback_queries from the inline keyboards
@dp.callback_query_handler() #This message handler handles all callback queries from the bot
async def ans_query(call: types.CallbackQuery):
    # Extract the custom callback data
    callback_data = call.data  
    print(f"This is the callback_data: {callback_data}")
    # Parse or process the custom data to determine the action
    action = callback_data.split(':')[1]  # Extracting the custom data
    # Call the corresponding function or perform the action
    if callback_data.startswith("choice"):
        try:
            if callback_data.startswith("choiceelim"):
                if variables.elim_vote[str(call.message.chat.id)] == True:
                    pass
                else:
                    if action == "one" and variables.elim_vote[call.message.chat.id] == False:
                        elim_waiting_room.vote.category_list[0] += " 🙋‍♂️"
                        variables.elim_vote[str(call.message.chat.id)] = True
                    elif action == "two" and variables.elim_vote[call.message.chat.id] == False:
                        elim_waiting_room.vote.category_list[1] += " 🙋‍♂️"
                        variables.elim_vote[str(call.message.chat.id)] = True
                    elif action == "three" and variables.elim_vote[call.message.chat.id] == False:
                        elim_waiting_room.vote.category_list[2] += " 🙋‍♂️"
                        variables.elim_vote[str(call.message.chat.id)] = True
                    elif action == "four" and variables.elim_vote[call.message.chat.id] == False:
                        elim_waiting_room.vote.category_list[3] += " 🙋‍♂️"
                        variables.elim_vote[str(call.message.chat.id)] = True
                    elif action == "five" and variables.elim_vote[call.message.chat.id] == False:
                        elim_waiting_room.vote.category_list[4] += " 🙋‍♂️"
                        variables.elim_vote[str(call.message.chat.id)] = True
                    else:
                        pass # This block of code will not even run
            elif callback_data.startswith("choice"):
                if variables.vote[str(call.message.chat.id)] == True:
                    pass
                else:
                    if action == "one" and variables.vote[call.message.chat.id] == False: # this will make sure a user does not vote more than one time
                        waiting_room.vote.category_list[0] += " 🙋‍♂️" # This will append a green roun sticker to the line of the option the user chooses to signify vote
                        variables.vote[str(call.message.chat.id)] = True
                        print(variables.vote[str(call.message.chat.id)])
                    elif action == "two" and variables.vote[call.message.chat.id] == False: # this will make sure a user does not vote more than one time
                        waiting_room.vote.category_list[1] += " 🙋‍♂️" # This will append a green roun sticker to the line of the option the user chooses to signify vote
                        variables.vote[str(call.message.chat.id)] = True
                    elif action == "three" and variables.vote[call.message.chat.id] == False: # this will make sure a user does not vote more than one time
                        waiting_room.vote.category_list[2] += " 🙋‍♂️" # This will append a green roun sticker to the line of the option the user chooses to signify vote
                        variables.vote[str(call.message.chat.id)] = True
                    elif action == "four" and variables.vote[call.message.chat.id] == False: # this will make sure a user does not vote more than one time
                        waiting_room.vote.category_list[3] += " 🙋‍♂️" # This will append a green roun sticker to the line of the option the user chooses to signify vote
                        variables.vote[str(call.message.chat.id)] = True
                    elif action == "five" and variables.vote[call.message.chat.id] == False: # this will make sure a user does not vote more than one time
                        waiting_room.vote.category_list[4] += " 🙋‍♂️" # This will append a green roun sticker to the line of the option the user chooses to signify vote
                        variables.vote[str(call.message.chat.id)] = True
                    else:
                        pass
            else: # more conditions can later be added here instead of the else block 
                pass
        except Exception as e:
            print(f"There was an error this is the error {e}")
    elif callback_data.startswith("Answer"):
        option = callback_data.split(':')[1]
        game_room = variables.user_gaming_room[str(call.message.chat.id)]
        game = variables.gaming_room[game_room]
        check_if_users_answered_is_empty = variables.users_answered[str(call.message.chat.id)] # this is going to check if the dictionary that stores a boolean value signifying if a user has answered has not is empty,
        if check_if_users_answered_is_empty == None:
            variables.users_answered[str(call.message.chat.id)] = False # Flag to make sure once a user answer a question he can't give another answer again
        else:
            pass
        if variables.users_answered.get(str(call.message.chat.id),False) == False:
            print(f"This is the option picked: {option.lower}\nAnd this is the game answer{game.normal_option_and_answer['correct_answer'].lower()}")
            print(f"Game correct answer {game.normal_option_and_answer['correct_answer']}")
            if option.lower() == game.normal_option_and_answer['correct_answer'].lower():
                await game.highlight_users_option(option,call.message.chat.id) # This method is responsible for making the user's selection visible to the user
                variables.users_answered[str(call.message.chat.id)] = True
            else:
                await game.highlight_users_option(option,call.message.chat.id) # This method is responsible for making the user's selection visible to the user
                variables.users_answered[str(call.message.chat.id)] = True
    elif callback_data.startswith("answerelim"): # this call back data will handle callback request from the elimination trivia game inline keyboard queriy
        # answwerelim callback data will start with small letter a so that it will be different from the Answer callback data so as to make sure the Answer callback data dosen't run even when the answerelim callback data is the one that is suppose to run because of the startswith function
        option = callback_data.split(':')[1]
        game_room = variables.user_gaming_room[str(call.message.chat.id)]
        game = variables.gaming_room[game_room]
        check_if_elim_users_answered_is_empty = variables.elim_users_answered[str(call.message.chat.id)] # this is going to check if the dictionary that stores a boolean value signifying if a user has answered has not is empty,
        # if it is then it returns none to the variable then below a conditional statement is then used to give a value to the elim_users_answered dictionary for the user if there is no value
        if check_if_elim_users_answered_is_empty == None:
            variables.elim_users_answered[str(call.message.chat.id)] = False # Flag to make sure once a user answer a question he can't give another answer again
        else:
            pass
        if variables.elim_users_answered.get(str(call.message.chat.id),False) == False:
            print(f"This is the option picked: {option.lower}\nAnd this is the game answer{game.normal_option_and_answer['correct_answer'].lower()}")
            print(f"Game correct answer {game.normal_option_and_answer['correct_answer']}")
            if option.lower() == game.normal_option_and_answer['correct_answer'].lower():
                await game.highlight_users_option(option,call.message.chat.id) # This method is responsible for making the user's selection visible to the user
                variables.elim_users_answered[str(call.message.chat.id)] = True
            else:
                await game.highlight_users_option(option,call.message.chat.id) # This method is responsible for making the user's selection visible to the user
                variables.elim_users_answered[str(call.message.chat.id)] = True


async def main(): 
    # I will write add a function here that will retrieve data from my database where i store all the 
    # my users information   
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())