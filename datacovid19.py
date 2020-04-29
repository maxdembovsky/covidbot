import telebot as tl
from telebot import types
from stats import *
import datetime

# Constants
TOKEN = '1161315344:AAER0gFZNqg0WUcPGebgj3jCB7Zo6-wV5eY'
bot = tl.TeleBot(TOKEN)
date_now = str(datetime.datetime.today())[0:10]


@bot.message_handler(commands=['start'])
def welcome(message):
    """Welcome new customer. Create keyboard buttons."""

    sticker = open('AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    left_button = types.KeyboardButton('Find out world statistics')
    right_button = types.KeyboardButton('Find out statistics for all countries')
    markup.add(left_button, right_button)

    bot.send_message(message.chat.id,
                     "Welcome, {}!".format(message.from_user.first_name) +
                     "\n"
                     "I'll help you find out information about COVID-19."
                     "\n\n"
                     "Enter the country you are interested in."
                     "\n"
                     "For example, Russia.",
                     parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """Processing messages entered from the keyboard or using keyboard buttons."""

    if message.chat.type == 'private':
        if message.text == 'Find out world statistics':

            date, confirmed, deaths, recovered = world_stat()

            total_confirmed = confirmed[-1]
            total_deaths = deaths[-1]
            total_recovered = recovered[-1]

            confirmed_dynamics = confirmed[-1] - confirmed[-2]
            deaths_dynamics = deaths[-1] - deaths[-2]
            recovered_dynamics = recovered[-1] - recovered[-2]

            image_world = open('world_plot.png', 'rb')
            bot.send_photo(message.chat.id, photo=image_world)

            markup = types.InlineKeyboardMarkup(row_width=2)
            log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale world')
            dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics world')
            markup.add(log_scale, dynamics)

            bot.send_message(message.chat.id,
                             'Statistics the spread of the virus on {} '.format(date_now) + 'in the world.'
                             '\n\n'
                             'Confirmed: {} '.format(total_confirmed) + '(+{})'.format(confirmed_dynamics) +
                             '\n\n'
                             'Deaths: {} '.format(total_deaths) + '(+{})'.format(deaths_dynamics) +
                             '\n\n'
                             'Recovered: {} '.format(total_recovered) + '(+{})'.format(recovered_dynamics) +
                             '\n\n'
                             'You can also view the distribution statistics in a logarithmic scale and '
                             'find out the distribution dynamics of morbidity during the day.',
                             parse_mode='html',
                             reply_markup=markup)

            world_log_scale()
            world_dynamics()

        elif message.text == 'Find out statistics for all countries':  # TODO: do top 20 countries
            stats_for_all_countries()
            text = str()
            with open('info_countries', 'r') as f:
                for line in f:
                    text += line + '\n'
            bot.send_message(message.chat.id, 'Stats for all countries on {}:\n\n'.format(date_now) + text,
                             parse_mode='html')

            f.close()

        elif message.text:
            try:
                country = message.text  # TODO: большой вопрос, что делать если страна введена разными буквами

                date, confirmed, deaths, recovered = country_stat(country)

                total_confirmed = confirmed[-1]
                total_deaths = deaths[-1]
                total_recovered = recovered[-1]

                confirmed_dynamics = confirmed[-1] - confirmed[-2]
                deaths_dynamics = deaths[-1] - deaths[-2]
                recovered_dynamics = recovered[-1] - recovered[-2]

                show_country_stat(country)
                image_country = open('country_plot.png', 'rb')
                bot.send_photo(message.chat.id, photo=image_country)

                markup = types.InlineKeyboardMarkup(row_width=2)
                log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale country')
                dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics country')
                markup.add(log_scale, dynamics)

                bot.send_message(message.chat.id,
                                 'Statistics the spread of the virus on {} '.format(date_now) + 'in {}.'.format(country)
                                 + '\n\n'
                                 'Confirmed: {} '.format(total_confirmed) + '(+{})'.format(confirmed_dynamics) +
                                 '\n\n'
                                 'Deaths: {} '.format(total_deaths) + '(+{})'.format(deaths_dynamics) +
                                 '\n\n'
                                 'Recovered: {} '.format(total_recovered) + '(+{})'.format(recovered_dynamics) +
                                 '\n\n'
                                 'You can also view the distribution statistics in a logarithmic scale and '
                                 'find out the distribution dynamics of morbidity during the day.',
                                 parse_mode='html',
                                 reply_markup=markup)

                show_log_scale_country(country)
                show_dynamics_country(country)

            except Exception:
                bot.send_message(message.chat.id, 'This country is not in the database. Try again.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Processing messages entered from the inline keyboard"""

    if call.message:
        if call.data == 'log scale world':

            image_world_log = open('world_log.png', 'rb')
            bot.send_photo(call.message.chat.id, photo=image_world_log)

            markup = types.InlineKeyboardMarkup(row_width=2)
            log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale world')
            dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics world')
            markup.add(log_scale, dynamics)

            bot.send_message(call.message.chat.id,
                             'You can also view the distribution statistics in a logarithmic scale and '
                             'find out the distribution dynamics of morbidity during the day.',
                             parse_mode='html',
                             reply_markup=markup)

        elif call.data == 'dynamics world':

            image_world_dynamics = open('world_dynamics.png', 'rb')
            bot.send_photo(call.message.chat.id, photo=image_world_dynamics)

            markup = types.InlineKeyboardMarkup(row_width=2)
            log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale world')
            dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics world')
            markup.add(log_scale, dynamics)

            bot.send_message(call.message.chat.id,
                             'You can also view the distribution statistics in a logarithmic scale and '
                             'find out the distribution dynamics of morbidity during the day.',
                             parse_mode='html',
                             reply_markup=markup)

        elif call.data == 'log scale country':

            image_country_log = open('country_log.png', 'rb')
            bot.send_photo(call.message.chat.id, photo=image_country_log)

            markup = types.InlineKeyboardMarkup(row_width=2)
            log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale country')
            dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics country')
            markup.add(log_scale, dynamics)

            bot.send_message(call.message.chat.id,
                             'You can also view the distribution statistics in a logarithmic scale and '
                             'find out the distribution dynamics of morbidity during the day.',
                             parse_mode='html',
                             reply_markup=markup)

        elif call.data == 'dynamics country':

            image_country_dynamics = open('country_dynamics.png', 'rb')
            bot.send_photo(call.message.chat.id, photo=image_country_dynamics)

            markup = types.InlineKeyboardMarkup(row_width=2)
            log_scale = types.InlineKeyboardButton('Log scale', callback_data='log scale country')
            dynamics = types.InlineKeyboardButton('Dynamics', callback_data='dynamics country')
            markup.add(log_scale, dynamics)

            bot.send_message(call.message.chat.id,
                             'You can also view the distribution statistics in a logarithmic scale and '
                             'find out the distribution dynamics of morbidity during the day.',
                             parse_mode='html',
                             reply_markup=markup)


bot.polling(none_stop=True)
