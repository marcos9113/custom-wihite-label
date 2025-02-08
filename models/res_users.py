from odoo import models, fields, api, exceptions
from datetime import datetime
import logging
from pprint import pprint

from odoo.api import ValuesType, Self

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    state = fields.Selection(selection_add=[('unverified', "Unverified")])

    def _delete_unverified_users(self):
        """ Delete Portal signups if they have not been verified for > 24 hrs
        """
        for user_id in self.search([('share', '=', True), ('sh_user_from_signup', '=', False)]):
            hrs_since = (fields.Datetime.now() - user_id.create_date).seconds / 3600
            if hrs_since >= 24.0:
                _logger.warning(
                    f"Deleted User {user_id.id} - {user_id.name} because it's unverified for more than 24 hrs")

                partner_id = user_id.partner_id
                user_id.unlink()
                partner_id.unlink()

        return True

    def _compute_state(self):
        for user_id in self:
            if user_id.login_date and user_id.sh_user_from_signup:
                user_id.state = 'active'
            elif user_id.share:
                user_id.state = 'unverified'
            else:
                user_id.state = 'new'
