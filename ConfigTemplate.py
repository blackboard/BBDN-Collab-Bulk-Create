collab = {
    "collab_key" : "YOURKEY",
    "collab_secret" : "YOURSECRET",
    "collab_base_url" : "COLLAB_URI",
    "verify_certs" : "True"
}

session_settings = {
    "createdTimezone" : "America/New_York",
    "courseRoomEnabled" : "false",
    "boundaryTime": "15",
    "participantCanUseTools": "false",
    "occurrenceType": "S",
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
            "level" : "INFO",
            "formatter" : "simple",
            "filename" : "logs/session-creation.log",
            "maxBytes" : 10485760,
            "backupCount" : 20,
            "encoding" : "utf8"
        },
        "console": {
            "class" : "logging.StreamHandler",
            "level" : "INFO",
            "formatter" : "simple",
            "stream" : "ext://sys.stdout"
        }
    },
    "loggers" : {
        "sessions" : {
            "level": "INFO",
            "handlers" : ["collab_file_handler","console"],
            "propagate" : "no"
        },
        "contexts": {
            "level": "INFO",
            "handlers": ["collab_file_handler","console"],
            "propagate": "no"
        },
        "users": {
            "level": "INFO",
            "handlers": ["collab_file_handler","console"],
            "propagate": "no"
        },
        "csv": {
            "level": "INFO",
            "handlers": ["collab_file_handler","console"],
            "propagate": "no"
        },
        "email": {
            "level": "INFO",
            "handlers": ["collab_file_handler","console"],
            "propagate": "no"
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["collab_file_handler","console"]
    }
}