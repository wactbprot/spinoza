import logging
import redis
logging.basicConfig(level=logging.DEBUG)

class KV:
    def __init__(self):
        self.host = "localhost"
        self.port = 6379
        self.db = 0
        self.old = {}
        self.init()
        logging.info('initialization complete') 

    def init(self):
        logging.info('make server') 
        self.srv = redis.StrictRedis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        self.ini_ok = True

    def pubsub(self):
        logging.info('make pubsub') 
        self.pubsub = self.srv.pubsub()

    def subs(self, channel='io'):
        self.pubsub.subscribe(channel)

    def all_keys(self):
        return self.srv.keys("*")
    
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
        

        