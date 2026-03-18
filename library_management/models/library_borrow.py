# from datetime import timedelta, date
# from odoo import api, models, fields
# from odoo.exceptions import ValidationError
#
#
# class BorrowModel(models.Model):
#     _name = 'library.borrow'
#     _description = 'Library Borrow'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#
#     name = fields.Char(string='Sequence', copy=False, default='New', readonly=True, required=True)
#     member_id = fields.Many2one('library.member', string='Member')
#     book_id = fields.Many2one('library.book', string='Book')
#     borrow_date = fields.Datetime(string='Borrow Date', default=fields.Datetime.now)
#     return_date = fields.Datetime(string='Return Date')
#     actual_return_date = fields.Datetime(string='Actual Return Date')
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('issued', 'Issued'),
#         ('returned', 'Returned'),
#         ('late', 'Late'),
#     ], string='Status', default='draft', tracking=True)  # tracking=True logs state changes
#     color = fields.Integer()
#     fine_amount = fields.Float(
#         compute='compute_fine_amount', string='Fine Amount', store=True
#     )
#
#     # ── Compute fine amount ──────────────────────────────────────
#     @api.depends('actual_return_date', 'return_date')
#     def compute_fine_amount(self):
#         for rec in self:
#             rec.fine_amount = 0.0
#             if rec.return_date and rec.actual_return_date:
#                 if rec.return_date < rec.actual_return_date:
#                     late_days = (rec.actual_return_date - rec.return_date).days
#                     rec.fine_amount = late_days * 10
#
#     # ── Auto-sequence on create ──────────────────────────────────
#     @api.model_create_multi
#     def create(self, vals):
#         for rec in vals:
#             rec['name'] = self.env['ir.sequence'].next_by_code('library.borrow')
#         return super().create(vals)
#
#     # ── Onchange: set return_date = borrow_date + 7 days ────────
#     @api.onchange('book_id', 'borrow_date')
#     def change_data(self):
#         for rec in self:
#             if rec.book_id and rec.book_id.available_qty < 1:
#                 raise ValidationError('Out of Stock!')
#             if rec.borrow_date:
#                 rec.return_date = rec.borrow_date + timedelta(days=7)
#
#     # ── ISSUE BUTTON ─────────────────────────────────────────────
#     # FIX: removed wrong @api.depends decorator — buttons need no decorator
#     # def issue_button(self):
#     #     for rec in self:
#     #         # 1. Stock check
#     #         if not rec.book_id:
#     #             raise ValidationError('Please select a book!')
#     #         if rec.book_id.available_qty <= 0:
#     #             raise ValidationError('Book is out of stock!')
#     #
#     #         # 2. Update state + reduce stock
#     #         rec.book_id.available_qty -= 1
#     #         rec.state = 'issued'
#     #
#     #         # 3. Send Book Borrowed email
#     #         rec._send_email_with_log(
#     #             template_xml_id='library_management.email_template_book_borrowed',
#     #             log_subject='Book Borrowed Email Sent',
#     #             log_note=f'Borrow confirmation email sent to <b>{rec.member_id.name}</b> '
#     #                      f'for book <b>{rec.book_id.name}</b>. '
#     #                      f'Due date: {rec.return_date}.',
#     #         )
#
#     def issue_button(self):
#         for rec in self:
#             # 1. Stock check
#             if not rec.book_id:
#                 raise ValidationError('Please select a book!')
#             if rec.book_id.available_qty <= 0:
#                 raise ValidationError('Book is out of stock!')
#
#             # 2. Update state + reduce stock
#             rec.book_id.available_qty -= 1
#             rec.state = 'issued'
#
#     def action_send_mail(self):
#         for rec in self:
#             if rec.state != 'issued':
#                 continue
#             rec._send_email_with_log(
#                 template_xml_id='library_management.email_template_book_borrowed',
#                 log_subject='Book Issued – Email Sent (Server Action)',
#                 log_note=(
#                     f'Book issue email triggered via server action for '
#                     f'<b>{rec.member_id.name}</b> – '
#                     f'<b>{rec.book_id.name}</b>. '
#                     f'Due: {rec.return_date}.'
#                 ),
#             )
#
#     # ── DUE DATE REMINDER BUTTON ─────────────────────────────────
#     def action_send_due_reminder(self):
#         for rec in self:
#             rec._send_email_with_log(
#                 template_xml_id='library_management.email_template_due_date_reminder',
#                 log_subject='Due Date Reminder Sent',
#                 log_note=f'Due date reminder sent to <b>{rec.member_id.name}</b> '
#                          f'for <b>{rec.book_id.name}</b>. Due: {rec.return_date}.',
#             )
#
#     # ── OPEN RETURN WIZARD ───────────────────────────────────────
#     def action_open_wizard(self):
#         return {
#             'name': 'Return Book',
#             'type': 'ir.actions.act_window',
#             'res_model': 'library.return.wizard',
#             'view_mode': 'form',
#             'target': 'new',
#             'context': {
#                 'active_id': self.id,
#                 'active_model': self._name,
#             },
#         }
#
#     # ── SHARED HELPER: send email + post log note ────────────────
#     def _send_email_with_log(self, template_xml_id, log_subject, log_note):
#         """
#         Send a mail.template email and post an internal log note
#         to the chatter in one call.
#
#         :param template_xml_id: str  e.g. 'library_management.email_template_book_borrowed'
#         :param log_subject:     str  short subject for the chatter note
#         :param log_note:        str  HTML body for the chatter note
#         """
#         for rec in self:
#             template = self.env.ref(template_xml_id, raise_if_not_found=False)
#             if not template:
#                 rec.message_post(
#                     body=f'<p style="color:red">Email template <b>{template_xml_id}</b> not found.</p>',
#                     subject='Email Template Missing',
#                     message_type='comment',
#                     subtype_xmlid='mail.mt_note',
#                 )
#                 continue
#
#             try:
#                 # ── Send the email ───────────────────────────────────
#                 template.send_mail(rec.id, force_send=True)
#
#                 # ── Post SUCCESS log note to chatter ─────────────────
#                 rec.message_post(
#                     body=f"""
#                         <p>
#                           <span style="color:green">✓ Email Sent</span><br/>
#                           {log_note}
#                         </p>
#                     """,
#                     subject=log_subject,
#                     message_type='comment',
#                     subtype_xmlid='mail.mt_note',  # internal note (yellow, not emailed)
#                     author_id=self.env.user.partner_id.id,
#                 )
#
#             except Exception as e:
#                 # ── Post FAILURE log note to chatter ─────────────────
#                 rec.message_post(
#                     body=f'<p style="color:red">✗ Email failed: {e}</p>',
#                     subject=f'Email Failed: {log_subject}',
#                     message_type='comment',
#                     subtype_xmlid='mail.mt_note',
#                     author_id=self.env.user.partner_id.id,
#                 )
#
#     def late_email(self):
#         template = self.env.ref('library_book_management.email_late_book')
#         email_values = {'email_from': self.env.user.email}
#         template.send_mail(self.id, force_send=True, email_values=email_values)
#
# # ─────────────────────────────────────────────────────────────────────
#
#
# class ReturnWizard(models.TransientModel):
#     _name = 'library.return.wizard'
#     _description = 'Library Return Wizard'
#
#     actual_return_date = fields.Datetime(string='Actual Return Date')
#     fine_amount = fields.Float(string='Fine Amount', readonly=True)
#
#     def action_return(self):
#         active_id = self.env.context.get('active_id')
#         active_model = self.env.context.get('active_model')
#         record = self.env[active_model].browse(active_id)
#
#         if record.book_id:
#             record.book_id.available_qty += 1
#
#         record.write({
#             'actual_return_date': self.actual_return_date,
#             'fine_amount': self.fine_amount,
#             'state': 'returned',
#         })
#
#         fine_note = (
#             f'Fine applied: <b>{record.fine_amount}</b>'
#             if record.fine_amount else 'No fine applied.'
#         )
#         record._send_email_with_log(
#             template_xml_id='library_management.email_template_book_returned',
#             log_subject='Book Returned – Email Sent',
#             log_note=f'Return confirmation sent to <b>{record.member_id.name}</b>. {fine_note}',
#         )
#
#         return {'type': 'ir.actions.act_window_close'}


