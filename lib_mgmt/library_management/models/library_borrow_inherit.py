from datetime import timedelta
from odoo import api, models, fields


class BorrowModelInherit(models.Model):
    _inherit = 'library.borrow'

    remarks = fields.Text(string='Remarks')
    is_renewed = fields.Boolean(string='Is Renewed', default=False)
    renewed_return_date = fields.Datetime(string='Renewed Return Date')

    def write(self, vals):
        for rec in self:
            if 'is_renewed' in vals and vals['is_renewed']:
                if rec.return_date:
                    vals['renewed_return_date'] = rec.return_date + timedelta(days=7)
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            if not rec.get('remarks'):
                rec['remarks'] = 'No Remarks'
        return super().create(vals_list)
