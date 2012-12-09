'''
Created on 7 Dec 2012

@author: Jamie
'''
# Contents of configuration file: tweeter.cfg
#
# [DEFAULT]
# consumer_key = *********************
# consumer_secret = *******************************************
# access_token_key = **************************************************
# access_token_secret = ******************************************

import twitter
import ConfigParser
import logging

class tweeter:
    
    __client = None
    
    def __init__(self, __configFile = "tweeter.cfg"):
        
        __config = ConfigParser.RawConfigParser()
        logging.basicConfig(filename='tweeter.log',level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        
        try:
            __config.readfp(open(__configFile))
        except IOError as e:
            logging.debug("I/O Error ({0}): ({1})".format(e.errno, e.strerror))
            return
        try:
            __consumerKey = __config.get('DEFAULT', 'consumer_key')
            __consumerSecret = __config.get('DEFAULT', 'consumer_secret')
            __accessTokenKey = __config.get('DEFAULT', 'access_token_key')
            __accessTokenSecret = __config.get('DEFAULT', 'access_token_secret')
        except ConfigParser.NoSectionError as e:
            logging.debug("ConfigParser Error ({0})".format(e))
            return
        except ConfigParser.NoOptionError as e:
            logging.debug("ConfigParser Error ({0})".format(e))
            return
        self.__client = twitter.Api(consumer_key=__consumerKey,
                                    consumer_secret=__consumerSecret,
                                    access_token_key=__accessTokenKey,
                                    access_token_secret=__accessTokenSecret)
        
    def tweet(self, msg = None):
        if msg == None:
            logging.debug("Twitter Error Message is Empty")
            return
        if type(msg) is not str:
            logging.debug("Twitter Error Message is not a String")
            return
        if len(msg) > 140:
            logging.debug("Twitter Error Message Exceeds 140 Chars")
            return
        try:
            update = self.__client.PostUpdate(msg)
            return update.text
        except AttributeError as e:
            logging.debug("Attributer Error ({0})".format(e))
        except twitter.TwitterError as e:
            logging.debug("Twitter Error ({0})".format(e))

if __name__ == "__main__":
    longMesg = "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
    tooLongMesg = "901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
    emptyMesg = None
    errTweeter = tweeter("error.cfg")
    print errTweeter.tweet("Test1")
    myTweeter = tweeter()
    print myTweeter.tweet(123)
    print myTweeter.tweet(emptyMesg)
    print myTweeter.tweet(tooLongMesg)
    print myTweeter.tweet(longMesg)
    print myTweeter.tweet("Test1")





