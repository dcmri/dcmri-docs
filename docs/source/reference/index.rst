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

   .. grid-item-card:: Core
      :link: core
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-primary sd-text-white sd-font-weight-bold

      ⚙️ **core**
      ^^^
      Core classes for dcmri

   .. grid-item-card:: Lexicon
      :link: lexicon
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-secondary sd-text-white sd-font-weight-bold

      📖 **lexicon**
      ^^^
      Nomenclature for dcmri quantities

   .. grid-item-card:: Inverse Models
      :link: e2e
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-success sd-text-white sd-font-weight-bold

      ⏪ **e2e**
      ^^^
      Inverse signal models.

   .. grid-item-card:: Forward Models
      :link: forward
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-info sd-text-white sd-font-weight-bold

      ⏩ **forward**
      ^^^
      Forward signal models.

   .. grid-item-card:: Tracer Kinetics
      :link: kinetics
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-warning sd-text-dark sd-font-weight-bold

      ⏳ **kinetics**
      ^^^
      Compartment systems and tracer exchange dynamics.

   .. grid-item-card:: Relaxivity
      :link: relaxivity
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-danger sd-text-white sd-font-weight-bold

      🧲 **relaxivity**
      ^^^
      Conversion formulas between concentration and R1/R2.

   .. grid-item-card:: Bloch Equations
      :link: bloch
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: sd-bg-dark sd-text-white sd-font-weight-bold

      🌀 **bloch**
      ^^^
      Magnetization dynamics under MRI pulse sequences.

   .. grid-item-card:: Signal
      :link: signal
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: dcmri-bg-teal sd-text-white sd-font-weight-bold

      📈 **signal**
      ^^^
      MRI signal equations and sequence simulations.

   .. grid-item-card:: Inverse Problems
      :link: inverse
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: dcmri-bg-purple sd-text-white sd-font-weight-bold

      🔄 **inverse**
      ^^^
      Optimization, parameter estimation, and fitting routines.

   .. grid-item-card:: Utilities
      :link: utils
      :link-type: doc
      :text-align: center
      :class-card: reference-card
      :class-title: dcmri-bg-pink sd-text-white sd-font-weight-bold

      🛠️ **utils**
      ^^^
      Helper functions, array manipulation, and validation tracking.

.. Hiding the actual toctree so Sphinx still builds the pages structural pathways,
   but doesn't print out the boring duplicate list on the page.
.. toctree::
   :hidden:

   core
   lexicon
   e2e
   forward
   kinetics
   relaxivity
   bloch
   signal
   inverse
   utils