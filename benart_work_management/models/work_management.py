# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.tools.translate import _
from datetime import date, datetime

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
        stage_ids = self.env['benart.par.work_management_stage'].search([('active', '=', True)], order="sequence asc")

        if stage_ids:
            return stage_ids[0]

    state = fields.Selection([('open', 'Open'),
                              ('completed', 'Completed'),
                              ('cancelled', 'Cancelled')], string='State', default='open', translate=True,
                             track_visibility="onchange", required=True)

    res_partner_id = fields.Many2one('res.partner', required=True, string="Firm", translate=True,
                                     track_visibility="onchange")
    res_partner_id_name = fields.Char(related='res_partner_id.name')
    mobile = fields.Char(related='res_partner_id.mobile')
    email = fields.Char(related='res_partner_id.email')

    assingnee_id = fields.Many2one('hr.employee', string="Assingnee", translate=True,
                                   track_visibility="onchange")

    work_definiton_summary = fields.Char('Work Definition Summary', track_visibility="onchange", translate=True,
                                         required=True, )
    work_definiton = fields.Text('Work Definition', track_visibility="onchange", translate=True)

    work_management_stage_id = fields.Many2one('benart.par.work_management_stage', 'Stage',
                                               translate=True, track_visibility="onchange", required=True,
                                               index=True, default=_get_default_stage)

    certificate_name = fields.Char(related='certificate_id.certification_number')

    certificate_id = fields.Many2one('benart.certificate', 'Certificate',
                                     translate=True, track_visibility="onchange")

    deadline_date = fields.Date("Deadline", translate=True, track_visibility="onchange",
                                default=fields.Date.context_today)

    active = fields.Boolean('Active', default=True, track_visibility="onchange", translate=True)

    color = fields.Integer("Color Index", default=0)
    priority = fields.Selection(AVAILABLE_PRIORITIES, "Appreciation", default='0')

    categ_ids = fields.Many2many('benart.work_management_category', string="Tags")

    hide_deadline_date = fields.Boolean('Hide Deadline', compute='_compute_hide_deadline_date',
                                        track_visibility="onchange", translate=True)

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

    @api.model
    def get_email_to_only_admin(self):
        user_group = self.env.ref("odoo_benart_modified.group_certification_admin")
        email_list = [
            usr.login for usr in user_group.users if usr.login]
        return ",".join(email_list)

    @api.multi
    def work_management_batch(self):
        template = self.env.ref('benart_work_management.work_management_not_updated_work')
        work_management_id = self.env['benart.work_management'].search([('active', '=', True)], limit=1)
        if template:
            template.send_mail(work_management_id.id, force_send=True)

    @api.multi
    def get_not_updated_works(self):
        not_updated_work_management_ids = []
        work_management_ids = self.env['benart.work_management'].search([('active', '=', True), ('state', '=', 'open')])
        for i in work_management_ids:
            message_id = self.env['mail.message'].search(
                [ ('message_type', '=', 'comment'), ('model', '=', 'benart.work_management'),
                 ('res_id', '=', i.id)], order="date desc",limit=1)
            if not message_id and i.create_date < (datetime.today()-relativedelta(weeks=1)):
                not_updated_work_management_ids.append(i)
            elif message_id and message_id.date < (datetime.today()-relativedelta(weeks=1)):
                not_updated_work_management_ids.append(i)
        return not_updated_work_management_ids

    @api.multi
    def _compute_hide_deadline_date(self):
        for i in self:
            if self.env.user.has_group('benart_work_management.group_work_management_admin'):
                i.hide_deadline_date = True
            else:
                i.hide_deadline_date = False

    @api.multi
    @api.constrains('work_management_stage_id')
    def _compute_assingnee_id(self):
        template = self.env.ref('benart_work_management.work_management_assign_mail')
        for i in self:
            if i.work_management_stage_id and i.work_management_stage_id.default_assignee_id:
                i.assingnee_id = i.work_management_stage_id.default_assignee_id
                if template:
                    template.send_mail(i.id, force_send=True)

    @api.model
    def get_email_to(self):
        user_group = self.env.ref("benart_work_management.group_work_management_admin")
        email_list = [
            usr.login for usr in user_group.users if usr.login]
        if self.assingnee_id:
            email_list.append(self.assingnee_id.user_id.login)
        return ",".join(email_list)

    def complete_work(self):
        template = self.env.ref('benart_work_management.work_management_completed_maill')
        if template:
            for i in self:
                i.active = False
                i.state = "completed"
                template.send_mail(i.id, force_send=True)

    def cancel_work(self):
        template = self.env.ref('benart_work_management.work_management_cancelled_maill')
        if template:
            for i in self:
                i.active = False
                i.state = "cancelled"
                template.send_mail(i.id, force_send=True)

    def reopen_work(self):
        template = self.env.ref('benart_work_management.work_management_reopen_maill')
        if template:
            for i in self:
                i.active = True
                i.state = "open"
                template.send_mail(i.id, force_send=True)

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
    default_assignee_id = fields.Many2one('hr.employee', string="Assingnee", translate=True,
                                          track_visibility="onchange")
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
