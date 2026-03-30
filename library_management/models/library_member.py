from odoo import api, models, fields


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = "Library Member"
    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    partner_id = fields.Many2one('res.partner', string="Partner ID")
    borrow_count = fields.Integer(string="Borrow Count", compute='compute_borrow_count', store=True)
    member_ids = fields.One2many('library.borrow', 'member_id', string="Members")

    # count of borrow
    @api.depends('member_ids')
    def compute_borrow_count(self):
        for record in self:
            record.borrow_count = self.env['library.borrow'].search_count([('member_id', '=', record.id)])

        return {
            'name': 'Borrow Record',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', record.id)],

        }



