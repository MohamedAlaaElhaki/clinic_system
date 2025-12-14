from odoo.exceptions import ValidationError
from odoo import models, fields, api
from odoo .exceptions import ValidationError

class ClinicDoctor(models.Model):
    """نموذج الطبيب - المستوى الأول"""
    _name = 'clinic.doctor'
    _description = 'طبيب العيادة'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # ==== المعلومات الأساسية ====
    name = fields.Char(
        string='اسم الطبيب',
        required=True,
        tracking=True
    )
    
    medical_id = fields.Char(
        string='رقم الرخصة الطبية',
        required=True,
        tracking=True
    )
    
    specialty = fields.Selection(
        selection=[
            ('general', 'طب عام'),
            ('pediatric', 'أطفال'),
            ('surgery', 'جراحة'),
            ('orthopedic', 'عظام'),
            ('dental', 'أسنان'),
            ('dermatology', 'جلدية'),
            ('ophthalmology', 'عيون'),
            ('cardiology', 'قلب'),
            ('gynecology', 'نساء وتوليد'),
            ('other', 'تخصص آخر')
        ],
        string='التخصص',
        default='general',
        required=True
    )
    
    other_specialty = fields.Char(
        string='التخصص (إذا أخرى)'
    )
    
    # ==== معلومات الاتصال ====
    phone = fields.Char(
        string='هاتف العيادة',
        required=True
    )
    
    mobile = fields.Char(
        string='هاتف محمول'
    )
    
    email = fields.Char(
        string='البريد الإلكتروني'
    )
    
    # ==== المعلومات المهنية ====
    consultation_fee = fields.Float(
        string='أجر الكشف',
        default=100.0,
        digits=(10, 2)
    )
    
    experience_years = fields.Integer(
        string='سنوات الخبرة'
    )
    
    qualification = fields.Text(
        string='المؤهلات العلمية'
    )
    
    is_active = fields.Boolean(
        string='نشط',
        default=True,
        help='الطبيب يقبل حالياً مرضى جدد'
    )
    
    # ==== الصورة والتوقيع ====
    image = fields.Binary(
        string='صورة الطبيب',
        attachment=True
    )
    
    signature = fields.Binary(
        string='التوقيع',
        attachment=True,
        help='توقيع الطبيب للروشتات'
    )
    
    # ==== دوال خاصة ====
    @api.constrains('medical_id')
    def _check_medical_id(self):
        """التحقق من رقم الرخصة الطبية"""
        for doctor in self:
            if doctor.medical_id and not doctor.medical_id.isdigit():
                raise ValidationError("رقم الرخصة الطبية يجب أن يكون أرقام فقط")
    # في نهاية class ClinicDoctor في doctor.py أضف:

    # ==== العلاقات (المرحلة الثالثة) ====
    appointment_ids = fields.One2many(
        'clinic.appointment',  # ← دلوقتي موجود!
        'doctor_id',
        string='المواعيد'
    )
    
    # إحصاءات
    appointment_count = fields.Integer(
        string='عدد المواعيد',
        compute='_compute_appointment_count',
        store=False
    )
    
    upcoming_appointments = fields.Integer(
        string='مواعيد قادمة',
        compute='_compute_upcoming_appointments',
        store=False
    )
    
    @api.depends('appointment_ids', 'appointment_ids.state')
    def _compute_appointment_count(self):
        """حساب عدد مواعيد الدكتور"""
        for doctor in self:
            doctor.appointment_count = len(doctor.appointment_ids)
    
    @api.depends('appointment_ids', 'appointment_ids.state', 'appointment_ids.appointment_date')
    def _compute_upcoming_appointments(self):
        """حساب المواعيد القادمة"""
        today = fields.Date.today()
        for doctor in self:
            upcoming = doctor.appointment_ids.filtered(
                lambda a: a.state in ['draft', 'confirmed'] and 
                         a.appointment_date >= today
            )
            doctor.upcoming_appointments = len(upcoming)        