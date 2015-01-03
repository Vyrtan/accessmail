
# all information from http://www.patshaping.de/hilfen_ta/pop3_smtp.htm
clunkyConfig = {
    # GMAIL
    0: {
        "IMAP": {
            "host": "imap.gmail.com",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.gmail.com",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },

    # WEB.DE
    1: {
        "IMAP": {
            "host": "imap.web.de",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.web.de",
            "port": 587,
            "ssl": True,
            "auth": True
        }
    },

    # ARCOR
    2: {
        "IMAP": {
            "host": "imap.arcor.de",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "mail.arcor.de",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },

    # GMX
    3: {
        "IMAP": {
            "host": "imap.gmx.net",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "mail.gmx.net",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },

    # OUTLOOK (HOTMAIL)
    # .com probably has to be replaced by .de
    4: {
        "IMAP": {
            "host": "imap-mail.outlook.com",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp-mail.outlook.com",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    },

    # YAHOO
    5: {
        "IMAP": {
            "host": "imap.mail.yahoo.com",
            "port": 993,
            "ssl": True
        },
        "SMTP": {
            "host": "smtp.mail.yahoo.com",
            "port": 465,
            "ssl": True,
            "auth": True
        }
    }
}