.. _bloch:
.. currentmodule:: dcmri
   
**************
Magnetization
**************


Magnetization - modules
***********************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   Magnetization
   MxyReadMz
   MzPrep
   MzInflowPrep


Tissue properties
*****************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   WaterExchangeGeneric
   WaterExchangeArtery
   WaterExchangeKidney
   WaterExchangeLiver
   WaterExchangeTissueX


Sequences: properties
*********************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   sequence_channels
   sequence_readout_pulses
   sequence_readout_time
   sequence_repetition_time
   sequence_acquisition_times


Sequences: magnetization
************************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   Mz_ss_vectorized
   Mz_ss_spgr_vectorized
   Mz_ss_pr_spgr_vectorized
   Mz_ss_k0_pr_spgr_vectorized
   Mz_ss_spgri_vectorized
   Mz_prop_vectorized
   Mz_prop_spgr_vectorized
   Mz_prop_pr_spgr_vectorized


Dynamic sequences: magnetization (k-space center)
*************************************************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   Mz_wrapper_k0
   Mz_dyn_k0_spgr
   Mz_dyn_k0_pr_spgr
   Mz_dyn_ss_k0_pr_spgr
   Mz_dyn_ss_k0_spgr
   Mz_dyn_ss_k0_spgri
   Mz_dyn_k0_se
   Mz_dyn_k0
   Mz_dyn_ss_k0
   
   
Dynamic sequences: magnetization (all k-space)
**********************************************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   Mz_wrapper_k_all
   Mz_dyn_spgr
   Mz_dyn_pr_spgr
   Mz_dyn_ss_pr_spgr
   Mz_dyn_ss_spgr
   Mz_dyn_se
   Mz_dyn_ss_spgri
   Mz_dyn
   Mz_dyn_ss
   



