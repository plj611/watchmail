## Watchmail

Watchmail is a project to demostrate the idea of using email as a medium to execute actions on server. 

## Implementation

[Watchdog](https://pypi.org/project/watchdog/) is a prerequisite and monitor the change of the mailbox in mbox format. When there is a change in the mailbox, the message is read in and detemine the action the sender wants the server to preform. The message is removed after it.

## Installation 

### para.py
Put the para.py into the same directory as watchmail.py
para.py:
```python
mb = 'mailbox name'
cb = 'subject prefix to indicate it is an email to execute action'
```

### Add the user having the mailbox to mail group
Since we are running the program as the user, the user who has the mailbox needs to have permission to create the .lock file in /var/spool/mail.
```
gpasswd -a USER GROUP
```

### watchmail.service
Since we will use systemd to start the program on start up. We need to modify the watchmail.service. In here, it is assumed that Python3 is used and the user having the mailbox is running the program.
```
[Service]
ExecStart=/usr/bin/python3.6 'path to watchmail.py'
User=USER
```

```
$ sudo cp watchmail.service /etc/systemd/system/
$ sudo systemctl start watchmail
$ sudo systemctl enable watchmail
```
