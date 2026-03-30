import logging
from datetime import timedelta

from odoo import api, models, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BorrowModel(models.Model):
    _name = 'library.borrow'
    _description = 'Library borrow'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Sequence', copy=False, default='New', readonly=True, required=True)
    member_id = fields.Many2one('library.member', string='Member')
    book_id = fields.Many2one('library.book', string='Book')
    borrow_date = fields.Datetime(string='Borrow Date', default=fields.Datetime.now)
    return_date = fields.Datetime(string='Return Date')
    actual_return_date = fields.Datetime(string='Actual Return Date')
    state = fields.Selection([('draft', 'Draft'), ('issued', 'Issued'), ('returned', 'Returned'), ('late', 'Late')],
                             string='Status', default="draft")
    color = fields.Integer()
    fine_amount = fields.Float(compute='compute_fine_amount', string='Fine Amount', store=True)

    # schedule ir.corn jobs
    def check_late_books(self):
        today = fields.Datetime.now()

        _logger.info("====== CRON STARTED ======")
        _logger.info(f"Today: {today}")

        late_borrows = self.search([
            ('state', '=', 'issued'),
            ('return_date', '<', today),
        ])

        _logger.info(f"Found {len(late_borrows)} late records")

        for record in late_borrows:
            if record.state:
                record.state = 'late'
                record.late_email()
            _logger.info(f"Marked late: {record.state}")

        _logger.info("====== CRON FINISHED ======")

    @api.model
    def check_late_manually(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for rec in self:
            print(rec.state)
            if rec.state and rec.state == 'returned':
                rec.state = 'late'

    # delete record
    def delete_record(self):
        for record in self:
            if record.state == 'returned':
                record.unlink()
            else:
                raise ValidationError("You can only delete Returned records!")

    # compute field for fine amount
    @api.depends('actual_return_date', 'return_date')
    def compute_fine_amount(self):
        for rec in self:
            rec.fine_amount = 0.0
            if rec.return_date and rec.actual_return_date:  # we have to check first if the data is there
                if rec.return_date < rec.actual_return_date:  # then compare it
                    rem_date = (
                            rec.actual_return_date - rec.return_date).days  # add .days as without it will not calculate
                    rec.fine_amount = rem_date * 10  # whenever different arises it will calculate eg 2*10 20 fine

    # sequence for name
    @api.model_create_multi
    def create(self, vals):  # vals is dictionary
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('library.borrow')  # first is environment then follow by model
            rec['name'] = code  # overwrite the name field with code
        res = super().create(vals)  # each time it create the record in db
        return res

    # onchange requirements
    @api.onchange("book_id", 'borrow_date')
    def change_data(self):
        for rec in self:
            if rec.book_id and rec.book_id.available_qty <= 0:
                raise ValidationError("This book is out of stock!!!")
            if rec.book_id:
                rec.return_date = rec.borrow_date + timedelta(days=7)

    # action wizard to open
    def action_open_wizard(self):
        return {
            'name': 'Return Book',
            'type': 'ir.actions.act_window',
            'res_model': 'library.return.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
                'active_model': self._name,
            }
        }

    # issue button
    @api.depends('book_id')
    def issue_button(self):
        for rec in self:
            rec.state = 'issued'
            if rec.state and rec.state == 'issued':
                rec.message_post(
                    body=(f"Book has been issued by {rec.member_id.name}!!!"),
                )
            if rec.book_id.available_qty:
                if rec.book_id.available_qty <= 0:

                    raise ValidationError('Book is out of stock !!!!')

                else:
                    rec.book_id.available_qty -= 1

    # email template
    def late_email(self):
        template = self.env.ref('library_book_management.email_late_book')
        for record in self:
            # email_values = {
            #     'email_to': record.member_id.email,
            # }
            template.send_mail(record.id, force_send=True)


class ReturnWizard(models.TransientModel):
    _name = 'library.return.wizard'
    _description = 'Library Return Wizard'

    actual_return_date = fields.Datetime(string='Actual Return Date')
    fine_amount = fields.Float(string='Fine Amount', readonly=True)

    # wizard action
    def action_return(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        record = self.env[active_model].browse(active_id)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>', record)
        if record.book_id:
            record.book_id.available_qty += 1
        record.write({

            'actual_return_date': self.actual_return_date,
            'fine_amount': self.fine_amount,
            'state': 'returned',
        })

        record.message_post(
            body=(f"The Book has been returned by {record.member_id.name}!!!"),
            message_type='comment'
        )
        return {'type': 'ir.actions.act_window_close'}
