.. _kinetics:
.. currentmodule:: dcmri
   
*********************
Tracer-kinetic models
*********************

A library of functions for specific models, and a set of configurable 
wrapper functions.

.. grid:: 1 2 3 3
   :gutter: 3
   :padding: 2
   :class-container: text-center

   .. card:: Wrapper Functions
      :link: kinetics/wrappers
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      ⚙️
      ^^^
      Configurable, high-level wrapper interfaces for organs and whole tissues.

   .. card:: Building Blocks
      :link: kinetics/building_blocks
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      🧱
      ^^^
      Elementary components, paths, and mathematical systems for custom models.

   .. card:: Exchange Tissues
      :link: kinetics/exchange_tissues
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      🔄
      ^^^
      Vascular-interstitial tracer models featuring bidirectional exchange.

   .. card:: Liver Models
      :link: kinetics/liver
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      🧪
      ^^^
      Single and dual-inlet models spanning extracellular and intracellular spaces.

   .. card:: Kidney Models
      :link: kinetics/kidney
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      🧬
      ^^^
      Parenchymal and dedicated cortico-medullary structural models.

   .. card:: Aorta Models
      :link: kinetics/aorta
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      ❤️
      ^^^
      Tracer flux dynamics across specialized aortic pathways.

   .. card:: Sources
      :link: kinetics/sources
      :link-type: doc
      :shadow: md
      :class-header: bg-light font-weight-bold

      💉
      ^^^
      Tracer delivery, injections, and blood input profile generators.

.. Hiding the sub-pages from visual menus but making Sphinx aware of them:

.. toctree::
   :hidden:

   kinetics/wrappers
   kinetics/building_blocks
   kinetics/exchange_tissues
   kinetics/liver
   kinetics/kidney
   kinetics/aorta
   kinetics/sources