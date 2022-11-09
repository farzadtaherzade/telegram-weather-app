from telegram.ext import *
import requests
from json import *
from decouple import config

base_url = 'https://api.weatherapi.com/v1'
TOKEN = config("TOKEN")
KEY = config("APIKEY")


def get_weather(city: str):
    http = requests.get(f'{base_url}/current.json?key={KEY}&q={city}&aqi=no')
    if http.status_code == 400:
        return 'Pls Enter A Valid City Name'

    response = loads(http.text)
    status = response['current']['condition']['text']
    icon = "☀" if status == 'Clear' else "☀" if status == 'sunny' \
        else "☁" if status == 'cloud' else "☁" if status == 'overcast' \
        else "🌧" if status == 'rain' else "⛅" if status == 'Partly cloudy' \
        else '❄' if status == 'snow' else ''

    return f"""
Country Name: {response['location']['country']}
City Name: {response['location']['name']}
Temp : {response['current']['temp_c']}
Weather Status: {icon} {status}
    """


def start_command(update, context):
    update.message.reply_text('Send a city to see weather status')


print('Starting up bot...')


def help_command(update, context):
    pass


def handel_response(text: str) -> str:
    status = get_weather(text)
    return status


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = handel_response(text)

    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused error: {context.error}")


if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    # dp.add_handler(CommandHandler('help', help_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Errors
    dp.add_error_handler(error)

    # Run Bot
    updater.start_polling(1.0)
    updater.idle()
