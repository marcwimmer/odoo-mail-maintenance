from odoo import _, api, fields, models, SUPERUSER_ID
from datetime import datetime
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MissingEntry(models.Model):
    _name = 'mail.missed.fetch'
    _order = 'date desc'

    subject = fields.Char("Subject")
    date = fields.Date("Sent")
    missing_ok = fields.Boolean("Missing OK")
    mail_message_id = fields.Char("Message-ID", index=True)
    fetchmail_server_id = fields.Many2one("fetchmail.server", string="Fetchmail")

    @api.model
    def make_entry(self, server, parsed_message):
        message_id = parsed_message['message-id'].strip()
        self.env.cr.execute("select count(*) from mail_message where message_id=%s", (message_id,))
        existing_mm = self.env.cr.fetchone()[0]
        existing_entries = self.sudo().search([('mail_message_id', '=', message_id)])
        try:
            date = datetime.strptime(parsed_message['Date'], "%a, %d %b %Y %H:%M:%S %z")
        except:
            date = False
        if not existing_mm and not existing_entries:
            self.create({
                'mail_message_id': message_id,
                'date': date,
                'subject': parsed_message['Subject'],
                'fetchmail_server_id': server.id
            })
        elif existing_mm and existing_entries:
            existing_entries.unlink()

    _sql_constraints = [
        ('mail_message_id_unique', "unique(mail_message_id)", _("Only one unique entry allowed.")),
    ]