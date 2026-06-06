.. _user-guide:

##########
User guide
##########

Welcome to the ``dcmri`` user guide! Follow these sections to understand how to handle data structures, manage physical units, and model physiological tracking systems.

.. grid:: 1 2 2 3
   :gutter: 3
   :padding: 0
   :class-container: guide-grid

   .. grid-item-card::
      :link: getting_started
      :link-type: doc
      :class-card: guide-card

      🏁 **Getting Started**
      ^^^
      Installation steps, package dependencies, and setting up your first operational environment.

   .. grid-item-card::
      :link: usage
      :link-type: doc
      :class-card: guide-card

      💡 **Usage Overview**
      ^^^
      A bird's-eye view of design patterns, working with data arrays, and basic configuration pipelines.

   .. grid-item-card::
      :link: units
      :link-type: doc
      :class-card: guide-card

      📏 **Units & Dimensions**
      ^^^
      Guidelines on standard physiological units used across inputs (concentrations, time, and volumes).

   .. grid-item-card::
      :link: basics/index
      :link-type: doc
      :class-card: guide-card

      🌱 **Basics**
      ^^^
      Fundamental building blocks of signal processing and basic mathematical routines in ``dcmri``.

   .. grid-item-card::
      :link: tissues/index
      :link-type: doc
      :class-card: guide-card

      🧠 **Tissue Modeling**
      ^^^
      In-depth exploration of specific organ systems, perfusion dynamics, and compartmental workflows.

.. The underlying structured navigation path remains active for sidebars and searching
.. toctree::
   :hidden:
   :maxdepth: 2
   
   getting_started
   usage
   units
   basics/index
   tissues/index