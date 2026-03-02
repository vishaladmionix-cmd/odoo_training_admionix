from odoo import models, fields

class Student(models.Model):
    _name = 'orm.practice.student'
    _description = 'ORM Practice Student'

    name = fields.Char(string='Name',required=True)
    age = fields.Integer(string='Age',required=True)
    email = fields.Char()
    active = fields.Boolean(default=True)

    is_paid = fields.Boolean(default=False)
    print(;helopok)
wdwdwdewdwed