.. _lexicon:

.. currentmodule:: dcmri

*******
Lexicon
*******

Quantities: dictionaries
------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   all_quantities
   all_groups
   all_tissues
   all_compartments


Quantities: properties
----------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   quantity_desc
   quantity_unit
   quantity_group
   quantity_key
   quantity_dicom
   quantity_osipi


Quantities: operations
----------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   parse_quantity
   modify_quantity
   increment_quantity
   popindex_quantity


Quantities: input / output
--------------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   print_quantities
   quantity_to_json
   quantity_from_json
   quantity_to_csv
   

Sequences: dictionaries
-----------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   all_sequences
   all_contrast_agents


Sequences: properties
---------------------

.. autosummary::
   :toctree: ../api/
   :template: autosummary.rst

   sequence_channels
   sequence_readout_pulses
   sequence_readout_time
   sequence_repetition_time
   sequence_acquisition_times

