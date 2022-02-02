import telebot
import sqlite3
import random
conn = sqlite3.connect('base.db', check_same_thread=False)
curs = conn.cursor()
curs.execute('create table if not exists dudes(id INT, message_id INT)')
curs.execute('create table if not exists mesgs(id INT, message TEXT)')
conn.commit()

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANKYbMQ9i1fON8FMtefQsftOcdRbI4AAhgAAygPahTUuHPWOzYDSSME')
    bot.send_message(message.chat.id, 'Если вас ещё не нашёл Тайный Санта или вы не знаете, как выглядит ваш подопечный, можете оставить или забрать свой подарок на баре 🎅')

@bot.message_handler(commands=['start_game'])
def start_game_handler(message):
    if message.chat.id==307518206:
        l = curs.execute('select * from dudes').fetchall()
        random.shuffle(l)
        le = len(l)
        for i in range(le):
            bot.copy_message(l[i][0],l[(i+1)%le][0],l[(i+1)%le][1])

@bot.message_handler(commands=['send_me_all'])
def all_handler(message):
    if message.chat.id==307518206:
        pass # Function for debugging
        
@bot.message_handler(content_types=['text','audio','document','photo','sticker','video','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message'])
def any_handler(message):
    curs.execute(f'delete from dudes where id={message.chat.id}')
    curs.execute(f'insert into dudes values({message.chat.id},{message.id})')
    conn.commit()
    bot.send_message(message.chat.id, 'Ок, теперь жди второго этапа, когда я разошлю всем по сообщению, и каждый для кого-то станет тайным сантой.')

bot.polling(none_stop=True)
