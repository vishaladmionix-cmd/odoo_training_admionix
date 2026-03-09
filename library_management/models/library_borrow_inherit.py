# models/library_borrow_inherit.py

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class BorrowModelInherit(models.Model):
    _inherit = 'library.borrow'  # ← NO _name, just _inherit
    #   this means: "go find library.borrow
    #   and add everything below into it"

    # ── NEW FIELDS added to existing library.borrow ─────

    remarks = fields.Text(string='Remarks')
    # staff can add notes like "Book was damaged"

    is_renewed = fields.Boolean(string='Is Renewed', default=False)
    # track if borrow was renewed/extended

    renewed_return_date = fields.Datetime(string='Renewed Return Date')

    # new return date after renewal

    # ── NEW OVERRIDE: write() ────────────────────────────
    # When is_renewed becomes True, auto-extend return date by 7 days
    # Everything else works exactly as before via super()

    def write(self, vals):
        for rec in self:
            if 'is_renewed' in vals and vals['is_renewed']:
                if rec.return_date:
                    from datetime import timedelta
                    vals['renewed_return_date'] = rec.return_date + timedelta(days=7)
        return super().write(vals)  # ← original write() still runs

    # ── NEW OVERRIDE: create() ───────────────────────────
    # When record is created, auto-fill remarks as 'No Remarks'
    # Your original sequence logic still runs via super()

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('remarks'):
                rec['remarks'] = 'No Remarks'  # default remark
        return super().create(vals)  # ← your original create() runs here
        #   sequence number still gets assigned


