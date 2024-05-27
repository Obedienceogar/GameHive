from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# This file contains all the variables that contain the text the bot is going to send to the user

start_message = "🎮 Welcome to Gamexchange! 🤖\
Ready to level up your gaming experience and earn real rewards? Get ready to embark on an exciting gaming\
adventure where skill meets opportunity.\
🕹️ Play, compete, and win cash prizes! 💰\
Let's make gaming pay off! 🚀 #GameOn\n<i>\n\
Note: by clicking yes you \
agree to the bot's terms and conditions</i>"# This is the start message that will be sent by
# The bot the first time a user starts the bot

help_message = '''
<b>📚Help:</b> Click the "📚Help" button to get a quick overview of what each button does in the bot. It provides explanations for all available buttons, making it easy to navigate and use the bot effectively.\n\n\
<b>💸Withdraw:</b> The "💸Withdraw" button allows you to withdraw funds from your account balance. When you tap this button, you can follow the prompts to initiate a withdrawal transaction. It's a convenient way to access your earnings.\n\n\
<b>🎮Play Games</b>: If you're looking for some fun and entertainment, click the "🎮Play Games" button. You can play games in the bot alongside other users, compete, and win exciting prizes. It's a great way to challenge your skills and enjoy your time in the bot's community.\n\n\
<b>💼Account:</b> Access your account details by clicking the "💼Account" button. Here, you can view your account balance, referral link, the number of valid and invalid referrals, the number of games played, and your Telegram username. Stay informed about your bot-related activities.\n\n\
<b>👥Referrals:</b> Tap the "👥Referrals" button to check your referral-related information. This includes your referral link and the counts of valid and invalid referrals you've made. It's a helpful feature for tracking your referral program success.\n\n\
<b>📊Statistics:</b> Get insights into the bot's performance by clicking the "📊Statistics" button. You can find information about the total number of bot users, the total number of active users, and recent activity updates. Stay updated on the bot's community growth.\n\n\
<b>🤖Support:</b> If you have any questions, concerns, or need assistance with anything related to the bot, click the "🤖Support" button. The bot's friendly support team is here to help you promptly. Don't hesitate to reach out whenever you need assistance or guidance.\n\n\
<b>💰Balance:</b> Access your account details by clicking the "💰Balance" button. Here, you can view your account balance, referral link, the number of valid and invalid referrals, the number of games played, and your Telegram username. Stay informed about your bot-related activities.\n\n\n\
These buttons are designed to enhance your bot experience and provide you with a variety of options to navigate, manage your account, enjoy games, and seek assistance. Feel free to explore them and make the most of your time in our bot's community! 🚀🤖🎉
'''
API_ENDPOINT_FOR_PROXY = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

contvar = False #This variable is responsible for helping the waiting room to call the start game method once the right conditions have been fufilled 

elim_contvar = False # This variable is responsible for helping the elimwaiting room to call the startt game method once the right conditions have been fufilled

pause = False # This variable helps pause entry to the waiting room once the time left is small to avoid clashes 

elim_pause = False # This variable helps pause entry to the elimwaitingroom

sleep_time_for_pause = None # this is the time the user has to wait before entring the waiting room

elim_sleep_time_for_pause = None # this is the time the user has to wait before entering the waiting room

categories = [
    "General Knowledge",
    "Entertainment: Books",
    "Entertainment: Film",
    "Entertainment: Music",
    "Entertainment: Musicals & Theatres",
    "Entertainment: Television",
    "Entertainment: Video Games",
    "Entertainment: Board Games",
    "Science & Nature",
    "Science: Computers",
    "Science: Gadgets",
    "Science: Mathematics",
    "Mythology",
    "Sports",
    "Geography",
    "History",
    "Politics",
    "Art",
    "Celebrities",
    "Animals",
    "Vehicles",
    "Entertainment: Comics",
] # Categories for open trivia db

trivia_difficulty = ["easy","medium","hard"] # Open trivia difficulty level

