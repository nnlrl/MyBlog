#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author    : nnlrl
# Created   : 2021/11/04
# Title     : var.py
# Objective :


import contextvars

aio_databases = contextvars.ContextVar('databases')
redis_var = contextvars.ContextVar('redis')
