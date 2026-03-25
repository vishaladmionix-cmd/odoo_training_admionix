from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookModel(models.Model):
    _name = "library.book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True, tracking=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    price = fields.Float(string="Price")
    available_qty = fields.Integer(string="Available Qty", default=1)
    state = fields.Selection(
        [('available', 'Available'), ('unavailable', 'Unavailable')],
        compute='_compute_state',
        store=True,
    )
    book_ids = fields.One2many('library.borrow', 'book_id', string="Borrow Records")

    _check_isbn = models.Constraint(
        'UNIQUE(isbn)',
        'ISBN number must be unique.',
    )

    @api.depends('available_qty')
    def _compute_state(self):
        for book in self:
            book.state = 'unavailable' if book.available_qty == 0 else 'available'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('price', 0) < 0:
                raise ValidationError('Price cannot be less than 0.')
        return super().create(vals_list)

    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price < 0:
                raise ValidationError('Price cannot be less than 0.')

    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + " (Copy)",
            'isbn': False,
            'available_qty': 1,
            'book_ids': False,
        })
        return super().copy(default)

    def write(self, vals):
        return super().write(vals)

    def test_browse(self):
        book = self.env['library.book'].browse(1)
        print("Book ID:", book.id)
        print("Book Name:", book.name)

    def test_search_issued(self):
        records = self.env['library.book'].search([('state', '=', 'unavailable')])
        print("Unavailable Books:")
        for rec in records:
            print("Book:", rec.name, "Qty:", rec.available_qty)

    def test_search_count_unavailable(self):
        count = self.env['library.book'].search_count([('available_qty', '=', 0)])
        print("Total Unavailable Books:", count)

    def test_read_books(self):
        books = self.env['library.book'].search([])
        data = books.read(['name', 'available_qty'])
        print("===== READ =====")
        print(data)

    def delete_unavailable_books(self):
        books = self.env['library.book'].search([('available_qty', '=', 0)])
        books.unlink()
        print("Deleted Unavailable Books")

    def test_mapped(self):
        books = self.env['library.book'].search([])
        print("Book Names:", books.mapped('name'))

    def test_sorted(self):
        books = self.env['library.book'].search([])
        sorted_books = books.sorted('name')
        print("Sorted Books:", sorted_books.mapped('name'))

    def test_filter(self):
        books = self.env['library.book'].search([])
        available_books = books.filtered(lambda b: b.available_qty > 0)
        print("Available Books:", available_books.mapped('name'))
