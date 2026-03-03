from gzip import WRITE

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookModel(models.Model):
    _name = "library.book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book"
    name = fields.Char(string="Name", required=True, tracking=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    price = fields.Float(string="Price")
    available_qty = fields.Integer(string="Available Qty", default=1)
    state = fields.Selection([('available', 'Available'), ('unavailable', 'Unavailable')], compute='_compute_state',store=True)
    book_ids = fields.One2many('library.borrow', 'book_id', string="Books")

    # _sql_constraints = [
    #     ('unique_isbn', 'UNIQUE(isbn)', 'ISBN number should be unique!!!'),
    # ]

    # unique sql constraint for isbn field
    _check_isbn = models.Constraint(
        'UNIQUE(isbn)',
        'ISBN number must be unique!!!.',
    )

    # state change according to qty available
    @api.depends('available_qty')
    def _compute_state(self):
        for book in self:
            if book.available_qty == 0:
                book.state = 'unavailable'
            else:
                book.state = 'available'

    # -----------------------------------   CREATE  -------------------------------------------------------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('price', 0) < 0:
                raise ValidationError('Price cannot be less than 0')
        return super().create(vals_list)

    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price < 0:
                raise ValidationError('Price cannot be less than 0')

    # -------------------------  COPY  --------------------------------------------------------------------------------------------------------
    def copy(self, default=None):
        default = dict(default or {})

        default.update({
            'name': self.name + " (Copy)",
            'isbn': False,
            'available_qty': 1,
            'book_ids': False,
        })

        return super().copy(default)

# ------------------------------  WRITE   ----------------------------------------------------------------------------

    def write(self, vals):
        print("Write Method is called")
        print("Updated Values: ", vals)
        return super().write(vals)

# ------------------------------------  BROWSE  -----------------------------------------------------------------------------------------
    def test_browse(self):
        book = self.env['library.book'].browse(1)
        print("Book ISBN: ",book.id)
        print("Book Name: ", book.name)

# ------------------------------------  SEARCH  -------------------------------------------------------------------------------------
    def test_search_issued(self):
        records = self.env['library.book'].search([('state', '=', 'unavailable')])

        print("Search method is called")
        print("Unavailable Books: ")

        for rec in records:
            print("Book:", rec.name)
            print("Qty: ",rec.available_qty)

# ------------------------------------ SEARCH COUNT    ------------------------------------------------------------------------------------
    def test_search_count_unavailable(self):
        count = self.env['library.book'].search_count([
            ('available_qty', '=', 0)
        ])
        print("search_count method is called")
        print("Total Unavailable Books:", count)
# ------------------------------------    READ    -------------------------------------------------------------------------------
    def test_read_books(self):
        books = self.env['library.book'].search([])
        data = books.read(['name', 'available_qty'])
        print("===== READ CALLED =====")
        print(data)

# ------------------------------------   UNLINK  --------------------------------------------------------------------------
    def delete_unavailable_books(self):
        books = self.env['library.book'].search([
            ('available_qty', '=', 0)
        ])
        books.unlink()
        print("Deleted Unavailable Books")

# --------------------------------------- MAP ----------------------------------------------------------------

    def test_mapped(self):
        books = self.env['library.book'].search([])
        names = books.mapped('name')
        print("Book Names:", names)
# -----------------------------------    SORT    ---------------------------------------------------------------

    def test_sorted(self):
        books = self.env['library.book'].search([])
        sorted_books = books.sorted('name')
        print("Sorted Books:", sorted_books.mapped('name'))

# -------------------------------------   FILTER -----------------------------------------------------------------

def test_filter(self):
    # Step 1: Get all books
    books = self.env['library.book'].search([])

    # Step 2: Filter books with available quantity > 0
    available_books = books.filtered(lambda b: b.available_qty > 0)

    # Step 3: Print names of filtered books
    print("Available Books:", available_books.mapped('name'))