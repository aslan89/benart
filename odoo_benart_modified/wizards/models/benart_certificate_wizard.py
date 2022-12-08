# -*- encoding: utf-8 -*-
#

from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class BenartCertificateWizard(models.TransientModel):
    _name = 'benart.certificate.wizard'
    _description = 'Sertifika Toplu Güncelleme'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    certificate_status = fields.Selection([
        ('active', 'Active'),
        ('passive', 'Passive'),
        ('canceled', 'Cancelled'),
        ('onhold', 'Onhold')], string='Certificate Status',
        required=True, translate=True, track_visibility="onchange")

    certificate_ids = fields.Many2many('benart.certificate',
                                    relation='benart_certificate_wizard_rel',
                                    string='Sertifikalar', required=True)

    @api.model
    def default_get(self, fields):
        res = super(BenartCertificateWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')
        if active_model == "benart.certificate":
            res["certificate_ids"] = active_ids
        return res

    @api.one
    def action_apply(self):
        for certificate_id in self.certificate_ids:
            pass
            certificate_id.write({
                'certificate_status': self.certificate_status
            })

