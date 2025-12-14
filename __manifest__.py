# _manifest_.py
{
    'name': 'نظام العيادة الطبي',
    'version': '1.0.0',
    'summary': 'إدارة كاملة للعيادات الطبية',
    'category': 'Healthcare',
    'author': 'أنت',
    'depends': ['base', 'mail'],
    
    # أهم جزء: إضافة ملفات XML
    'data': [
        # 1. الشاشات
        'views/patient_views.xml',
        'views/doctor_views.xml', 
        'views/appointment_views.xml',
        
        # 2. القوائم (هتعملها بعد كده)
        # 'views/menu_views.xml',
        
        # 3. الصلاحيات (هتعملها بعد كده)
        # 'security/ir.model.access.csv',
    ],
    
    'installable': True,
    'application': True,
}