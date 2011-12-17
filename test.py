#!/usr/bin/env python
# -*- coding: utf-8 -*-

from units_parser import *
import units


unit1 = 'J/K/mol'
unit2 = 'atm.cm3.K-1.mol-1'

cunit1 = parse_compound_units(unit1)
cunit2 = parse_compound_units(unit2)
print cunit1.conversion(cunit2)
print cunit1.conversion(cunit2) * 8.314
print cunit1.get_dims()
print cunit2.get_dims()
