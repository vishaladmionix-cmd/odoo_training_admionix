from odoo import models, fields

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    published_date = fields.Date(string="Published Date")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("published", "Published"),
        ],
        string="Status",
        default="draft",
    )
