collab = {
    "collab_key" : "YOURKEY",
    "collab_secret" : "YOURSECRET",
    "collab_base_url" : "COLLAB_URI",
    "verify_certs" : "True"
}

email = {
    "from" : "EMAILADDRESS",
    "subject" : "SUBJECT"
}

session_settings = {
    "createdTimezone" : "America/New_York",
    "courseRoomEnabled" : "false",
    "boundaryTime": "15",
    "participantCanUseTools": "false",
    "occurrenceType": "S",
    "recurrenceEndType": "on_date",
    "daysOfTheWeek": [
      "mo",
      "tu",
      "we",
      "th",
      "fr"
    ],
    "recurrenceType": "daily",
    "interval": "1",
    "numberOfOccurrences": 0,
    "endDate": "2020-03-27T17:00:00.000Z",
    "allowInSessionInvitees": "false",
    "allowGuest": "false",
    "guestRole": "participant",
    "canAnnotateWhiteboard": "false",
    "canDownloadRecording": "false",
    "canPostMessage": "false",
    "canShareAudio": "false",
    "canShareVideo": "false",
    "mustBeSupervised": "true",
    "openChair": "false",
    "raiseHandOnEnter": "true",
    "showProfile": "false"
}

logging = {
    "version" : 1,
    "formatters" : {
        "simple" : {
            "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    "handlers" : {
        "collab_file_handler" : {
            "class" : "logging.handlers.RotatingFileHandler",
            "level" : "DEBUG",
            "formatter" : "simple",
            "filename" : "logs/session-creation.log",
            "maxBytes" : 10485760,
            "backupCount" : 20,
            "encoding" : "utf8"
        }
    },
    "loggers" : {
        "sessions" : {
            "level": "DEBUG",
            "handlers" : ["collab_file_handler"],
            "propagate" : "no"
        },
        "contexts": {
            "level": "DEBUG",
            "handlers": ["collab_file_handler"],
            "propagate": "no"
        },
        "users": {
            "level": "DEBUG",
            "handlers": ["collab_file_handler"],
            "propagate": "no"
        },
        "csv": {
            "level": "DEBUG",
            "handlers": ["collab_file_handler"],
            "propagate": "no"
        },
        "email": {
            "level": "DEBUG",
            "handlers": ["collab_file_handler"],
            "propagate": "no"
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["collab_file_handler"]
    }
}