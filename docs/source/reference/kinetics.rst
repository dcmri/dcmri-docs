.. _kinetics:
.. currentmodule:: dcmri
   
*********************
Tracer-kinetic models
*********************

A library of functions for specific models, and a set of configurable 
wrapper functions.


Wrapper functions
*****************

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   ConcAorta
   ConcLiver
   ConcKidney
   ConcCortMed
   ConcTissueX
   FluxTissueX


Building blocks
***************

Components for constructing more complex kinetic models.

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc
   flux


Pass
----

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_pass
   flux_pass
   res_pass
   prop_pass
   
Trap
----

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_trap
   flux_trap
   res_trap
   prop_trap

Compartment
-----------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_comp
   flux_comp
   res_comp
   prop_comp


Plug flow
---------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_plug
   flux_plug
   res_plug
   prop_plug

Bi-compartment
--------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_bicomp
   flux_bicomp

Step
----

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_step
   flux_step
   res_step
   prop_step

Chain
-----

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_chain
   flux_chain
   res_chain
   prop_chain


Plug-flow compartment
---------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   flux_pfcomp

Two-compartment exchange
------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_2cxm
   flux_2cxm

Free
----

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_free
   flux_free
   res_free
   prop_free

Multicompartment
----------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_ncomp
   flux_ncomp
   res_ncomp
   prop_ncomp

Non-stationary compartment
--------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_nscomp
   flux_nscomp
   

Michaelis-Menten compartment
----------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_mmcomp
   flux_mmcomp



Exchange tissues
****************

Concentrations and flux in vascular-interstitial tissues with bidirectional exchange.

Uptake
------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_u
   flux_tissue_u

Fast exchange
-------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_fx
   flux_tissue_fx

No exchange
-----------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_nx
   conc_tissue_nxp
   flux_tissue_nx
   flux_tissue_nxp

Weakly vascularized
-------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_wv
   flux_tissue_wv

High flow
---------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_hf
   flux_tissue_hf

High flow uptake
----------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_hfu
   flux_tissue_hfu

Two-compartment uptake
----------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_tissue_2cu
   flux_tissue_2cu

Two-compartment exchange
------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst
   
   conc_tissue_2cx
   flux_tissue_2cx

Liver
*****

Single-inlet extracellular
--------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_1i_ec_d
   conc_liver_1i_ec

Single-inlet intracellular
--------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_1i_ic
   conc_liver_1i_ic_hf
   conc_liver_1i_ic_hfd
   conc_liver_1i_ic_hfdu

Single-inlet intracellular (non-stationary)
-------------------------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_1i_ic__u
   conc_liver_1i_ic__e
   conc_liver_1i_ic__ue
   conc_liver_1i_ic_hf__u
   conc_liver_1i_ic_hf__e
   conc_liver_1i_ic_hf__ue
   conc_liver_1i_ic_hfd__u
   conc_liver_1i_ic_hfd__e
   conc_liver_1i_ic_hfd__ue
   conc_liver_1i_ic_hfdu__u

Dual-inlet extracellular
------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_2i_ec_hf
   conc_liver_2i_ec

Dual-inlet intracellular
------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_2i_ic
   conc_liver_2i_ic_hf
   conc_liver_2i_ic_u
   
Dual-inlet intracellular (non-stationary)
-----------------------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_liver_2i_ic__e
   conc_liver_2i_ic__u
   conc_liver_2i_ic__ue
   conc_liver_2i_ic_hf__e
   conc_liver_2i_ic_hf__u
   conc_liver_2i_ic_hf__ue
   conc_liver_2i_ic_u__u


Kidney
******

Parenchymal
-----------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_kidney_2cf
   conc_kidney_2pf
   conc_kidney_cpf
   conc_kidney_2cfu
   conc_kidney_2pfu
   conc_kidney_hf
   conc_kidney_hfu
   conc_kidney_fn


Cortico-medullary
-----------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   conc_kidney_cm9


Aorta
*****

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   flux_aorta
   flux_aorta_hlo
   flux_aorta_hlol
   flux_aorta_hlok


Sources
*******

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   ca_injection