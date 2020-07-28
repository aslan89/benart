# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date


class Certificate(models.Model):
    _name = 'benart.certificate'
    _rec_name = 'certification_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    certification_body_id = fields.Many2one('benart.parameter',
                                            domain="[('parameter_name', '=', 'certification_body'),('is_active', '=', True)]")
    accreditation_id = fields.Many2one('benart.parameter', translate=True, track_visibility="onchange",
                                       domain="[('parameter_name', '=', 'accreditation'),('is_active', '=', True)]")
    document_type_id = fields.Many2one('benart.parameter', translate=True, track_visibility="onchange",
                                       domain="[('parameter_name', '=', 'document_type'),('is_active', '=', True)]",
                                       required=True)
    res_partner_id = fields.Many2one('res.partner', required=True, string="Firm", translate=True,
                                     track_visibility="onchange")
    advicer_id = fields.Many2one('benart.advicer', string="Advicer")
    scope = fields.Text("Scope", required=True, translate=True, track_visibility="onchange")
    certification_number = fields.Char("Certification Number", required=True, track_visibility="onchange")
    standart_definition = fields.Char("Standart Definition", required=True, track_visibility="onchange")

    certificate_status = fields.Selection([
        ('active', 'Active'),
        ('passive', 'Passive'),
        ('canceled', 'Cancelled'),
        ('onhold', 'Onhold')], string='Certificate Status',
        copy=False, default='active', required=True, translate=True, track_visibility="onchange")

    release_date = fields.Date("Release Date", required=True, track_visibility="onchange")
    validity_date = fields.Date("Validity Date", required=True, track_visibility="onchange")

    validity__status = fields.Selection([
        ('years_to_validity_expire', 'Years to Validity Expire'),
        ('months_to_validity_expire', 'Months to Validity Expire'),
        ('weeks_to_validity_expire', 'Weeks to Validity Expire'),
        ('days_to_validity_expire', 'Days to Validity Expire'),
        ('expired', 'Expired'),
    ], string='Validity Status', store=True, readonly=1,
        translate=True, compute='_compute_validity__status')

    validity_status = fields.Char(String='Validity Status', readonly=1, track_visibility="onchange", translate=True)

    active = fields.Boolean('Active', default=True, track_visibility="onchange", translate=True)

    def create_assignment(self):
        for i in self:
            self.env['benart.work_assignment'].create({'res_partner_id': i.res_partner_id.id, 'certificate_id': i.id,
                                                       'work_definiton_summary': "BATCH"})

    @api.multi
    @api.depends('validity_date')
    def _compute_validity__status(self):
        for i in self:
            if i.validity_date:
                rdelta = relativedelta(i.validity_date, date.today())

                if rdelta.years > 0:
                    i.validity__status = "years_to_validity_expire"
                elif rdelta.months > 0:
                    i.validity__status = "months_to_validity_expire"
                elif rdelta.weeks > 0:
                    i.validity__status = "weeks_to_validity_expire"
                elif rdelta.days > 0:
                    i.validity__status = "days_to_validity_expire"
                else:
                    i.validity__status = "expired"

    @api.multi
    def validity_status_batch(self):
        certificate_ids = self.env['benart.certificate'].search([('active', '=', True)])
        for i in certificate_ids:
            if i.validity_date:
                rdelta = relativedelta(i.validity_date, date.today())

                if rdelta.years > 0:
                    i.validity__status = "years_to_validity_expire"
                elif rdelta.months > 0:
                    i.validity__status = "months_to_validity_expire"
                elif rdelta.weeks > 0:
                    i.validity__status = "weeks_to_validity_expire"
                elif rdelta.days > 0:
                    i.validity__status = "days_to_validity_expire"
                else:
                    i.validity__status = "expired"


class ResPartner(models.Model):
    _inherit = 'res.partner'