one = InlineKeyboardButton(text="1",callback_data='choice:one')
two = InlineKeyboardButton(text="2",callback_data="choice:two")
three = InlineKeyboardButton(text="3",callback_data="choice:three")
four = InlineKeyboardButton(text="4",callback_data="choice:four")
five = InlineKeyboardButton(text="5",callback_data="choice:five")

choice_button = InlineKeyboardMarkup().add(one,two,three,four,five)

one = InlineKeyboardButton(text="1",callback_data='choiceelim:one')
two = InlineKeyboardButton(text="2",callback_data="choiceelim:two")
three = InlineKeyboardButton(text="3",callback_data="choiceelim:three")
four = InlineKeyboardButton(text="4",callback_data="choiceelim:four")
five = InlineKeyboardButton(text="5",callback_data="choiceelim:five")

elim_choice_button = InlineKeyboardMarkup().add(one,two,three,four,five)

user_gaming_room = {} # This will store the paricular gaming room a user is in and it will use the user's id as a key while the gaming room
# as it's value

gaming_room = {} # This is whwere all instances of a new gaming class which is created is stored

knockout_trivia_game_rule = ("\t\t\t\tRules 🌟\n\n1.\tEach player 🎲 gets the same question in the game and has to answer \
📝 their question to move on to the next round\n\n\
2.\tAny player who answers incorrectly gets eliminated from the game ❌🚫\n\n\
3.\tAll players 🏆 who participated in the game eventually get rewarded 🎁\n\n\
4.\tThe last player standing after all others have been eliminated automatically wins the game 🏆🥇e\n\n\
5.\tThe second-to-last and last players to be eliminated sometimes receive rewards after the game ends 🎁🥈🥉\n\n\
6.\tRewards are calculated 🧮 based on the number of players who joined the game 🎲")

quickfire_trivia_game_rule = ("\t\t\t\tRules 🌟\n\n1.\tEach player 🎲 gets the same question in the game and has to answer \
📝 their question to move on to the next round\n\n\
2.\tAny player who answers incorrectly 🚫 gets dropped out of the round, while other players 🔄 continue\n\n\
3.\tEach player 🎉 gets rewarded 💰 after each successful round!\n\n\
")

vote = {} # This dictionary will keep track of people that have voted

elim_vote = {}

not_enough_questions = 60 # this variable will help in handling the response_code 1. Each time the api request returns response_code 1 the api call will be made again but this time
# With a lesser amount of questions to be retrieved, this will be achieved by minusing 5 from this variable per unsuccessful api request with the api response _code 1

users_answered = {} # This will keep track of people that have answered a question

elim_users_answered = {}

data_file_address = "D:\Gamexchange\Gameexchange\data.json" # This is the file location of the data.json file

per_refer = float(0.02) # This is the amount of money that will be given to a user once his referral successfully verifies his account

STRUCTURE_PRICE = float(0.005) # This amount will be used by a function in the functions python file to construct the amount to be paid to a user

per_round = float(0.0005) # this is the amount that a user will be paid per round in the trivia game mode not in the elimination trivia game mood

game_code = {} # This variable will be responsible for storing all the keys generated for each users that wants to play a game
# this key will be used by the bot to check if the user actually visited the website or not

admin_send_message = None # this variable will store the messagae the admin want's to send to the user

ADMINS = ("1376299836","6088118370") # This tuple will store the list of the admins of the bot

ERROR_ADMIN = ADMINS[0] # This is the admin that will be incharge of handling error messages generated from the bot and also storing user data's

SUPPORT_ADMIN = ADMINS[1] # This is the admin that will be incharge of handling support ticket's from users

error_message = (
    "❌ Oops! Something went wrong. We apologize for the inconvenience.\n\n"
    "🤖 If this issue persists, please tap the support button below or contact our admins.\n\n"
)
emojis = ['🎮', '🕹️', '👾', '🎲', '🃏', '🎯', '🎳','🎰', '🏓', '🎮']



