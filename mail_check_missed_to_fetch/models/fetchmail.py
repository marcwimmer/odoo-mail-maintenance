from odoo import _, api, fields, models, SUPERUSER_ID
from datetime import datetime
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MissingEntry(models.Model):
    _name = 'mail.missed.fetch'

    subject = fields.Char("Subject")
    datetime = fields.Datetime("Sent")
    missing_ok = fields.Boolean("Missing OK")
    mail_message_id = fields.Char("Message-ID", index=True)

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
                        self.env['mail.missed.fetch'].make_entry(server, mm)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.server_type, server.name, exc_info=True)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            elif server.server_type == 'pop':
                raise NotImplementedError("POP")
        return True

    _sql_constraints = [
        ('mail_message_id_unique', "unique(mail_message_id)", _("Only one unique entry allowed.")),
    ]
