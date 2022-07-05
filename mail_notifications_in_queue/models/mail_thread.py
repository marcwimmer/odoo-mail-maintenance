from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _notify_record_by_email(
        self,
        message,
        recipients_data,
        msg_vals=None,
        model_description=False,
        mail_auto_delete=True,
        check_existing=False,
        force_send=False,  
        send_after_commit=True,
        **kwargs
    ):
        mail_auto_delete = False  # this is the change
        res = super()._notify_record_by_email(
            message,
            recipients_data,
            msg_vals=msg_vals,
            model_description=model_description,
            mail_auto_delete=mail_auto_delete,
            check_existing=check_existing,
            force_send=force_send,  
            send_after_commit=send_after_commit,
            **kwargs
        )
        return res