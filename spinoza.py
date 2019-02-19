from mmpy_bot.bot import Bot
import redis
import re
from kv import KV
import utils as utils
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
from mmpy_bot.scheduler import schedule


@listen_to('bots?')
def help_me(message):
    
    message.reply('Im @spinoza, I observe and interact with the redis server at: {host}'.format(host = kv.host))
    message.reply('If I should follow another server command me *follow server* (e.g. `@spinoza follow i75464)`.' )

@respond_to('follow (.*)', re.IGNORECASE)
def follow(message, server=None):
    message.reply('Ok, try to connect to server *{}* and follow'.format(server))
    kv.host = server
    kv.init()
    message.reply("Connected to server.")
    md_keys = utils.list_to_markdown(kv.all_keys()) 
    message.reply("""Available keys are (Ask for the value of a 
                    `particular_key` by commanding `@spinoza show particular_key` 
                    or observe a key every N(=20) seconds by 
                    `@spinoza observe particular_key 20`): {keys}""".format(keys=md_keys))

@respond_to('get (.*)', re.IGNORECASE)
@respond_to('show (.*)', re.IGNORECASE)
def show(message, key=None):
    if kv.ini_ok:
        value=kv.get(key)
        message.reply(utils.kv_to_markdown(key=key, value=value))
    else:
        message.reply("Please start with the *follow server_name* command")
           
@respond_to('observe (.*) (.*)', re.IGNORECASE)
@respond_to('whatch (.*) (.*)', re.IGNORECASE)
def whatch_key(message, key, dt=10):
    value=kv.get(key)
    schedule.every(int(dt)).seconds.do(message.reply, utils.kv_to_markdown(key=key, value=value))




@respond_to('stop', re.IGNORECASE)
def cancel_jobs(message):
    schedule.clear()
    message.reply('all jobs canceled.')

if __name__ == "__main__":
    kv = KV()

    Bot().run()