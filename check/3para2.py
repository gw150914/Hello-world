#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 23:18:05 2022

@author: yy
"""

import bilby
import numpy as np
import scipy.constants as C
import matplotlib.pyplot as plt

# First set up logging and some output directories and labels
outdir = 'outdir'
label = 'create_your_own_source_model'
sampling_frequency = 4096
duration = 10

c = C.c
G = C.G
M_sun = 2.0 * 10**30
pc = C.parsec
kpc = 1e3 * pc
iota = 30
epsilon = 5e-2
f0 = 1000
Omega0 = 2 * np.pi * f0
R_NS = 1.2e4
M_NS = 2.4 * M_sun
I_3  = 0.2 * 2 * M_NS * R_NS**2
dl   = 1000

tau_gw   = 5. * c**5 / (128. * G * I_3 * epsilon**2 * (2 * np.pi * f0)**4)
print('tau_gw', tau_gw)

def h_waveform(t, epsilon, f0, d, ra, dec, psi, geocent_time):
    
    Omega0 = 2 * np.pi * f0
    dl = d * kpc
    
    Omega = Omega0 * (1 + 128. * G * I_3 * epsilon**2 * Omega0**4 * t / (5 * c**5))**(-0.25)
    arg   = 4 * G * epsilon * I_3 * Omega**2 / (c**4 * dl)
    plus  = arg * np.cos(2 * Omega * t) * 0.5 * (1 + np.cos(iota)**2)
    cross = arg * np.sin(2 * Omega * t) * np.cos(iota)
    return {'plus': plus, 'cross': cross}

injection_parameters = dict(epsilon = epsilon, f0=f0, d=dl, geocent_time=0, ra=0, dec=0, psi=0)
waveform_generator   = bilby.gw.waveform_generator.WaveformGenerator(duration=duration, 
                        sampling_frequency=sampling_frequency, time_domain_source_model=h_waveform)

# Set up interferometers.
ifos = bilby.gw.detector.InterferometerList(['ET'])
ifos.set_strain_data_from_power_spectral_densities(
    sampling_frequency=sampling_frequency, duration=duration,
    start_time=injection_parameters['geocent_time'] +3)
ifos.inject_signal(waveform_generator=waveform_generator,
                   parameters=injection_parameters)


prior = injection_parameters.copy()
prior['epsilon'] = bilby.core.prior.LogUniform(minimum=1e-4, maximum=1e-1, name='epsilon')
prior['f0'] = bilby.core.prior.Uniform(minimum=1e2, maximum = 1e4, name='f0')
prior['d'] = bilby.core.prior.Uniform(minimum = 1e2, maximum = 1e4, name='d')

likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
    interferometers=ifos, waveform_generator=waveform_generator)

result = bilby.core.sampler.run_sampler(
    likelihood, prior, sampler='dynesty', outdir=outdir, label=label,
    resume=False, sample='unif', injection_parameters=injection_parameters)
result.plot_corner()
