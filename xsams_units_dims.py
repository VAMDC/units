from units import *

d_wavenumber = Dimensions(L=-1)
d_frequency = Dimensions(T=-1)

xsams_units = {
    #'Threshold': [],
'Temperature': [Dimensions(Theta=1),],
'TotalPressure': [d_pressure,],
'TotalNumberDensity': [Dimensions(L=-3), Dimensions(Q=1,L=-3)],
'PartialPressure': [d_pressure,],
'MoleFraction': [d_dimensionless,],
'Concentration': [Dimensions(L=-3), Dimensions(Q=1,L=-3)],
'Probability': [d_dimensionless,],
    #'NonRadiativeWidth': [],
'TransitionEnergy': [d_energy,],
'TransitionProbabilityA': [Dimensions(T=-1),],
'OscillatorStrength': [d_dimensionless,],
    #'LineStrength': [],
'WeightedOscillatorStrength': [d_dimensionless,],
'Log10WeightedOscillatorStrength': [d_dimensionless,],
    #'IdealisedIntensity': [],
'EffectiveLandeFactor': [d_dimensionless,],
'Wavenumber': [d_wavenumber,],
'Wavelength': [d_length,],
'Energy': [d_energy,],
'Frequency': [d_frequency,],
    #'DielectronicIntensityFactor': [],
    #'CollisionalIntensityFactor': [],
'BranchingRatio': [d_dimensionless,],
# BandCentre and BandWidth may be in wavelength, wavenumber or frequency
'BandCentre': [d_length, d_wavenumber, d_frequency],
'BandWidth': [d_length, d_wavenumber, d_frequency],
'Mass': [d_mass,],
# we allow energies, wavenumbers and frequencies for StateEnergy:
'StateEnergy': [d_energy, d_wavenumber, d_frequency], 
'IonizationEnergy': [d_energy,], 
'LandeFactor': [d_dimensionless,],
'QuantumDefect': [d_dimensionless,],
# NB allow Polarizability in A^2.s^4.kg^-1.m^-1 or "Polarizability Volume", cm3
'Polarizability': [Dimensions(C=2, T=4, M=-1, L=-1), Dimensions(L=3)],
'HyperfineConstantA': [d_energy, d_frequency],
'HyperfineConstantB': [d_energy, d_frequency],
'MolecularWeight': [d_mass,],
'HarmonicFrequency': [d_wavenumber, d_frequency],
    #'Intensity': [],
'ParticleMass': [d_mass,],
'MaterialThickness': [d_length,],
'MaterialTemperature': [Dimensions(Theta=1),],

# these four elements are ReferencedTextType and not DataType, so don't have
# units
'OrdinaryStructuralFormula': [d_dimensionless,],
'ChemicalName': [d_dimensionless,],
'IUPACName': [d_dimensionless,],
'CASRegistryNumber': [d_dimensionless,],
}
