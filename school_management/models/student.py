from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolManagement(models.Model):
    _name = 'school.management'
    _description = 'School Management (Student)'

    name = fields.Char(required=True)
    age = fields.Integer()
    email = fields.Char()
    active = fields.Boolean(default=True)

    teacher_id = fields.Many2one('school.teacher', string="Class Teacher")
    subject_ids = fields.Many2many('school.subject', string="Subjects")

    is_minor = fields.Boolean(
        string="Is Minor",
        compute="_compute_is_minor",
        store=True
    )

    # -------------------------
    # COMPUTE
    # -------------------------
    @api.depends('age')
    def _compute_is_minor(self):
        for rec in self:
            rec.is_minor = bool(rec.age and rec.age < 18)

    # -------------------------
    # CONSTRAINTS
    # -------------------------
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age and rec.age < 5:
                raise ValidationError("Student age must be 5 or older.")

    @api.constrains('teacher_id')
    def _check_teacher(self):
        for rec in self:
            if not rec.teacher_id:
                raise ValidationError("Class Teacher must be assigned.")

    _sql_constraints = [
        ('school_management_email_unique', 'unique(email)', 'This email is already in use!')
    ]


# --------------------------------------------------------------------

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name', required=True)
    student_ids = fields.One2many('school.management', 'teacher_id', string='Students')
    subject_ids = fields.Many2many('school.subject', string="Subjects")


# --------------------------------------------------------------------

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name = fields.Char(string="Subject Name", required=True)
    student_ids = fields.Many2many('school.management', string="Students")
    teacher_ids = fields.Many2many('school.teacher', string="Teachers")
