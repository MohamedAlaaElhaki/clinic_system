# في data/demo_data.py (أنشئ الملف)
from odoo import fields, models, api

def _create_sequences(self):
    """إنشاء تسلسل للمواعيد"""
    sequence_data = {
        'name': 'Appointment Sequence',
        'code': 'clinic.appointment',
        'prefix': 'APT/%(year)s/',
        'padding': 5,
        'company_id': False,
    }
    
    if not self.env['ir.sequence'].search([('code', '=', 'clinic.appointment')]):
        self.env['ir.sequence'].create(sequence_data)