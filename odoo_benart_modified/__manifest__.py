# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Certification',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 90,
    'summary': 'Track your certificate',
    'description': "",
    'website': '',
    'depends': [
        'hr',
        'contacts',
        'calendar',
        'fetchmail',
        'utm',
        'document',
        'web_tour',
        'digest',
        'backend_theme_v12',
        'theme_nice_bootstrap',
        'theme_common',
        'web_responsive',
        'website_animate',
    ],
    'data': [
        'security/certification_group.xml',
        'security/ir.model.access.csv',
        'data/validity_status_batch.xml',
        'views/hr_certificate_view.xml',
        'views/res_partner_view.xml',
        'views/web.xml',
        'views/hide_contract.xml',

    ],
    'demo': [

    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
