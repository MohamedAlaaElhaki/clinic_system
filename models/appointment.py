from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class ClinicAppointment(models.Model):
    """نموذج الموعد - يربط المريض بالطبيب"""
    _name = 'clinic.appointment'
    _description = 'موعد العيادة'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date, appointment_time'
    _rec_name = 'name'
    
    # ==== العلاقات (المرحلة الثانية) ====
    patient_id = fields.Many2one(
        'clinic.patient',
        string='المريض',
        required=True,
        tracking=True,
        ondelete='cascade'
    )
    
    doctor_id = fields.Many2one(
        'clinic.doctor',
        string='الطبيب',
        required=True,
        tracking=True
    )
    
    # ==== معلومات الموعد ====
    name = fields.Char(
        string='رقم الموعد',
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('clinic.appointment') or 'New'
    )
    
    appointment_date = fields.Date(
        string='تاريخ الموعد',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    
    appointment_time = fields.Float(
        string='وقت الموعد',
        required=True,
        help='الوقت بصيغة عشري (9.5 = 9:30)'
    )
    
    duration = fields.Float(
        string='مدة الكشف (ساعات)',
        default=0.5,
        help='مدة الكشف الافتراضية 30 دقيقة'
    )
    
    # ==== حالة الموعد ====
    state = fields.Selection(
        selection=[
            ('draft', 'مسودة'),
            ('confirmed', 'مؤكد'),
            ('in_progress', 'قيد الكشف'),
            ('done', 'منتهي'),
            ('canceled', 'ملغي')
        ],
        string='الحالة',
        default='draft',
        tracking=True,
        copy=False
    )
    
    # ==== معلومات الكشف ====
    reason = fields.Text(
        string='سبب الزيارة',
        required=True
    )
    
    diagnosis = fields.Text(
        string='التشخيص',
        states={'done': [('readonly', True)]}
    )
    
    prescription = fields.Text(
        string='الوصفة الطبية',
        states={'done': [('readonly', True)]}
    )
    
    notes = fields.Text(
        string='ملاحظات إضافية'
    )
    
    # ==== التكاليف ====
    consultation_fee = fields.Float(
        string='أجر الكشف',
        related='doctor_id.consultation_fee',
        readonly=True,
        store=True
    )
    
    paid_amount = fields.Float(
        string='المبلغ المدفوع',
        default=0.0
    )
    
    payment_status = fields.Selection(
        selection=[
            ('not_paid', 'غير مدفوع'),
            ('partial', 'مدفوع جزئياً'),
            ('paid', 'مدفوع بالكامل')
        ],
        string='حالة الدفع',
        default='not_paid',
        compute='_compute_payment_status',
        store=True
    )
    
    # ==== حقول الوقت ====
    checkin_time = fields.Datetime(
        string='وقت الحضور',
        readonly=True
    )
    
    checkout_time = fields.Datetime(
        string='وقت الانتهاء',
        readonly=True
    )
    
    # ==== الحقول المحسوبة ====
    @api.depends('paid_amount', 'consultation_fee')
    def _compute_payment_status(self):
        """حساب حالة الدفع"""
        for appointment in self:
            if appointment.paid_amount <= 0:
                appointment.payment_status = 'not_paid'
            elif appointment.paid_amount >= appointment.consultation_fee:
                appointment.payment_status = 'paid'
            else:
                appointment.payment_status = 'partial'
    
    # ==== القيود (Constraints) ====
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        """التحقق من تاريخ الموعد"""
        for appointment in self:
            if appointment.appointment_date < fields.Date.today():
                raise ValidationError("لا يمكن حجز موعد في تاريخ ماضي!")
    
    @api.constrains('appointment_time')
    def _check_appointment_time(self):
        """التحقق من وقت الموعد"""
        for appointment in self:
            if appointment.appointment_time < 8.0 or appointment.appointment_time > 20.0:
                raise ValidationError("مواعيد العمل من 8 صباحاً إلى 8 مساءً")
    
    # ==== دوال الأعمال (Business Methods) ====
    def action_confirm(self):
        """تأكيد الموعد"""
        for appointment in self:
            if appointment.state == 'draft':
                appointment.state = 'confirmed'
    
    def action_start(self):
        """بدء الكشف"""
        for appointment in self:
            if appointment.state == 'confirmed':
                appointment.state = 'in_progress'
                appointment.checkin_time = fields.Datetime.now()
    
    def action_done(self):
        """إنهاء الكشف"""
        for appointment in self:
            if appointment.state == 'in_progress':
                appointment.state = 'done'
                appointment.checkout_time = fields.Datetime.now()
    
    def action_cancel(self):
        """إلغاء الموعد"""
        for appointment in self:
            if appointment.state in ['draft', 'confirmed']:
                appointment.state = 'canceled'
    
    def action_reset(self):
        """إعادة الموعد لمسودة"""
        for appointment in self:
            if appointment.state == 'canceled':
                appointment.state = 'draft'
    
    # ==== دوال العرض ====
    def name_get(self):
        """تنسيق اسم الموعد"""
        result = []
        for appointment in self:
            name = f'{appointment.name} - {appointment.patient_id.name}'
            if appointment.appointment_date:
                name += f' ({appointment.appointment_date})'
            result.append((appointment.id, name))
        return result