#!/bin/env python

import time
import mailbox

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import para

class MyFileSystemEventHandler(FileSystemEventHandler):
   def __init__(self):
      self.f = mailbox.mbox('/var/spool/mail/' + para.mb)
      FileSystemEventHandler.__init__(self)

   def on_created(self, event):
      print('Hello, you create a file {}'.format(event.src_path))

   def on_modified(self, event):
      if isinstance(event, FileModifiedEvent):
         print('You modified a file {}'.format(event.src_path))
         if (event.src_path.find(para.mb) != -1):
            for key, message in self.f.items():
               if message['subject'].startswith(para.cb):
                  sub = message['subject']
                  print(sub)
                  tmp = sub.split('-')
                  cmd_action = tmp[1]
                  cmd_action = cmd_action.split(':')
                  cmd = cmd_action[0]
                  action = cmd_action[1]

                  switch = {
                     '00': self.connect_back, 
                  }.get(cmd, lambda x, y: None)
                  switch(action, key)
 
   def connect_back(self, action, key):
      print('Hello I need to connect back')
      try:
         self.f.lock()
         self.f.remove(key)
         self.f.flush()
         self.f.unlock()
         print('I am setting the flag now')
      except:
         pass

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
