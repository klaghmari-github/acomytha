"""Envoi minimal des e-mails transactionnels, avec boîte mémoire pour le développement."""

from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from acomytha.settings import Settings


class MailService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.outbox: list[dict[str, str]] = []

    def send_verification(self, email: str, url: str) -> None:
        subject = "Activez votre compte AcoMytha"
        body = (
            "Bienvenue dans AcoMytha.\n\n"
            "Pour activer votre compte parent, ouvrez ce lien valable "
            f"{self.settings.email_verification_hours} heures :\n{url}\n\n"
            "Si vous n'êtes pas à l'origine de cette demande, ignorez ce message."
        )
        self.outbox.append({"to": email, "subject": subject, "body": body, "url": url})
        if not self.settings.smtp_host:
            logging.getLogger("acomytha.mail").info("Lien de validation pour %s : %s", email, url)
            return
        message = EmailMessage()
        message["From"] = self.settings.smtp_from
        message["To"] = email
        message["Subject"] = subject
        message.set_content(body)
        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=15) as smtp:
            smtp.starttls()
            if self.settings.smtp_user:
                smtp.login(self.settings.smtp_user, self.settings.smtp_password)
            smtp.send_message(message)
