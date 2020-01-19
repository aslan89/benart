# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Parameter(models.Model):
    _name = 'benart.parameter'
    _rec_name = 'paramter_value'

    parameter_name = fields.Selection([('certification_body', 'Certification Body'), ('accreditation', 'Accreditation'),
                                       ('document_type', 'Document Type')],
                                      string='Parameter Name')

    paramter_value = fields.Char('Value')
    is_active = fields.Boolean('Is Active?', default=True)
    file = fields.Binary('File')
    file_name = fields.Char('File Name')

    document_type_id = fields.Many2one('benart.document_type','Document Type')


class DocumentType(models.Model):
    _name = 'benart.document_type'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
