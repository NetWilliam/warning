#!/usr/bin/env python
#! coding: utf-8
import itertools  
import sys    
import time   
              
import zmq    
              
def main():   
    if len (sys.argv) != 2:  
        print 'usage: publisher <bind-to>'  
        sys.exit (1)  
      
    bind_to = sys.argv[1]  
      
    all_topics = ['sports.general','sports.football','sports.basketball',  
                  'stocks.general','stocks.GOOG','stocks.AAPL',  
                  'weather']  
      
    ctx = zmq.Context()  
    s = ctx.socket(zmq.PUB)  
    s.bind(bind_to)  
  
    print "Starting broadcast on topics:"  
    print "   %s" % all_topics  
    print "Hit Ctrl-C to stop broadcasting."  
    print "Waiting so subscriber sockets can connect..."  
    print  
    time.sleep(1.0)  
      
    msg_counter = itertools.count()  
    try:  
        for topic in itertools.cycle(all_topics):  
            msg_body = str(msg_counter.next())  
            import pickle
            print '   Topic: %s, msg:%s' % (topic, msg_body)#, " pickle format: ", pickle.dumps([topic, msg_body])
            s.send_multipart([topic, msg_body])  
            #s.send_pyobj([topic, msg_body])  
            # short wait so we don't hog the cpu  
            time.sleep(0.1)  
    except KeyboardInterrupt:  
        pass  
  
    print "Waiting for message queues to flush..."  
    time.sleep(0.5)  
    s.close()  
    print "Done."  
  
if __name__ == "__main__":  
    main()  

