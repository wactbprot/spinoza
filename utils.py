import re
import json

def list_to_markdown(lst):
    return "\n{}".format("\n".join( ["* {}".format(i) for i in lst]))

def kv_to_markdown(key, value):
    if value is None:
        return "No value behind key"

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
    txt = """Im the bot @spinoza. I interact with the redis server at: **{host}**.
    \n* If I should follow another server command:  **follow server** e.g. @spinoza follow i75464
    \n* I'll *observe* or *watch* redis keys periodically if you command: **observe key** e.g. @spinoza observe info@0 or  @spinoza watch raw_result@2
    \n* To list all the keys available use: **all** or **list** e.g. @spinoza list or @spinoza all
    \n* *Get* or *show* the value behind the key by : **get** or **show** e.g. @spinoza show raw_result@2 or @spinoza get info@0
    \n* Try @spinoza who
    """.format(host=kv.host)
    return txt

def help_life():
    txt = """
    **Baruch Spinoza** (/bəˈruːk spɪˈnoʊzə/; Dutch: [baːˈrux spɪˈnoːzaː]; born
    Benedito de Espinosa, Portuguese: [bɨnɨˈðitu ðɨ ʃpiˈnɔzɐ]; 24 November **1632**
    – 21 February **1677**, later Benedict de Spinoza) was a **Jewish-Dutch philosopher**
    of Portuguese Sephardi origin. By laying the groundwork for
    the Enlightenment and modern biblical criticism, including modern
    conceptions of the self and the universe, he came to be considered one
    of the great **rationalists** of 17th-century philosophy. Along with René
    Descartes, Spinoza was a leading philosophical figure of the Dutch Golden
    Age. Spinoza's given name, which means 'Blessed', varies among different
    languages. In Hebrew, it is written ברוך שפינוזה‬. His Portuguese name is
    Benedito 'Bento' de Espinosa or d'Espinosa. In his Latin works, he used
    Latin: Benedictus de Spinoza. (--https://en.wikipedia.org/wiki/Baruch_Spinoza)
    """

    return txt