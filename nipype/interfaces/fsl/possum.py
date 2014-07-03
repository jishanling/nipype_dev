#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# @Author: oesteban - code@oscaresteban.es
# @Date:   2014-07-03 15:27:53
# @Last Modified by:   oesteban
# @Last Modified time: 2014-07-03 16:26:09
"""
The possum module provides classes for interfacing with `POSSUM
<http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/POSSUM>`_ command line tools.
Please, check out the link for pertinent citations using POSSUM.

.. Note:: This was written to work with FSL version 5.0.6.

    Change directory to provide relative paths for doctests
    >>> import os
    >>> filepath = os.path.dirname( os.path.realpath( __file__ ) )
    >>> datadir = os.path.realpath(os.path.join(filepath, '../../testing/data'))
    >>> os.chdir(datadir)

"""

import os
import shutil
import warnings

from nipype.interfaces.fsl.base import FSLCommand, FSLCommandInputSpec, Info
from nipype.interfaces.base import (TraitedSpec, isdefined, File, Directory,
                                    InputMultiPath, OutputMultiPath, traits)
from nipype.utils.filemanip import fname_presuffix, split_filename, copyfile


class B0CalcInputSpec(FSLCommandInputSpec):
    in_file = File(exists=True, mandatory=True, argstr='-i %s', position=0,
                   desc='filename of input image (usually a tissue/air segmentation)')
    out_file = File(argstr='-o %s', position=1, name_source=['in_file'],
                    name_template='%s_b0field', output_name='out_file',
                    desc='filename of B0 output volume')


    x_grad = traits.Float(0.0, argstr='--gx=%0.4f', desc=('Value for zeroth-order x-gradient field '
                          '(per mm)'))
    y_grad = traits.Float(0.0, argstr='--gy=%0.4f', desc=('Value for zeroth-order y-gradient field '
                          '(per mm)'))
    z_grad = traits.Float(0.0, argstr='--gz=%0.4f', desc=('Value for zeroth-order z-gradient field '
                          '(per mm)'))

    x_b0 = traits.Float(0.0, argstr='--b0x=%0.2f', desc=('Value for zeroth-order b0 field '
                        '(x-component), in Tesla'))
    y_b0 = traits.Float(0.0, argstr='--b0y=%0.2f', desc=('Value for zeroth-order b0 field '
                        '(y-component), in Tesla'))
    z_b0 = traits.Float(1.0, argstr='--b0=%0.2f', desc=('Value for zeroth-order b0 field '
                        '(z-component), in Tesla'))

    delta = traits.Float(-9.45e-6, argstr='-d %e', desc='Delta value (chi_tissue - chi_air)')
    chi_air = traits.Float(4.0e-7, argstr='--chi0=%e', desc='susceptibility of air')
    compute_xyz = traits.Bool(False, argstr='--xyz',
                              desc='calculate and save all 3 field components (i.e. x,y,z)')
    extendboundary = traits.Float(1.0, argstr='--extendboundary=%0.2f', desc=('Relative proportion to '
                                  'extend voxels at boundary'))
    directconv = traits.Bool(False, argstr='--directconv',
                             desc='use direct (image space) convolution, not FFT')


class B0CalcOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='filename of B0 output volume')


class B0Calc(FSLCommand):
    """
    B0 inhomogeneities occur at interfaces of materials with different magnetic susceptibilities,
    such as tissue-air interfaces. These differences lead to distortion in the local magnetic field,
    as Maxwell’s equations need to be satisfied. An example of B0 inhomogneity is the first volume
    of the 4D volume ```$FSLDIR/data/possum/b0_ppm.nii.gz```.

    Examples ::

    >>> from nipype.interfaces.fsl import B0Calc
    >>> b0calc = B0Calc()
    >>> b0calc.inputs.in_file = 'tissue+air_map.nii'
    >>> b0calc.inputs.z_b0 = 3.0
    >>> b0calc.cmdline
    'b0calc -i tissue+air_map.nii -o tissue+air_map_b0field.nii.gz --b0=3.00'

    """

    _cmd = 'b0calc'
    input_spec = B0CalcInputSpec
    output_spec = B0CalcOutputSpec


