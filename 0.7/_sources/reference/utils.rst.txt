.. _utils:

.. currentmodule:: dcmri
   
*********
Utilities
*********


Constants
*********


.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   ca_conc
   ca_std_dose
   r2s
   r2sq
   r1
   T1
   T2
   T2s
   PD
   perfusion

Convolution
***********

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conv
   stepconv
   expconv
   biexpconv
   nexpconv

Deconvolution
*************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   deconv
   convmat
   invconvmat

Data
****

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   fetch
   clear_cache
   load_minipig
   load_kruk
   load_tristan_rats
   load_tristan_humans


Measurement
***********

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   sample
   add_noise
   mle_rice
   describe


Digital reference objects
*************************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   shepp_logan