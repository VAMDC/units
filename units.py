# -*- coding: utf-8 -*-
import sys
from collections import Counter

si_unit_stems = (u'm', u's', u'g', u'mol', u'K', u'cd', u'A')

class SIPrefix(object):
    def __init__(self, prefix, name, power):
        self.prefix = prefix
        self.name = name
        self.power = power
        self.fac = 10**power
si_prefixes = { u'f': SIPrefix(u'f', 'femto', -15),
                u'p': SIPrefix(u'p', 'pico', -12),
                u'n': SIPrefix(u'n', 'nano', -9),
                u'μ': SIPrefix(u'μ', 'micro', -6),
                u'm': SIPrefix(u'm', 'milli', -3),
                u'c': SIPrefix(u'c', 'centi', -2),
                u'd': SIPrefix(u'd', 'deci', -1),
                u'k': SIPrefix(u'k', 'kilo', 3),
                u'M': SIPrefix(u'M', 'mega', 6),
                u'G': SIPrefix(u'G', 'giga', 9),
                u'T': SIPrefix(u'T', 'tera', 12),
              }

class BaseUnit(object):
    def __init__(self, stem, name, unit_type, fac, description, latex, dims=None):
        self.stem = stem
        self.name = name
        self.unit_type = unit_type
        self.fac = fac
        self.description = description
        self.latex = latex
        self.dims = dims
    def __str__(self):
        return self.stem

class AtomUnit(object):
    def __init__(self, prefix, base_unit, exponent=1):
        self.prefix = prefix
        self.si_prefix = si_prefixes.get(prefix)
        self.base_unit = base_unit
        self.exponent = exponent

        self.si_fac = 1.
        if self.si_prefix:
            self.si_fac = self.si_prefix.fac
        self.si_fac = (self.si_fac * self.base_unit.fac) ** self.exponent

        self.dims = self.base_unit.dims ** self.exponent

    def __pow__(self, power):
        return AtomUnit(self.prefix, self.base_unit, self.exponent * power)

    def __str__(self):
        return unicode((self.prefix, unicode(self.base_unit), self.exponent))

class CompoundUnit(object):
    def __init__(self, atom_units):
        self.atom_units = atom_units
        self.dims = self.get_dims()

    def get_dims(self):
        dims = Dimensions()
        for atom_unit in self.atom_units:
            dims *= atom_unit.dims
        return dims

    def __mul__(self, other_atom):
        atom_units = self.atom_units
        atom_units.append(other_atom)
        return CompoundUnit(atom_units)

    def __div__(self, other_atom):
        atom_units = self.atom_units
        atom_units.append(other_atom**-1)
        return CompoundUnit(atom_units)

    def __str__(self):
        return u'.'.join([unicode(atom_unit) for atom_unit in self.atom_units])

    def to_si(self):
        fac = 1.
        for atom_unit in self.atom_units:
            fac *= atom_unit.si_fac
        return fac

    def conversion(self, other):
        return self.to_si() / other.to_si()
            
class Dimensions(object):
    # these are the abbreviations for Length, Mass, Time, Temperature,
    # Quantity (amount of substance), Current, and Luminous Intensity:
    dim_names = ['L', 'M', 'T', 'Theta', 'Q', 'C', 'I']
    dim_index = {}
    for i, dim_name in enumerate(dim_names):
        dim_index[dim_name] = i

    def __init__(self, dims=None, **kwargs):
        self.dims = [0]*7
        if dims:
            # initialize by dims array
            if not kwargs:
                self.dims = dims
            else:
                print 'bad initialisation of Dimensions object'
                sys.exit(1)
        else:
            # initialize by keyword arguments
            for dim_name in kwargs:
                self.dims[self.dim_index[dim_name]] = kwargs[dim_name]

    def __mul__(self, other):
        new_dims = []
        for i, dim in enumerate(self.dims):
            new_dims.append(dim + other.dims[i])
        return Dimensions(tuple(new_dims))

    def __div__(self, other):
        new_dims = []
        for i, dim in enumerate(self.dims):
            new_dims.append(dim - other.dims[i])
        return Dimensions(tuple(new_dims))

    def __pow__(self, pow):
        new_dims = []
        for dim in self.dims:
            new_dims.append(dim * pow)
        return Dimensions(tuple(new_dims))

    def __str__(self):
        s_dims = []
        for i, dim_name in enumerate(self.dim_names):
            if self.dims[i] != 0:
                this_s_dim = dim_name
                if self.dims[i] != 1:
                    this_s_dim += '%d' % self.dims[i]
                s_dims.append(this_s_dim)
        if len(s_dims) == 0:
            return '[dimensionless]'
        return '.'.join(s_dims)

