from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError
class MissingEntry(models.Model):
    _name = 'mail.missed.fetch'

    subject = fields.Char("Subject")
    date = fields.Date("Sent")
    missing_ok = fields.Boolean("Missing OK")
    mail_message_id = fields.Char("Message-ID", index=True)

    _sql_constraints = [
        ('mail_message_id_unique', "unique(mail_message_id)", _("Only one unique entry allowed.")),
    ]