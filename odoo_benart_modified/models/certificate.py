# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import date


class Certificate(models.Model):
    _name = 'benart.certificate'
    _rec_name = 'certification_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    certification_body_id = fields.Many2one('benart.parameter',
                                            domain="[('parameter_name', '=', 'certification_body'),('is_active', '=', True)]")
    accreditation_id = fields.Many2one('benart.parameter', translate=True, track_visibility="onchange",
                                       domain="[('parameter_name', '=', 'accreditation'),('is_active', '=', True)]")
    record_type_id = fields.Many2one('benart.parameter', translate=True, track_visibility="onchange",
                                     domain="[('parameter_name', '=', 'record_type'),('is_active', '=', True)]")
    
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
        default='active', required=True, translate=True, track_visibility="onchange")

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

    hide_create_assignment = fields.Boolean('Hide Create Assignment', compute='_compute_hide_create_assignment',
                                            track_visibility="onchange", translate=True)

    @api.multi
    @api.constrains('certification_number')
    def constrains_certification_number(self):
        for i in self:
            certificate_ids = self.env['benart.certificate'].search([('certification_number', '=', i.certification_number),
                                                   ('id', '!=', self.id)])
            if certificate_ids:
                raise UserError(_("This certification number already used!"))


    @api.multi
    def _compute_hide_create_assignment(self):
        for i in self:
            work_management_id = self.env['benart.work_management'].search(
                [('res_partner_id', '=', i.res_partner_id.id), ('certificate_id', '=', i.id),
                 ('active', '=', True)])
            if work_management_id:
                i.hide_create_assignment = True
            else:
                i.hide_create_assignment = False

    def create_assignment(self):
        for i in self:
            if i.res_partner_id.id and i.id:
                self.env['benart.work_management'].create(
                    {'res_partner_id': i.res_partner_id.id, 'certificate_id': i.id,
                     'work_definiton_summary': "CERTIFICATION UPDATE NEEDED"})

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

                if i.validity__status in ("weeks_to_validity_expire", "days_to_validity_expire"):
                    work_management_id = self.env['benart.work_management'].search(
                        [('res_partner_id', '=', i.res_partner_id.id), ('certificate_id', '=', i.id),
                         ('active', '=', True)])
                    if not work_management_id:
                        self.env['benart.work_management'].create(
                            {'res_partner_id': i.res_partner_id.id, 'certificate_id': i.id,
                             'work_definiton_summary': "CERTIFICATION UPDATE NEEDED"})


class ResPartner(models.Model):
    _inherit = 'res.partner'
