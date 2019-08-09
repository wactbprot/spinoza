import re
import json

def list_to_markdown(lst):
    return "\n{}".format("\n".join( ["* {}".format(i) for i in lst]))

def kv_to_markdown(key, value):
    if value is None:
        return "No value for key {k}".format(k=key)

    pat = "^([{\[].*?[}\]])$"
    m = re.search(pat, value)
    if m:
        value = json.dumps(json.loads(m.group(1)), sort_keys=True, indent=4, separators=(',', ': '))
        value = "```json\n{value}\n```".format(value=value)

    return 'The value of key **{key}** is:\n {value}'.format(key = key, value=value)

def reply(message, kvc):
    key, value, changed = kvc
    if changed:
        content = kv_to_markdown(key=key, value=value)
        message.reply(content)

def help_text(kv):
    return open("help.md").read()

def help_life():
    return open("who.md").read()

def text_stop(kv):
    return "stop all watching"