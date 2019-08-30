import re
import logging
from mmpy_bot.bot import Bot
import redis
from kv import KV
from mp import MP
import utils as utils

from mmpy_bot.bot import respond_to
from mmpy_bot.bot import listen_to

from mmpy_bot.scheduler import schedule


@listen_to('^\.ssi$')
def ssmp_info(message):
    message.reply(utils.json_to_markdown(mp.get_ssmp_info()))

@listen_to('^\.ssee$')
def ssmp_info(message):
    message.reply(utils.json_to_markdown(mp.get_ssmp_expansion_exchange()))

@listen_to('^\.ssem$')
def ssmp_meta(message):
    message.reply(utils.json_to_markdown(mp.get_ssmp_expansion_meta()))

@listen_to('^\.sses$')
def ssmp_state(message):
    message.reply(utils.json_to_markdown(mp.get_ssmp_expansion_state()))

@listen_to('^\.sp$')
def gn_pressure(message):
    message.reply(mp.get_gn_pressure())

@listen_to('^\.sv$')
def valve_state(message):
    message.reply(mp.get_valve_state())

@listen_to('^\.ss$')
def servo_state(message):
    message.reply(mp.get_servo_state())

@listen_to('^\.s\?$')
@listen_to('^\.sh$')
def help_me(message):
    message.reply(utils.help_text(kv))

@listen_to('^\.st$')
def observe_target_pressure(message): 
    message.reply("start observing key target_pressure")
    schedule.every(20).seconds.do(lambda: utils.reply(message, kv.eget('current_target_pressure@0')))

@listen_to('^\.si$')
def observe_info(message):
    message.reply("start observing key info")
    schedule.every(20).seconds.do(lambda: utils.reply(message, kv.eget('info@0')))

@listen_to('^\.sr$')
def observe_results(message):
    ks = kv.part_keys("raw_result")
    for k in ks:
        message.reply("start observing key {key}".format(key=k))
        schedule.every(20).seconds.do(lambda: utils.reply(message, kv.eget(k)))

@respond_to('help')
def help_me(message):
    message.reply(utils.help_text(kv))

@listen_to('^\.sw$')
@respond_to('who')
def help_who(message):
    message.reply(utils.help_life())

@respond_to('all')
@respond_to('list')
def all_keys(message):
    message.reply(utils.list_to_markdown(kv.all_keys()))

@respond_to('line ([0-9]{1,2})')
def all_keys(message, n=None):
    message.reply(utils.list_to_markdown(kv.line_keys(n)))
 
@respond_to('get (.*)')
@respond_to('show (.*)')
def show(message, key=None):
    if kv.ini_ok:
        value=kv.get(key)
        message.reply(utils.kv_to_markdown(key=key, value=value))
    else:
        message.reply(utils.text_follow(kv))

@respond_to('observe (.*)')
@respond_to('watch (.*)')
def watch_key(message, key):
    utils.reply(message, "start observing key {key}".format(key=key))
    schedule.every(20).seconds.do(lambda: utils.reply(message, kv.eget(key)))

@listen_to('^\.so$')
@respond_to('stop')
def cancel_jobs(message):
    schedule.clear()
    message.reply(utils.text_stop(kv))

if __name__ == "__main__":
    kv = KV()
    mp = MP()
    Bot().run()