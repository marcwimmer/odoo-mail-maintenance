import arrow
import re
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from email.utils import formatdate
import email
import logging
_logger = logging.getLogger()

class FetchMailServer(models.Model):
    _inherit = 'fetchmail.server'

    check_missing_days = fields.Integer("Check Missing for days", default=14)

    def _check_missed_mails(self):
        for rec in self:
            rec._checked_for_missed_mails()

    def _checked_for_missed_mails(self):
        for server in self:
            _logger.info('start checking for new emails on %s server %s', server.server_type, server.name)
            imap_server = None
            pop_server = None
            date = arrow.get().shift(days=-1 * server.check_missing_days).strftime("%d-%b-%Y")
            if server.server_type == 'imap':
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    result, data = imap_server.search(None, 'SINCE', date)
                    for num in data[0].split():
                        _logger.info(f"Checking for missing mail id {num}")
                        res_id = None
                        result, data = imap_server.fetch(num, '(RFC822)')
                        if result != 'OK':
                            raise Exception("Error fetching imap mail: " + result)
                        mm = email.message_from_string(data[0][1].decode('utf-8'))
                        self.env['mail.missed.fetch'].make_entry(mm)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.server_type, server.name, exc_info=True)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            elif server.server_type == 'pop':
                raise NotImplementedError("POP")
        return True
