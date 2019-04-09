import re
import logging
from mmpy_bot.bot import Bot
import redis
from kv import KV
import utils as utils
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
from mmpy_bot.scheduler import schedule

@respond_to('help', re.IGNORECASE)
def help_me(message):
    message.reply(utils.help_text(kv))

@respond_to('who', re.IGNORECASE)
def help_who(message):
    message.reply(utils.help_life())

@respond_to('all', re.IGNORECASE)
@respond_to('list', re.IGNORECASE)
def all_keys(message):
    message.reply(utils.list_to_markdown(kv.all_keys()))

@respond_to('line ([0-9]{1,2})', re.IGNORECASE)
def all_keys(message, n=None):
    message.reply(utils.list_to_markdown(kv.line_keys(n)))

@respond_to('follow (.*)', re.IGNORECASE)
def follow(message, host=None):
    kv.host = host
    kv.init()
    message.reply(utils.text_host(kv))
   
@respond_to('get (.*)', re.IGNORECASE)
@respond_to('show (.*)', re.IGNORECASE)
def show(message, key=None):
    if kv.ini_ok:
        value=kv.get(key)
        message.reply(utils.kv_to_markdown(key=key, value=value))
    else:
        message.reply(utils.text_follow(kv))
           
@respond_to('observe (.*)', re.IGNORECASE)
@respond_to('watch (.*)', re.IGNORECASE)
def watch_key(message, key):
    schedule.every(20).seconds.do(lambda: utils.reply(message, kv.eget(key)))

@respond_to('stop', re.IGNORECASE)
def cancel_jobs(message):
    schedule.clear()
    message.reply(utils.text_stop(kv))

if __name__ == "__main__":
    kv = KV()
    Bot().run()