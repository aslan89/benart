# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Advicer(models.Model):
    _name = "benart.advicer"
    _rec_name = 'company_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_name = fields.Char("Company Name", required=True, translate=True, track_visibility="onchange")
    authority_first_name = fields.Char("Authority Name", translate=True, track_visibility="onchange")
    authority_second_name = fields.Char("Authority Second Name", translate=True, track_visibility="onchange")
    adress = fields.Text("Address", required=True, translate=True, track_visibility="onchange")
    city = fields.Char("City", required=True, translate=True, track_visibility="onchange")
    country = fields.Char("Country", translate=True, track_visibility="onchange")
    phone_number = fields.Char("Phone Number", translate=True, track_visibility="onchange")
    fax_number = fields.Char("Fax Number", translate=True, track_visibility="onchange")
    website = fields.Char("Website", translate=True, track_visibility="onchange")
    email = fields.Char("Email", translate=True, track_visibility="onchange")
    tax_identity = fields.Char(" Tax Number / Tax Department", translate=True, track_visibility="onchange")

    active = fields.Boolean('Active', default=True, track_visibility="onchange", translate=True)
