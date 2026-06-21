import imaplib
import email
import re


class EmailReader:

    EMAIL = "anilkumar3939105@gmail.com"
    PASSWORD = "fery twuu qziq znux"

    @classmethod
    def get_latest_otp(cls):

        mail = imaplib.IMAP4_SSL(
            "imap.gmail.com"
        )

        mail.login(
            cls.EMAIL,
            cls.PASSWORD
        )

        mail.select("inbox")

        _, data = mail.search(
            None,
            "ALL"
        )

        ids = data[0].split()

        latest = ids[-1]

        _, msg_data = mail.fetch(
            latest,
            "(RFC822)"
        )

        raw = msg_data[0][1]

        msg = email.message_from_bytes(raw)

        body = str(msg)

        match = re.search(
            r"\b\d{6}\b",
            body
        )

        return match.group(0) if match else None