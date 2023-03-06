##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pixel = fields.Char(string="Pixel Id")
    access_token = fields.Char(string="Access Token")
    is_test = fields.Boolean(default=False)
    test_event_code = fields.Char(string="Test Event Code")

    @api.model
    def get_values(self):
        """get values from the fields"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo().get_param
        pixel_facebook = params('lt_server_side_tracking.pixel')
        access_token_facebook = params('lt_server_side_tracking.access_token')
        is_test = params('lt_server_side_tracking.is_test')
        test_event_code = params('lt_server_side_tracking.test_event_code')

        res.update(
            pixel=pixel_facebook,
            access_token=access_token_facebook,
            is_test=is_test,
            test_event_code=test_event_code,
        )
        return res

    def set_values(self):
        """Set values in the fields"""
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('lt_server_side_tracking.pixel', self.pixel)
        self.env['ir.config_parameter'].sudo().set_param('lt_server_side_tracking.access_token', self.access_token)
        self.env['ir.config_parameter'].sudo().set_param('lt_server_side_tracking.is_test', self.is_test)
        self.env['ir.config_parameter'].sudo().set_param('lt_server_side_tracking.test_event_code',
                                                         self.test_event_code)
