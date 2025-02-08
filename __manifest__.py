# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "GameRun Sign-up Approval",
    'version': '18.0.1.0',
    'category': "Website",
    'summary': "GameRun Multi-Sport Facility Booking System",
    'description': """
GameRun Multi-Sport Facility Booking System
    """,
    'website': 'https://www.gamerun.ai',
    'depends': ['base', 'auth_signup', 'sh_signup_email_approval'],
    'data': [
        'data/ir_cron.xml',
        'data/mail_templates.xml',
        'views/signup_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'assets': {
        'web.assets_backend': [
        ],
    },
    'license': 'LGPL-3',
}
