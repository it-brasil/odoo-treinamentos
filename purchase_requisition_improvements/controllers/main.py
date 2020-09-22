import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PurchaseOrderController(http.Controller):
    @http.route("/purchase/<string:po_eid>", type="http", website=True, auth="public", methods=['GET', 'POST'])
    def purchase_fill_prices(self, po_eid=None, **kw):
        po_id = request.env['purchase.order'].sudo().search(
            [('unique_eid', '=', po_eid),
             ('unique_eid', '!=', None)], limit=1)

        if kw:
            for key, value in kw.items():
                if not key.startswith('input_'):
                    continue
                line_id = int(key.replace('input_', ''))
                line = po_id.order_line.filtered(lambda x: x.id == line_id)

                line.price_unit = float(value.replace(',', '.'))
        
        return request.render("purchase_requisition_improvements.portal_purchase_order", {'po': po_id})