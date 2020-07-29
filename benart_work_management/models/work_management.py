# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.tools.translate import _

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Less Important'),
    ('2', 'Important'),
    ('3', 'High Important')
]


class WorkManagement(models.Model):
    _name = 'benart.work_management'
    _rec_name = 'work_definiton_summary'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    @api.model
    def _get_default_stage(self):
        stage_ids = self.env['benart.par.work_management_stage'].search([('active','=',True)], order="sequence asc")

        if stage_ids:
            return stage_ids[0]

    res_partner_id = fields.Many2one('res.partner', required=True, string="Firm", translate=True,
                                     track_visibility="onchange")
    res_partner_id_name = fields.Char(related='res_partner_id.name')
    mobile = fields.Char(related='res_partner_id.mobile')
    email = fields.Char(related='res_partner_id.email')

    work_definiton_summary = fields.Char('Work Definition Summary', track_visibility="onchange", translate=True)
    work_definiton = fields.Text('Work Definition', track_visibility="onchange", translate=True)

    work_management_stage_id = fields.Many2one('benart.par.work_management_stage', 'Stage',
                                               translate=True, track_visibility="onchange", required=True,
                                               index=True, default = _get_default_stage )

    certificate_name = fields.Char(related='certificate_id.certification_number')

    certificate_id = fields.Many2one('benart.certificate', 'Certificate',
                                               translate=True, track_visibility="onchange")

    active = fields.Boolean('Active', default=True, track_visibility="onchange", translate=True)

    color = fields.Integer("Color Index", default=0)
    priority = fields.Selection(AVAILABLE_PRIORITIES, "Appreciation", default='0')

    categ_ids = fields.Many2many('benart.work_management_category', string="Tags")

    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State', translate=True,
        copy=False, default='normal', required=True)

    legend_blocked = fields.Char(related='work_management_stage_id.legend_blocked', string='Kanban Blocked',
                                 readonly=False)
    legend_done = fields.Char(related='work_management_stage_id.legend_done', string='Kanban Valid', readonly=False)
    legend_normal = fields.Char(related='work_management_stage_id.legend_normal', string='Kanban Ongoing',
                                readonly=False)



    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (
        self.env.ref('benart_work_management.ir_attachment_view_search_inherit_work_management').id,)
        return action


class WorkManagementStage(models.Model):
    _name = 'benart.par.work_management_stage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'

    name = fields.Char('Name', required=True, translate=True, track_visibility="onchange")
    active = fields.Boolean(default=True, translate=True, track_visibility="onchange")

    sequence = fields.Integer(
        "Sequence", default=10,
        help="Gives the sequence order when displaying a list of stages.")

    fold = fields.Boolean(
        "Folded in Recruitment Pipe",
        help="This stage is folded in the kanban view when there are no records in that stage to display.")

    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda self: _('Blocked'), translate=True, required=True)
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda self: _('Ready for Next Stage'), translate=True, required=True)
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda self: _('In Progress'), translate=True, required=True)


class WorkManagementCategory(models.Model):
    _name = 'benart.work_management_category'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, translate=True, track_visibility="onchange")
    active = fields.Boolean(default=True, translate=True, track_visibility="onchange")
