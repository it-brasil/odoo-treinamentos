import re
import json
import requests
from odoo import api, models



class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'


    @api.model
    def _send_sms_batch(self, messages):
        result = []

        url = 'https://api.totalvoice.com.br/sms'
        token = ''

        header = {'Content-Type': 'application/json', 'Access-Token': token}

        for message in messages:
            number = message.get('number')
            number = re.sub('[^0-9]', '', number or '')
            data = {
                'numero_destino': number,
                'mensagem':  message.get('content'),
            }

            response = requests.post(url, data=json.dumps(data), headers=header)  
            if response.status_code == 200:
                result.append({'state': 'success', 'res_id': message['res_id']})
            else:
                print(response.text)
                result.append({'state': 'insufficient_credit', 'res_id': message['res_id']})
        return result