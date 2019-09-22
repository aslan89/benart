# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Advicer(models.Model):
    _name = "benart.advicer"
    _rec_name = 'company_name'

    company_name = fields.Char("Company Name", required=True)
    authority_first_name = fields.Char("Authority Name")
    authority_second_name = fields.Char("Authority Second Name")
    adress = fields.Text("Address", required=True)
    city = fields.Char("City", required=True)
    country = fields.Char("Country")
    phone_number = fields.Char("Phone Number")
    fax_number = fields.Char("Fax Number")
    website = fields.Char("Website")
    email = fields.Char("Email")
    tax_identity = fields.Char(" Tax Number / Tax Department")


