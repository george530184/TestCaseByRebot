# -*- coding: utf-8 -*-
__author__ = 'Jerry'

import os

CLOUD_URL = 'www.cigwifi.net'

__all__ =['ret']

ret = os.system('ping -c 4 %s' % CLOUD_URL)