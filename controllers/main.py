# noinspection PyUnresolvedReferences
from odoo.addons.sh_signup_email_approval.controllers.web_login import VerifyUserValidation
# noinspection PyUnresolvedReferences
from odoo.addons.sh_signup_email_approval.controllers.web_signup import WebHome
from odoo import http, SUPERUSER_ID
from odoo.http import request, Response
import logging
from pprint import pprint

_logger = logging.getLogger(__name__)


class SignUpHome(WebHome):

    def do_signup(self, qcontext):
        res = super().do_signup(qcontext)

        user_id = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))], limit=1)
        if user_id and user_id.share:
            user_id.state = 'unverified'

        return res


class VerifyUser(VerifyUserValidation):

    @http.route()
    def verify_user_validation(self, url, code):
        res = super().verify_user_validation(url, code)

        user_id = request.env.user
        if user_id.share and user_id.sh_user_from_signup and not user_id.id == request.env.ref('base.public_user').id:
            _logger.warning(f"New User {user_id.id} - {user_id.name} has been verified.")

            mail_tmpl_id = request.env.ref(
                'auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
            if mail_tmpl_id:
                mail_tmpl_id.sudo().with_user(SUPERUSER_ID).with_context(signup_approved=True).send_mail(user_id.id)
                _logger.warning(f"Welcome email sent to new User {user_id.id} - {user_id.name}")

        return res
