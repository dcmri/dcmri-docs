.. _tissue-types:

************
Tissue types
************

Select a tissue or organ system below to explore its specific tracer kinetic models, transport equations, and perfusion parameters.

.. grid:: 1 1 2 2
   :gutter: 3
   :padding: 0
   :class-container: tissue-grid

   .. grid-item-card::  Tracer Exchange Tissues
      :link: exchange
      :link-type: doc
      :class-card: tissue-card
      :class-title: sd-font-weight-bold

      🔄 **Exchange Tissues**
      ^^^
      General models for capillary-tissue exchange, including single-compartment, 
      two-compartment exchange (2CXM), and adiabatic approximation methods.

   .. grid-item-card::  Liver Kinetics
      :link: liver
      :link-type: doc
      :class-card: tissue-card
      :class-title: sd-font-weight-bold

      🩺 **Liver Models**
      ^^^
      Dual-input perfusion systems tracking blood flow from both the hepatic artery 
      and portal vein, including hepatocytes and biliary excretion functions.

   .. grid-item-card::  Kidney Kinetics
      :link: kidney
      :link-type: doc
      :class-card: tissue-card
      :class-title: sd-font-weight-bold

      🔬 **Kidney Models**
      ^^^
      Renal filtration and transit systems capturing glomerular filtration rate (GFR), 
      tubular dynamics, and plasma clearance parameters.

   .. grid-item-card::  Whole-Body Circulation
      :link: whole_body
      :link-type: doc
      :class-card: tissue-card
      :class-title: sd-font-weight-bold

      🌍 **Whole Body System**
      ^^^
      Closed-loop systemic circulation networks mapping macro-vascular transport, 
      recirculation kinetics, and multi-organ connectivity.

.. Maintain the standard backend document index for Sphinx structure tracking
.. toctree::
   :hidden:
   :maxdepth: 2

   exchange
   liver
   kidney
   whole_body