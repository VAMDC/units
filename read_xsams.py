#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from units_parser import *
from units import *
from xsams_units_dims import *
from xml.dom.minidom import parse


xsams_name = '/Users/christian/Downloads/HIT-2011-10-03T20_35_44.539109.xsams'
xsams_file = os.path.join('/Users/christian/Downloads', xsams_name)

dom = parse(xsams_file)

d_wavenumber = units.Dimensions
for elm in dom.getElementsByTagName("Value"):
    tagName = elm.parentNode.tagName
    if tagName == 'FitParameter':
        # don't check FitParameters... yet
        continue
    if tagName == 'LineshapeParameter':
        # don't check LineshapeParameters... yet
        continue
    attr = elm.getAttribute('units')
    if attr == 'unitless' or attr == '':
        unit = None
        dims = d_dimensionless
    else:
        unit = parse_compound_units(attr)
        dims = unit.get_dims()
    ok = False
    for dim in xsams_units[tagName]:
        #print 'Comparing',dims,'with',dim,':',dims == dim
        if dims == dim:
            ok = True
            #print 'OK:',unit,dims
            break
    if not ok:
        print 'Eek!',unit,dims,' should be in',\
                    ''.join([str(x) for x in xsams_units[tagName]])


