import uuid
import base64
from odoo import fields, models



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_new_eid(self):
        u = uuid.uuid4()
        b = base64.b32encode(u.bytes).decode()
        return b[0:24]

    unique_eid = fields.Char(string="EID", size=32, default=lambda x: x._get_new_eid(), readonly=True)

    def get_link_portal(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return "%s/purchase/%s" % (
            base_url,
            self.unique_eid,
        )
