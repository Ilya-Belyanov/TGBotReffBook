import bot

if __name__ == "__main__":
    bot.executor.start_polling(bot.dispatcher, skip_updates=True)
