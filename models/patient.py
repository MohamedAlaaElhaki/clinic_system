from odoo.exceptions import ValidationError
from odoo import models, fields, api 
from odoo .exceptions import ValidationError

class ClinicPatient(models.Model):
    """نموذج المريض - المستوى الأول"""
    _name = 'clinic.patient'
    _description = 'مريض العيادة'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    
    # ==== الحقول الأساسية ====
    name = fields.Char(
        string='الاسم بالكامل',
        required=True,
        tracking=True,
        help='اسم المريض الثلاثي'
    )
    
    # المعلومات الشخصية
    birth_date = fields.Date(
        string='تاريخ الميلاد',
        tracking=True
    )
    
    age = fields.Integer(
        string='العمر',
        compute='_compute_age',
        store=False,
        help='يتم حسابه تلقائياً من تاريخ الميلاد'
    )
    
    gender = fields.Selection(
        selection=[
            ('male', 'ذكر'),
            ('female', 'أنثى'),
            ('other', 'أخرى')
        ],
        string='الجنس',
        default='male',
        tracking=True
    )
    
    national_id = fields.Char(
        string='رقم البطاقة',
        size=14,
        tracking=True,
        help='الرقم القومي ١٤ رقم'
    )
    
    # ==== معلومات الاتصال ====
    phone = fields.Char(
        string='رقم الهاتف',
        required=True,
        tracking=True
    )
    
    mobile = fields.Char(
        string='رقم المحمول',
        tracking=True
    )
    
    email = fields.Char(
        string='البريد الإلكتروني'
    )
    
    address = fields.Text(
        string='العنوان'
    )
    
    # ==== المعلومات الطبية ====
    blood_type = fields.Selection(
        selection=[
            ('a_plus', 'A+'),
            ('a_minus', 'A-'),
            ('b_plus', 'B+'),
            ('b_minus', 'B-'),
            ('ab_plus', 'AB+'),
            ('ab_minus', 'AB-'),
            ('o_plus', 'O+'),
            ('o_minus', 'O-')
        ],
        string='فصيلة الدم'
    )
    
    medical_history = fields.Text(
        string='التاريخ المرضي',
        help='الأمراض المزمنة، الحساسيات، العمليات السابقة'
    )
    
    # ==== الحقول المحسوبة ====
    @api.depends('birth_date')
    def _compute_age(self):
        """حساب العمر من تاريخ الميلاد"""
        today = fields.Date.today()
        for patient in self:
            if patient.birth_date:
                age = today.year - patient.birth_date.year
                # تصحيح إذا عيد الميلاد لم يأت بعد هذا العام
                if (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day):
                    age -= 1
                patient.age = age
            else:
                patient.age = 0
    
    # ==== دوال مساعدة ====
    def name_get(self):
        """تنسيق عرض اسم المريض"""
        result = []
        for patient in self:
            name = patient.name
            if patient.phone:
                name = f'{name} - {patient.phone}'
            result.append((patient.id, name))
        return result
    # في نهاية class ClinicPatient في patient.py أضف:

    # ==== العلاقات (المرحلة الثالثة) ====
    appointment_ids = fields.One2many(
        'clinic.appointment',  # ← دلوقتي موجود!
        'patient_id',
        string='المواعيد'
    )
    
    # إحصاءات
    appointment_count = fields.Integer(
        string='عدد المواعيد',
        compute='_compute_appointment_count',
        store=False
    )
    
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        """حساب عدد مواعيد المريض"""
        for patient in self:
            patient.appointment_count = len(patient.appointment_ids)