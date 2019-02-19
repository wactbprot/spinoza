 
def list_to_markdown(lst):#
    return "\n{}".format("\n".join( ["* {}".format(i) for i in lst]))

def kv_to_markdown(key, value):
    return 'The value of key *{key}* is {value}'.format(key = key, value=value)