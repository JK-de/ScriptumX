"""Email backends: msmtp/sendmail, with safe logging when mail is not configured."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend

logger = logging.getLogger('scriptumx.mail')


def msmtp_is_configured() -> bool:
    """True when msmtp/sendmail exists and /etc/msmtprc has a non-comment account."""
    conf = os.environ.get('MSMTPRC', '/etc/msmtprc')
    if not os.path.isfile(conf):
        return False
    try:
        with open(conf, 'r', encoding='utf-8') as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                # Real config lines (host / account / from) mean relay may work
                if stripped.lower().startswith(('account', 'host', 'from', 'auth')):
                    # Ignore pure template placeholders
                    if 'example.com' in stripped.lower() or 'YOUR_' in stripped:
                        continue
                    return True
    except OSError:
        return False
    return False


def _sendmail_binary():
    for candidate in ('msmtp', '/usr/bin/msmtp', 'sendmail', '/usr/sbin/sendmail'):
        path = shutil.which(candidate) if not candidate.startswith('/') else (
            candidate if os.path.isfile(candidate) and os.access(candidate, os.X_OK) else None
        )
        if path:
            return path
    return None


class MsmtpEmailBackend(BaseEmailBackend):
    """
    Deliver mail via msmtp/sendmail -t.
    If msmtp is not configured, log the message (including password-reset links)
    for admins and do not raise — never put passwords in email bodies (Django
    reset mails only contain a link).
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        if not msmtp_is_configured():
            logger.warning(
                'msmtp not configured; logging %s email(s) instead of sending',
                len(email_messages),
            )
            return ConsoleEmailBackend(fail_silently=self.fail_silently).send_messages(
                email_messages
            )

        binary = _sendmail_binary()
        if not binary:
            logger.error('msmtp/sendmail binary missing; logging emails')
            return ConsoleEmailBackend(fail_silently=self.fail_silently).send_messages(
                email_messages
            )

        sent = 0
        for message in email_messages:
            try:
                raw = message.message().as_bytes(linesep='\r\n')
                proc = subprocess.run(
                    [binary, '-t', '-i'],
                    input=raw,
                    capture_output=True,
                    check=False,
                )
                if proc.returncode != 0:
                    err = proc.stderr.decode('utf-8', errors='replace')
                    logger.error('msmtp failed (%s): %s', proc.returncode, err)
                    if not self.fail_silently:
                        raise RuntimeError('msmtp failed: %s' % err)
                else:
                    sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
                logger.exception('msmtp send failed')
        return sent
