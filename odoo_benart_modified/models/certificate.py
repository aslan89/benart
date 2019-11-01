# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date


class Certificate(models.Model):
    _name = 'benart.certificate'
    _rec_name = 'certification_number'

    application_date = fields.Date("Application Date")
    certification_body_id = fields.Many2one('benart.parameter',
                                            domain="[('parameter_name', '=', 'certification_body'),('is_active', '=', True)]")
    accreditation_id = fields.Many2one('benart.parameter',
                                       domain="[('parameter_name', '=', 'accreditation'),('is_active', '=', True)]")
    document_type_id = fields.Many2one('benart.parameter', domain="[('parameter_name', '=', 'document_type'),('is_active', '=', True)]",
                                       required=True)
    res_partner_id = fields.Many2one('res.partner', required=True)
    advicer_id = fields.Many2one('benart.advicer', string="Advicer")
    scope = fields.Text("Scope", required=True)
    certification_number = fields.Char("Certification Number", required=True)

    certificate_status = fields.Selection([
        ('active', 'Active'),
        ('passive', 'Passive'),
        ('canceled', 'Cancelled'),
        ('onhold', 'Onhold')], string='Certificate Status',
        copy=False, default='active', required=True)

    release_date = fields.Date("Release Date", required=True)
    validity_date = fields.Date("Validity Date", required=True)

    validity_status = fields.Char(String='Validity Status')


    @api.constrains('validity_date')
    def _compute_validity_status(self):

        if self.validity_date:
            rdelta = relativedelta(self.validity_date, date.today())

            if rdelta.years > 0:
                self.write({'validity_status': 'Years to Validity Expire'})
            elif rdelta.months > 0:
                self.write({'validity_status': 'Months to Validity Expire'})
            elif rdelta.weeks > 0:
                self.write({'validity_status': 'Weeks to Validity Expire'})
            elif rdelta.days > 0:
                self.write({'validity_status': 'Days to Validity Expire'})
            else:
                self.write({'validity_status': 'Validity Expired'})


class ResPartner(models.Model):
    _inherit = 'res.partner'