d_dimensionless = Dimensions()
d_length = Dimensions(L=1)
d_area = d_length**2
d_volume = d_length**3
d_time = Dimensions(T=1)
d_mass = Dimensions(M=1)
d_energy = Dimensions(M=1, L=2, T=-2)
d_force = d_mass * d_length / d_time**2
d_pressure = d_force / d_area
d_charge = Dimensions(C=1) * Dimensions(T=1)
d_voltage = d_energy / d_charge     # 1 V = 1 J/C
d_magfield_strength = d_voltage * d_time / d_area   # 1 T = 1 Vs/m^2

base_units = [

BaseUnit('1', 'unity', 'unity', 1., '', '1', d_dimensionless),

BaseUnit('m', 'metre', 'length', 1., '', 'm', d_length),
BaseUnit('s', 'second', 'time', 1., '', 's', d_time),
BaseUnit('g', 'gram', 'mass', 1.e-3, '', 'g', d_mass),
BaseUnit('K', 'kelvin', 'temperature', 1., '', 'K', Dimensions(Theta=1)),
BaseUnit('mol', 'mole', 'amount', 1., '', 'mol', Dimensions(Q=1)),
BaseUnit('N', 'newton', 'force', 1., '', 'N', d_force),
BaseUnit('J', 'joule', 'energy', 1., '', 'J', d_energy),
BaseUnit('W', 'watt', 'power', 1., '', 'W', d_energy / d_time),
BaseUnit('Pa', 'pascal', 'pressure', 1., '', 'Pa', d_pressure),
BaseUnit('C', 'coulomb', 'charge', 1., '', 'C', d_charge),
BaseUnit('V', 'volt', 'voltage', 1., '', 'V', d_voltage),
BaseUnit('T', 'tesla', 'magnetic field strength', 1., '', 'T', d_magfield_strength),
BaseUnit('Hz', 'hertz', 'cyclic frequency', 1., '', 'Hz', d_time**-1),

# Dimensionless units
BaseUnit('deg', 'degree', 'angle', 1., '', 'deg', d_dimensionless),
BaseUnit('rad', 'radian', 'angle', 1., '', 'rad', d_dimensionless),
BaseUnit('sr', 'steradian', 'solid angle', 1., '', 'sr', d_dimensionless),

# Non-SI pressure units
BaseUnit('bar', 'bar', 'pressure', 1.e5, '', 'bar', d_pressure),
BaseUnit('atm', 'atmosphere', 'pressure', 1.01325e5, '', 'atm', d_pressure),
BaseUnit('Torr', 'torr', 'pressure', 133.322368, '', 'Torr', d_pressure),
# (but see e.g. Wikipedia for the precise relationship between Torr and mmHg
BaseUnit('mmHg', 'millimetres of mercury', 'pressure', 133.322368, '', 'mmHg', d_pressure),

# Non-SI force units
BaseUnit('dyn', 'dyne', 'force', 1.e-5, '', 'dyn', d_force),
# Energy units
BaseUnit('erg', 'erg', 'energy', 1.e-7, '', 'erg', d_energy),
BaseUnit('eV', 'electron volt', 'energy',  1.602176487e-19, '', 'eV', d_energy),
BaseUnit('Eh', 'hartree', 'energy', 4.35974394e-18, '', 'E_h', d_energy),
BaseUnit('cal', 'thermodynamic calorie', 'energy', 4.184, '', 'cal', d_energy),
BaseUnit('Ry', 'rydberg', 'energy', 13.60569253 * 1.602176487e-19, '', 'Ry', d_energy),

# Non-SI mass units
BaseUnit('u', 'atomic mass unit', 'mass', 1.660538921e-27, '', 'u', d_mass),
BaseUnit('amu', 'atomic mass unit', 'mass', 1.660538921e-27, '', 'amu', d_mass),
BaseUnit('me', 'electron mass', 'mass', 9.10938291e-31, '', 'm_e', d_mass),

# Non-SI length units
BaseUnit(u'Å', 'angstrom', 'length', 1.e-10, '', '\AA', d_length),
BaseUnit('a0', 'bohr radius', 'length', 5.2917721092e-11, '', 'a_0', d_length),

# Non-SI area units
BaseUnit('b', 'barn', 'area', 1.e-28, '', 'b', d_area),

# Non-SI volume units
BaseUnit('l', 'litre', 'volume', 1.e-3, '', 'l', d_volume),

# Non-SI time units
BaseUnit('min', 'minute', 'time', 60., '', 'min', d_time),
BaseUnit('hr', 'hour', 'time', 3600., '', 'hr', d_time),
BaseUnit('h', 'h', 'time', 3600., '', 'h', d_time),
BaseUnit('d', 'day', 'time', 86400., '', 'd', d_time),

]

base_unit_stems = {}
#all_units = []
for base_unit in base_units:
    base_unit_stems[base_unit.stem] = base_unit
    #for prefix in si_prefixes.keys():
        #unit = ''.join([prefix, base_unit.stem])
        #unit = prefix +  base_unit.stem
        #all_units.append(unit)
        #base_unit_stems.append(base_unit.stem)
        #print unit,
    #print

# any duplicate units?
#y = Counter(all_units)
#print [i for i in y if y[i]>1]
