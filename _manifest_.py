{
    'name': 'نظام إدارة العيادة',
    'version': '1.0.0',
    'summary': 'نظام متكامل لإدارة العيادات الطبية',
    'description': 'إدارة المرضى، الأطباء، المواعيد، الفواتير',
    'category': 'Healthcare',
    'author': 'Mohamed Alaa',
    'depends': ['base', 'mail'],
    'data': [
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
