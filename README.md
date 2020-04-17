# BBDN-Collab-Bulk-Create
This is an open source Python project that allows an institution with a Blackboard Collaborate license to bulk create contexts, users, sessions, and enrollments.

This project is built with Python 3.7. You have two choices to build. You can use virtualenv. From the commandline on a Mac:

```
source venv/bin/activate
python CreateSessions.py
deactivate
```

If you are running on Windows, here is a [document describing the use of virtualenv](https://docs.python.org/3.7/library/venv.html).

You can also just install the libraries locally:

```
pip install -r requirements.txt
```

Before running, you must copy ConfigTemplate.py to Config.py and insert your credentials.




