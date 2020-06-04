import telebot

import settings
import questions_api


bot = telebot.TeleBot(settings.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(
		message.chat.id,
		"Я могу подобрать кафедральные материалы по вашему вопросу. Что вас интересует?"
	)

@bot.message_handler(content_types=['text'])
def handle_question(message):
	chat_id = message.chat.id

	try:
		user = message.from_user
		q_user = questions_api.login(user.username, f'{user.first_name} {user.last_name}')
		question = questions_api.send_question(q_user['id'], message.text)
		
		bot.send_message(chat_id, "Ищу материалы...")
		resources = questions_api.get_resources(question['id'])
		bot.send_message(chat_id, str(resources))


	except Exception as e:
		print(e)
		bot.send_message(
			chat_id,
			"Не удалось обработать запрос, попробуйте еще раз."
		)

def send_resources(chat_id, resources):
	pass

if __name__ == '__main__':
	print('run...')
	bot.polling()