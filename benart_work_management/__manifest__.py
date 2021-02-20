# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Work Management',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 90,
    'summary': 'Track your work',
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
        'odoo_benart_modified',
        'mail',
        'contacts'
    ],
    'data': [
        'security/work_management_group.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/work_management_view.xml',
        'data/work_management_batch.xml',
        'data/mail_template.xml'

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
