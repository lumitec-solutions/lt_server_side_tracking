##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, api
import requests
import time
import hashlib


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        self.send_facebook_conversion(vals, res)
        return res

    def send_facebook_conversion(self, values, res):
        """Send data to facebook"""
        country = self.env['res.country'].browse(values.get('country_id'))
        date_time = time.mktime(res.create_date.timetuple())
        pixel_id = self.env['ir.config_parameter'].sudo().get_param('lt_server_side_tracking.pixel')
        access_token = self.env['ir.config_parameter'].sudo().get_param('lt_server_side_tracking.access_token')
        test_code = self.env['ir.config_parameter'].sudo().get_param('lt_server_side_tracking.test_event_code')
        url = 'https://graph.facebook.com/v16.0/' + pixel_id + '/events'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + access_token}
        payload = {
            "data": [
                {
                    "event_name": "Lead",
                    "event_time": date_time,
                    "user_data": {
                        "em": [hashlib.sha256(values.get('email_from').encode('utf-8')).hexdigest()] if values.get(
                            'email_from') else [],
                        "ct": [hashlib.sha256(values.get('city').encode('utf-8')).hexdigest()] if values.get(
                            'city') else [],
                        "zp": [hashlib.sha256(values.get('zip').encode('utf-8')).hexdigest()] if values.get(
                            'zip') else [],
                        "country": [hashlib.sha256(country.code.encode(
                            'utf-8')).hexdigest()] if country else [],
                    },
                    "custom_data": {
                        "currency": self.env['ir.config_parameter'].sudo().get_param('lead.conversion.currency'),
                        "value": int(self.env['ir.config_parameter'].sudo().get_param('lead.conversion.value')),
                    },
                    "event_id": res.id
                }
            ],
            "test_event_code": test_code if test_code else ""
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False
