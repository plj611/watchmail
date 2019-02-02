## Watchmail

Watchmail is a project to demostrate the idea of using email as a medium to execute actions on server. 

## Implementation

[Watchdog](https://pypi.org/project/watchdog/) is a prerequisite and monitor the change of the mailbox in mbox format. When there is a change in the mailbox, the message is read in and detemine the action the sender wants the server to preform. The message is removed after it.

## Installation 

### para.py

* Put the para.py into the same directory as watchmail.py

para.py:
```python
mb = 'mailbox name'
cb = 'subject prefix to indicate it is an email to execute action'
```
