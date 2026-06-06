.. _reference-guide:

#########
Reference
#########

This reference manual details all functions included in ``dcmri``, describing 
what they are and what they do. 

.. grid:: 1 2 3 3
   :gutter: 3
   :padding: 0
   :class-container: reference-grid

   .. grid-item-card:: End-to-End Models
      :link: e2e
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-primary sd-text-white sd-font-weight-bold

      🚀 **e2e**
      ^^^
      Complete tissue and organ pipeline models.

   .. grid-item-card:: Tracer Kinetics
      :link: kinetics
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-secondary sd-text-white sd-font-weight-bold

      ⏳ **kinetics**
      ^^^
      Compartment systems and tracer exchange dynamics.

   .. grid-item-card:: Relaxivity
      :link: relaxivity
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-success sd-text-white sd-font-weight-bold

      🧲 **relaxivity**
      ^^^
      Conversion formulas between concentration and R1/R2.

   .. grid-item-card:: Bloch Equations
      :link: bloch
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-info sd-text-white sd-font-weight-bold

      📊 **bloch**
      ^^^
      MRI signal equations and sequence simulations.

   .. grid-item-card:: Inverse Problems
      :link: inverse
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-warning sd-text-dark sd-font-weight-bold

      🔄 **inverse**
      ^^^
      Optimization, parameter estimation, and fitting routines.

   .. grid-item-card:: Utilities
      :link: utils
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-dark sd-text-white sd-font-weight-bold

      🛠️ **utils**
      ^^^
      Helper functions, array manipulation, and validation tracking.

.. Hiding the actual toctree so Sphinx still builds the pages structural pathways,
   but doesn't print out the boring duplicate list on the page.
.. toctree::
   :hidden:

   e2e
   kinetics
   relaxivity
   bloch
   inverse
   utils