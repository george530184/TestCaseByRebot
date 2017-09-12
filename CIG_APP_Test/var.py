# -*- coding: utf-8 -*-
__author__ = 'Jerry'

import os

__all__ =['APP']

PATH = lambda p: os.path.abspath(
	os.path.join(os.path.dirname(__file__), p)
)
APP = PATH('cig_android.apk')