#!/bin/env python
#/usr/bin/python3.6

import time
import mailbox

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import para
import MySQLdb
import datetime

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
            #print((list(f.values())[-1])['subject'])
            for key, message in f.items():
               if message['subject'].lower().startswith(para.cb):
                  sub = message['subject']
                  print('Subject of email: {}'.format(sub))
                  cmd = '99'
                  action = '9'
                  #print(len(sub))
                  if len(sub) == (5 + len(para.cb)):
                     tmp = sub[5:]
                     cmd = tmp[:2]
                     action = tmp[-1]
                     print('Whole: {} Cmd: {} Action: {}'.format(tmp, cmd, action))
#                  switch = {
#                     '00': self.connect_back, 
#                  }.get(cmd, lambda x: None)
#                  switch(action)
                 
                  if cmd in ('00', '01', '02', '03', '04'):
                     self.insert_db(cmd, action)

                  try:
                     f.lock()
                     f.remove(key)
                     f.close()
                  except:
                     print('error in working mbox')
 
#   def connect_back(self, action):
   def insert_db(self, cmd, action):
      print('Hello I need to insert in DB')
#      with open(para.cb_flag, 'w') as f:
#         if action == '1':
#            f.write('1\n')
#         else:
#            f.write('0\n')
 
#      conn = MySQLdb.connect(user = 'lh', password = 'IPa55w0rd!')
      conn = MySQLdb.connect(user = para.dbuser, password = para.dbpassword, db = para.dbmaster)
      cursor = conn.cursor()
      try:
#         ret = cursor.execute('select * from infra.indicator_lighthouse where cmd = %s', ('00', ))
#         ret = cursor.execute('select * from indicator_lighthouse where cmd = %s', ('00', ))
#         if ret == 0:
#            cursor.execute('insert into infra.indicator_lighthouse (cmd) values (%s)', ('00', ))
#            cursor.execute('insert into indicator_lighthouse (cmd) values (%s)', ('00', ))
#         cursor.execute('update infra.indicator_lighthouse set act = %s, date_time = %s where cmd = %s', (action, datetime.datetime.now(), '00'))
#         cursor.execute('update indicator_lighthouse set act = %s, date_time = %s where cmd = %s', (action, datetime.datetime.now(), '00'))

        
         cursor.execute('insert into indicator_lighthouse (cmd, act, create_date_time) values (%s, %s, %s)', (cmd, action, datetime.datetime.utcnow()))
         conn.commit()
         print('DB insert!')
      except:
         print('error in updating db')
         conn.rollback()
      finally:
         cursor.close()
         conn.close()

event_handler = MyFileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, '/var/spool/mail' , recursive=False)
observer.start()
try:
   while True:
      time.sleep(1)
except KeyboardInterrupt:
   observer.stop()
observer.join()
