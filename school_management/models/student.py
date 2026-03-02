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

    entry_progress = fields.Integer(string="Entry Progress")
    maximum_rate = fields.Integer(string="Maximum Rate", default=100)

    def action_create_test_student(self):
        return True

    is_minor = fields.Boolean(
        string="Is Minor",
        compute="_compute_is_minor",
        store=False,
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

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 5:
            return {
                'warning': {
                    'title': "Wrong Age",
                    'message': "Student age must be 5 or more."
                }
            }

    _sql_constraints = [
        ('school_management_email_unique', 'unique(email)', 'This email is already in use!')
    ]
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
