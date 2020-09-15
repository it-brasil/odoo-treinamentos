from odoo import api, fields, models



class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    supplier_ids = fields.Many2many('res.partner', string="Fornecedores")

    def action_generate_all_quotations(self): 
        for supplier in self.supplier_ids:
            order = self.env['purchase.order'].create({'partner_id': supplier.id, 'requisition_id': self.id})
            order._onchange_requisition_id()

            result = order.action_rfq_send()
            composer = self.env['mail.compose.message'].with_context(result['context']).create({})
            composer.onchange_template_id_wrapper()
            composer.action_send_mail()