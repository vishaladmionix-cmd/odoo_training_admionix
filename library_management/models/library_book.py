from odoo import models, fields, api


class BookModel(models.Model):
    _name = "library.book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book"
    name = fields.Char(string="Name",required=True, tracking=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    price = fields.Float(string="Price")
    available_qty = fields.Integer(string="Available Qty",default=1)
    state = fields.Selection([('available', 'Available'), ('unavailable', 'Unavailable')], compute='_compute_state')
    book_ids = fields.One2many('library.borrow', 'book_id', string="Books")

    # _sql_constraints = [
    #     ('unique_isbn', 'UNIQUE(isbn)', 'ISBN number should be unique!!!'),
    # ]

    # unique sql constraint for isbn field
    _check_isbn = models.Constraint(
        'UNIQUE(isbn)',
        'ISBN number must be unique!!!.',
    )

    #state change according to qty available
    @api.depends('available_qty')
    def _compute_state(self):
        for book in self:
            if book.available_qty == 0:
                book.state = 'unavailable'
            else:
                book.state = 'available'