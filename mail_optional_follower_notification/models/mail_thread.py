# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import config


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_compute_recipients(self, message, msg_vals):
        """Compute recipients to notify based on subtype and followers. This
        method returns data structured as expected for ``_notify_recipients``."""
        test_condition = config["test_enable"] and not self.env.context.get(
            "test_optional_follow_notification"
        )
        recipient_data = super()._notify_compute_recipients(message, msg_vals)
        if test_condition:
            return recipient_data
        if not self.env.context.get("notify_followers", False):
            # filter out all the followers
            pids = (
                msg_vals.get("partner_ids", [])
                if msg_vals
                else message.sudo().partner_ids.ids
            )
            recipient_data = [d for d in recipient_data if d["id"] in pids]

        return recipient_data
