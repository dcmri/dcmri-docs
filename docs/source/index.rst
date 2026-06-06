:title: Home
:orphan:
:html_theme.sidebar_secondary.remove:

.. container:: landing-header-hero

   .. grid:: 1 1 2 2
      :gutter: 3
      :padding: 0
      :class-container: align-items-center

      .. grid-item:: :columns: 12 12 4 4
         :class: text-center

         .. image:: _static/dcmri-logo.png
            :width: 240px

      .. grid-item:: :columns: 12 12 8 8

         .. raw:: html

            <h1 class="display-3 text-primary font-weight-bold" style="margin-bottom: 0.2rem; border-bottom: none;">dcmri</h1>
            <p class="lead text-muted font-italic" style="font-size: 1.4rem; letter-spacing: 0.5px;">
               A python toolbox for dynamic contrast MRI
            </p>

.. grid:: 1 1 2 2
   :gutter: 3
   :padding: 0
   :class-container: landing-hero

   .. grid-item:: :columns: 12
      
      .. admonition:: Mission
         :class: dropdown, note
         
         To simplify the analysis of dynamic-contrast MRI data, 
         and the development and distribution of methods.

.. rubric:: Getting Started

.. grid:: 1 3 3 3
   :gutter: 3
   :padding: 0
   :class-container: action-cards

   .. grid-item-card::
      :link: user_guide/index
      :link-type: doc
      :class-card: action-card sd-bg-light
      :text-align: center

      📖
      
      **User Guide**
      ^^^
      Background on basic concepts, physics, and mathematical derivations.

   .. grid-item-card::
      :link: reference/index
      :link-type: doc
      :class-card: action-card sd-bg-light
      :text-align: center

      ⚙️
      
      **Reference Guide**
      ^^^
      Find a suitable method, function, or class model and dive straight in.

   .. grid-item-card::
      :link: examples/index
      :link-type: doc
      :class-card: action-card sd-bg-light
      :text-align: center

      💻
      
      **Examples Gallery**
      ^^^
      A library of real-world examples applying methods to concrete questions.

---

.. rubric:: Features

.. grid:: 1 2 3 3
   :gutter: 3
   :padding: 0
   :class-container: feature-grid

   .. grid-item-card::
      :link: e2e
      :link-type: ref

      🏥 **Tissue Bank**
      ^^^
      An intuitive user interface to quickly analyze data across different biological structures and organ pipelines.

   .. grid-item-card:: 
      :link: bloch
      :link-type: ref

      🧲 **Signal & Bloch**
      ^^^
      Pre-built Bloch mathematical equations for common MRI imaging sequences and signal tracking simulations.

   .. grid-item-card::
      :link: kinetics
      :link-type: ref

      ⏳ **Tracer Kinetics**
      ^^^
      Basic pharmacokinetic building blocks, including multi-compartment systems and transit models.

   .. grid-item-card::
      :link: real-data
      :link-type: ref

      📊 **Data Libraries**
      ^^^
      Built-in access to real data, synthetic profiles, and simulated images to make comparative validation effortless.

   .. grid-item-card:: 
      :link: convolution-functions
      :link-type: ref

      🛠️ **Mathematical Utilities**
      ^^^
      Optimized helper functions tracking common input functions, constants, data sampling, and fast convolutions.

   .. grid-item-card::
      :link: releases/index
      :link-type: doc

      🚀 **Releases & Updates**
      ^^^
      Track package changes, operational updates, deprecations, and newly integrated features over time.

---

.. rubric:: About

.. grid:: 1 1 3 3
   :gutter: 4
   :padding: 0
   :class-container: metadata-footer

   .. grid-item-card:: 📜 Citing dcmri
      :class-card: metadata-card

      When you use ``dcmri`` in your research, please cite:
      
      .. code-block:: text

         Ebony Gunwhy, Eve Shalom and Steven Sourbron. 
         dcmri: an open-source python package for dynamic contrast MRI. 
         European Society of Magnetic Resonance in Medicine and Biology 
         (Barcelona, Spain), pp 491, Oct 2024.

   .. grid-item-card:: 🔓 License
      :class-card: metadata-card

      ``dcmri`` is distributed under the `Apache 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_ license.
      
      A permissive, free license that allows users to freely use, modify, and distribute the software with minimal restrictions.

   .. grid-item-card:: 👥 About
      :link: about/index
      :link-type: doc
      :class-card: metadata-card

      Learn more about the ``dcmri`` project background.
      
      Find out about our core mission objectives, meet the community contributors, or learn how you can get involved with code development.

.. Master tracking tree remains active implicitly
.. toctree::
   :maxdepth: 2
   :hidden:
   
   user_guide/index
   reference/index
   examples/index
   releases/index
   about/index