from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def send_mail(
            self, res_id, force_send=False, raise_exception=False, email_values=None, email_layout_xmlid=False):
        mail_tmpl_id = self.env.ref(
            'auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)

        if self.id == mail_tmpl_id.id:
            if self.env.context.get('signup_approved'):
                _logger.warning("Signup is approved... will send welcome email.")

            else:
                _logger.warning("Welcome email cannot be sent - User must verify their account first.")
                return False

        res = super().send_mail(res_id, force_send, raise_exception, email_values, email_layout_xmlid)

        return res
