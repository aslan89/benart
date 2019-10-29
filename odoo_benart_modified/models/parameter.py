# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Parameter(models.Model):
    _name = 'benart.parameter'
    _rec_name = 'paramter_value'

    parameter_name = fields.Selection([('certification_body', 'Certification Body'), ('accreditation', 'Accreditation'),
                                       ('document_attachment', 'Document'),
                                       ('document_type', 'Document Type')],
                                      string='Parameter Name')

    paramter_value = fields.Char('Value')
    is_active = fields.Boolean('Is Active?', default=True)

    file = fields.Binary('File')
    file_name = fields.Char('File Name')
