.. _utils:

.. currentmodule:: dcmri
   
*********
Utilities
*********


Lexicon
*******

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   init
   bounds
   select_params


Measurement
***********


.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   fetch
   sample
   add_noise
   mle_rice


Constants
*********


.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   ca_conc
   ca_std_dose
   r2s
   r1
   T1
   T2
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
   deconv
   convmat
   invconvmat


Input functions
***************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   parker
   tristan
   tristan_rat


Digital phantoms
****************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   shepp_logan
   aif
   brain
   tissue
   liver
   kidney
   tissue2scan