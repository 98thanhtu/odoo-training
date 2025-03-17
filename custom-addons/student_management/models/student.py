# -*- coding: utf-8 -*-

from odoo import models, fields


class Student(models.Model):
    _name = 'student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    avatar = fields.Binary(string='Avatar', attachment=True)
    address = fields.Char(string='Address')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    date_of_birth = fields.Datetime(string='Date Of Birth', groups="student_management.group_student_manager")
