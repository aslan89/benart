# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'


    company_number = fields.Char("Company Number", required=True,)

    certificated_ids = fields.One2many('benart.certificate', 'res_partner_id', string='Certificates')



