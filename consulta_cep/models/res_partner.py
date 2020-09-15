import re
import requests
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    street2 = fields.Char(string="Complemento")

    neighborhood = fields.Char(string="Bairro")

    def _execute_get_zip_info(self, zipcode):
        zipcode = re.sub('[^0-9]', '', zipcode or '')
        url = "https://viacep.com.br/ws/%s/json/unicode/" % zipcode

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @api.onchange('zip')
    def _consulta_cep_onchange_zip_code(self):
        data = self._execute_get_zip_info(self.zip)
        self.street = data.get('logradouro')
        self.street2 = data.get('complemento')
        self.city = data.get('localidade')
        self.neighborhood = data.get("bairro")

        uf = data.get('uf')
        state = self.env['res.country.state'].search([
            ('code', '=', uf),
            ('country_id.code', '=', 'BR'),
        ], limit=1)
        if state:
            self.state_id = state.id