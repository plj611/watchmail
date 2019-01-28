#!/bin/env python

import time
import mailbox

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import para

class MyFileSystemEventHandler(FileSystemEventHandler):
   def __init__(self):
      #self.f = mailbox.mbox('/var/spool/mail/' + para.mb)
      FileSystemEventHandler.__init__(self)

   def on_created(self, event):
      print('Hello, you create a file {}'.format(event.src_path))

   def on_modified(self, event):
      if isinstance(event, FileModifiedEvent):
         print('You modified a file {}'.format(event.src_path))
         if (event.src_path.find(para.mb) != -1):
            f = mailbox.mbox('/var/spool/mail/' + para.mb)
            print((list(f.values())[-1])['subject'])
            for key, message in f.items():
               if message['subject'].startswith(para.cb):
                  sub = message['subject']
                  print(sub)
                  cmd = '99'
                  action = '9'
                  print(len(sub))
                  if len(sub) == 9:
                     tmp = sub[5:]
                     cmd = tmp[:2]
                     action = tmp[-1]
                     print(tmp, cmd, action)
                  switch = {
                     '00': self.connect_back, 
# Default action is to delete the message
                  }.get(cmd, lambda f, x, y: None)
                  switch(f, action, key)
 
   def connect_back(self, f, action, key):
      print('Hello I need to connect back')
      try:
         print('I am setting the flag now')
         f.lock()
         f.remove(key)
         #f.flush()
         f.close()
         #f = mailbox.mbox('/var/spool/mail/' + para.mb)
      except:
         print('error') 

event_handler = MyFileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, '/var/spool/mail' , recursive=True)
observer.start()
try:
   while True:
      time.sleep(1)
except KeyboardInterrupt:
   observer.stop()
observer.join()
