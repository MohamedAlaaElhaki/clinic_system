{
    'name': 'نظام إدارة العيادة',
    'version': '1.0.0',
    'summary': 'نظام متكامل لإدارة العيادات الطبية',
    'category': 'Healthcare',
    'author': 'Mohamed Alaa',
    'depends': ['base', 'mail'],
    'data': [
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/menu_views.xml',  # ← أضفنا القوائم
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
