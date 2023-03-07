##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    'name': 'Facebook Server Side Tracking',
    'summary': 'Server side tracking',
    'author': "lumitec GmbH",
    'website': "https://www.lumitec.solutions",
    'category': 'Extra Tools',
    'version': '15.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'base',
        'web',
        'website',
        'crm',
    ],
    'data': [
        'data/defaults.xml',
        'views/res_config_settings.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