from datetime import timedelta, date
from odoo import api, models, fields
from odoo.exceptions import ValidationError


class BorrowModel(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Sequence', copy=False, default='New', readonly=True, required=True)
    member_id = fields.Many2one('library.member', string='Member')
    book_id = fields.Many2one('library.book', string='Book')
    borrow_date = fields.Datetime(string='Borrow Date', default=fields.Datetime.now)
    return_date = fields.Datetime(string='Return Date')
    actual_return_date = fields.Datetime(string='Actual Return Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    ], string='Status', default='draft', tracking=True)
    color = fields.Integer()
    fine_amount = fields.Float(
        compute='compute_fine_amount', string='Fine Amount', store=True
    )

    @api.depends('actual_return_date', 'return_date')
    def compute_fine_amount(self):
        for rec in self:
            rec.fine_amount = 0.0
            if rec.return_date and rec.actual_return_date:
                if rec.return_date < rec.actual_return_date:
                    late_days = (rec.actual_return_date - rec.return_date).days
                    rec.fine_amount = late_days * 10

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec['name'] = self.env['ir.sequence'].next_by_code('library.borrow')
        return super().create(vals)

    @api.onchange('book_id', 'borrow_date')
    def change_data(self):
        for rec in self:
            if rec.book_id and rec.book_id.available_qty < 1:
                raise ValidationError('Out of Stock!')
            if rec.borrow_date:
                rec.return_date = rec.borrow_date + timedelta(days=7)

    # ── ISSUE BUTTON ─────────────────────────────────────────────
    def issue_button(self):
        for rec in self:
            if not rec.book_id:
                raise ValidationError('Please select a book!')
            if not rec.member_id:
                raise ValidationError('Please select a member!')
            if rec.book_id.available_qty <= 0:
                raise ValidationError('Book is out of stock!')

            rec.book_id.available_qty -= 1
            rec.state = 'issued'

            # ✅ Send email automatically when book is issued
            rec._send_email_with_log(
                template_xml_id='library_management.email_template_book_borrowed',
                log_subject='Book Issued – Email Sent',
                log_note=(
                    f'Book issue confirmation email sent to '
                    f'<b>{rec.member_id.name}</b> '
                    f'for book <b>{rec.book_id.name}</b>. '
                    f'Due date: {rec.return_date}.'
                ),
            )

    # ── SERVER ACTION HANDLER ─────────────────────────────────────
    def action_send_mail(self):
        for rec in self:
            if rec.state != 'issued':
                continue
            rec._send_email_with_log(
                template_xml_id='library_management.email_template_book_borrowed',
                log_subject='Book Issued – Email Sent (Server Action)',
                log_note=(
                    f'Book issue email triggered via server action for '
                    f'<b>{rec.member_id.name}</b> – '
                    f'<b>{rec.book_id.name}</b>. '
                    f'Due: {rec.return_date}.'
                ),
            )

    # ── DUE DATE REMINDER BUTTON ─────────────────────────────────
    def action_send_due_reminder(self):
        for rec in self:
            rec._send_email_with_log(
                template_xml_id='library_management.email_template_due_date_reminder',
                log_subject='Due Date Reminder Sent',
                log_note=(
                    f'Due date reminder sent to <b>{rec.member_id.name}</b> '
                    f'for <b>{rec.book_id.name}</b>. Due: {rec.return_date}.'
                ),
            )

    # ── OPEN RETURN WIZARD ───────────────────────────────────────
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
            },
        }

    # ── SHARED HELPER ────────────────────────────────────────────
    def _send_email_with_log(self, template_xml_id, log_subject, log_note):
        for rec in self:
            template = self.env.ref(template_xml_id, raise_if_not_found=False)
            if not template:
                rec.message_post(
                    body=f'<p style="color:red">Email template <b>{template_xml_id}</b> not found.</p>',
                    subject='Email Template Missing',
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                )
                continue
            try:
                template.send_mail(rec.id, force_send=True)
                rec.message_post(
                    body=f'<p><span style="color:green">✓ Email Sent</span><br/>{log_note}</p>',
                    subject=log_subject,
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                    author_id=self.env.user.partner_id.id,
                )
            except Exception as e:
                rec.message_post(
                    body=f'<p style="color:red">✗ Email failed: {e}</p>',
                    subject=f'Email Failed: {log_subject}',
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                    author_id=self.env.user.partner_id.id,
                )


class ReturnWizard(models.TransientModel):
    _name = 'library.return.wizard'
    _description = 'Library Return Wizard'

    actual_return_date = fields.Datetime(string='Actual Return Date')
    fine_amount = fields.Float(string='Fine Amount', readonly=True)

    def action_return(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        record = self.env[active_model].browse(active_id)

        if record.book_id:
            record.book_id.available_qty += 1

        record.write({
            'actual_return_date': self.actual_return_date,
            'fine_amount': self.fine_amount,
            'state': 'returned',
        })

        fine_note = (
            f'Fine applied: <b>{record.fine_amount}</b>'
            if record.fine_amount else 'No fine applied.'
        )
        record._send_email_with_log(
            template_xml_id='library_management.email_template_book_returned',
            log_subject='Book Returned - Email Sent',
            log_note=f'Return confirmation sent to <b>{record.member_id.name}</b>. {fine_note}',
        )

        return {'type': 'ir.actions.act_window_close'}

