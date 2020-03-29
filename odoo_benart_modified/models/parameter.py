# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Parameter(models.Model):
    _name = 'benart.parameter'
    _rec_name = 'paramter_value'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    parameter_name = fields.Selection([('certification_body', 'Certification Body'), ('accreditation', 'Accreditation'),
                                       ('document_type', 'Document Type'),
                                       ('certificate_search_text', 'Certificate Search Text')], track_visibility="onchange",
                                      string='Parameter Name', translate=True)

    paramter_value = fields.Char('Value', translate=True, track_visibility="onchange")
    is_active = fields.Boolean('Is Active?', default=True, translate=True,track_visibility="onchange" )
    file = fields.Binary('File',track_visibility="onchange")
    file_name = fields.Char('File Name', translate=True, track_visibility="onchange")

    document_type_id = fields.Many2one('benart.document_type', 'Document Type', translate=True,track_visibility="onchange", )

    active = fields.Boolean('Active', default=True, track_visibility="onchange", translate=True)


class DocumentType(models.Model):
    _name = 'benart.document_type'

    name = fields.Char('Name', required=True, translate=True, track_visibility="onchange")
    active = fields.Boolean(default=True, translate=True, track_visibility="onchange")
