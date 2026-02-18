from odoo import models, api,fields

class Hospital(models.Model):
    _name = 'hospital.management'
    _description = 'hospital.management'
    patient_id = fields.Many2one('res.partner',string = 'Patient')
    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    address = fields.Text()
    age = fields.Integer()
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')])
    is_admit = fields.Boolean(default = True)
    emergency_id = fields.One2many('hospital.emergency','hospital_id', string = 'Emergency')
    file = fields.Binary()
    image = fields.Image()
    def action_open_emergency_wizard(self):
        return {
            'name': 'Create Emergency',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.emergency.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_hospital_id': self.id,
            }
        }


class HospitalEmergency(models.Model):
    _name = 'hospital.emergency'
    _description = 'hospital.emergency'
    hospital_id = fields.Many2one('hospital.management',string = 'Hospital')
    date = fields.Date()
    reason = fields.Char(string = 'Reason for Emergency')

class HospitalEmergencyWizards(models.TransientModel):
    _name = 'hospital.emergency.wizard'
    _description = 'hospital.emergency.wizard'
    hospital_id = fields.Many2one('hospital.management',string = 'Hospital')
    date = fields.Date()
    reason = fields.Char(string = 'Reason for Emergency')

    def create_emergency(self):
        self.env['hospital.emergency'].create({
            'hospital_id': self.hospital_id.id,
            'date': self.date,
            'reason': self.reason,
        })
