.. _lexicon:

.. currentmodule:: dcmri

*******
Lexicon
*******

Quantities: definition
----------------------

.. list-table::
   :widths: 30 70

   * - :doc:`quantities`
     - All quantities with their key, default value, unit, name, group,
       bounds and DICOM/OSIPI keys.

.. autosummary::
   :toctree: ../api/
   :template: custom-data-template.rst

   QUANTITIES
   GROUPS
   ROIS
   COMPS


Quantities: functions
---------------------

.. autosummary::
   :toctree: ../api/
   :template: custom-class-template.rst
   :recursive:

   unit
   group
   get_quantity
   build_varname
   parse_varname
   extend_varname
   increment_varindex
   remove_varindex
   print_quantities
   select_params
   

Sequences
---------

.. autosummary::
   :toctree: ../api/
   :template: custom-class-template.rst
   :recursive:

   SEQUENCES
   AGENTS
