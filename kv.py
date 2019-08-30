import logging
import redis
logging.basicConfig(level=logging.DEBUG)

class KV:
    def __init__(self):
        self.host = "localhost"
        self.port = 6379
        self.db = 0
        self.old = {}
        self.ini_ok = False
        self.init()
        logging.info('initialization complete') 

    def init(self):
        self.srv = redis.StrictRedis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        self.ini_ok = True
        logging.info('made server') 

    def all_keys(self):
        if self.ini_ok:
            return self.srv.keys("*")
        else:
            return None

    def part_keys(self, part):
        if self.ini_ok:
            return self.srv.keys("{part}*".format(part=part))
        else:
            return None

    def line_keys(self, n):
        if self.ini_ok:
            return self.srv.keys("*@{n}".format(n=n))
        else:
            return None
            
    def eget(self, k):
        """Returns a tupel with (key, value, changed)
        """
        v = self.get(k)
        if k in self.old:
            if self.old[k] == v:
                changed = False
            else:
                self.old[k] = v    
                changed =  True
                logging.info('value of key {} changed'.format(k)) 
        else:
            self.old[k] = v
            changed =  True
            logging.info('new value of key {}'.format(k)) 

        return k, v, changed

    
    def get(self, k):
        return  self.srv.get(k)

if __name__ == "__main__":
    kv = KV()
    ks = kv.part_keys("raw_result")
    for k in ks:
        print(k)