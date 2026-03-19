from odoo import api, models, fields


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = "Library Member"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    partner_id = fields.Many2one('res.partner', string="Partner ID")
    borrow_count = fields.Integer(string="Borrow Count", compute='_compute_borrow_count', store=True)
    member_ids = fields.One2many('library.borrow', 'member_id', string="Borrow")
    user_id = fields.Many2one('res.users', string="User")

    # count of borrow

    @api.depends('member_ids')
    def _compute_borrow_count(self):
        for record in self:
            record.borrow_count = len(record.member_ids)

    def action_view_borrows(self):
        self.ensure_one()
        return {
            'name': 'Borrow Records',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_send_registration_email(self):
        for rec in self:
            template = self.env.ref('library_management.email_template_member_registration')
            template.send_mail(rec.id, force_send=True)
