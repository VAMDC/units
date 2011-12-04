# -*- coding: utf-8 -*-
# units_parser.py

# Christian Hill, 28/11/2011
#
# The units_parser module, which provides some methods for manipulating
# physical units:

import units
from pyparsing import Word, Group, Literal, Suppress, ParseException, oneOf, Optional
import codecs

class UnitsError(Exception):
    def __init__(self, error_str):
        self.error_str = error_str
    def __str__(self):
        return self.error_str

class UnitAtom(object):
    def __init__(self, ustring):
        pre = None
        if len(ustring) > 1:
            pre, post = ustring[0], ustring[1:]
        else:
            post = ustring
        

caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowers = caps.lower()
letters = u'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
digits = u'1234567890'
exponent = Word(digits + '-')
prefix = oneOf(units.si_prefixes.keys())
ustem = Word(letters + u'Å')
uatom = (Group( u'1' | (Optional(prefix) + ustem)) + Optional(exponent)) | (Group( u'1' | ustem) + Optional(exponent))

def parse_unit_atom(unit_atom):
    #print '  ',unit_atom,
    try:
        uatom_data = uatom.parseString(unit_atom)
    except ParseException:
        raise
        raise UnitsError("Invalid unit atom syntax: %s" % unit_atom)
    if len(uatom_data[0]) == 1:
        prefix = None; stem = uatom_data[0][0]
    else:
        prefix = uatom_data[0][0]; stem = uatom_data[0][1]
        if stem not in units.base_unit_stems:
            prefix = None; stem = ''.join(uatom_data[0])
    try:
        base_unit = units.base_unit_stems[stem]
    except:
        raise UnitsError("Unrecognised unit: %s" % unit_atom)
    exponent = 1
    if len(uatom_data) == 2:
        exponent = int(uatom_data[1])

    #print prefix, stem, exponent
    return units.AtomUnit(prefix, base_unit, exponent)

def parse_mult_units(munit):
    atom_units = []
    for s_unit in munit.split('.'):
        atom_unit = parse_unit_atom(s_unit)
        if atom_unit.base_unit.stem != '1':
            # the unity 'unit' is not really a unit
            atom_units.append(atom_unit)
    return units.CompoundUnit(atom_units)

def parse_compound_units(cunit):
    print cunit
    dims = units.Dimensions()
    div_fields = cunit.split('/')
    ndiv_fields = len(div_fields)
    compound_unit = parse_mult_units(div_fields[0])
    for div_field in div_fields[1:]:
        compound_unit = compound_unit / parse_unit_atom(div_field)
    return compound_unit

parse_unit_atom('cm3')
parse_unit_atom('nmol')
parse_unit_atom('Mmol')
parse_unit_atom('mmHg')
#parse_unit_atom('pDa')
parse_unit_atom('s-1')
parse_unit_atom(u'μs')
parse_unit_atom(u'Å')
parse_unit_atom(u'mÅ-1')

tests = ['cm/s-1/K2', '1/atm/cm']
tests = []
for line in codecs.open('xsams_units.txt', 'r', encoding='utf-8'):
    tests.append(line.strip())
for test in tests:
    compound_unit = parse_compound_units(test)
    #print test,':',compound_unit,'conversion to SI:', compound_unit.to_si()
    print test,':',compound_unit,'dimensions:', compound_unit.dims

compound_unit1 = parse_compound_units('cm-1/atm')
compound_unit2 = parse_compound_units('cm-1/Pa')
compound_unit3 = parse_compound_units('1/m/Torr')
compound_unit1 = parse_compound_units('Torr')
compound_unit2 = parse_compound_units('mbar')

print compound_unit1,'to',compound_unit2,':', compound_unit1.conversion(compound_unit2)
