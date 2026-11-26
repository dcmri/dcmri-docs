.. _user-guide-quantities:

.. currentmodule:: dcmri

Quantities
==========

Every quantity that appears in the package, from a model parameter such as a
bolus arrival time to a hyperparameter such as the time step, is identified by
a short text **key**. Keys are handled with the class :class:`Qty`, which
builds a key from its parts, takes a key apart again, and looks up what it
means. This section explains how.

All naming conventions follow the `OSIPI CAPLEX lexicon
<https://osipi.github.io/OSIPI_CAPLEX/>`_ as closely as possible. Where a
quantity has an OSIPI code, it is stored with the quantity, so that results can
be related to the community standard.


Basic quantities
----------------

A *basic quantity* is a quantity that is registered in the package under a
plain key, such as ``'dt'``, ``'tmax'``, ``'dose'`` or ``'BAT'``. The
registry maps each key to a dictionary that fully defines the quantity:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Entry
     - Meaning
   * - ``init``
     - Default initial value.
   * - ``bounds``
     - Lower and upper bounds for fitting, or ``None`` if the quantity is not
       fitted.
   * - ``bounds_type``
     - Present for some quantities only. For example ``'add'`` means that the
       bounds are applied relative to the initial value.
   * - ``name``
     - Descriptive name.
   * - ``unit``
     - Unit of measurement, or ``None`` if the quantity has no unit.
   * - ``group``
     - Category the quantity belongs to, such as ``'indicator'`` or
       ``'hyperparameters'``.
   * - ``dicom_key``
     - Corresponding DICOM keyword, or ``None``.
   * - ``osipi_key``
     - Corresponding OSIPI code, or ``None``.

The full registry is returned by :func:`all_quantities`. It is a dictionary keyed
by the quantity keys:

.. code-block:: python

    >>> quantities = all_quantities()
    >>> list(quantities)[:3]
    ['dt', 'tmax', 'agent']
    >>> quantities['dt']
    {'init': 0.5, 'bounds': None, 'name': 'pseudo-continuous time step',
     'unit': 'sec', 'group': 'hyperparameters', 'dicom_key': None,
     'osipi_key': None}

Each quantity belongs to exactly one group. The available groups are returned
by :func:`all_groups`:

.. code-block:: python

    >>> sorted(all_groups())
    ['electromagnetic', 'hyperparameters', 'indicator', 'inverse problem',
     'physiological', 'sequence', 'signal', 'whole-body']


Derived keys
------------

The same physical quantity often occurs several times in a model, for
instance in different tissues, in different compartments of a tissue, or in
repeated form (a first and a second bolus). Instead of registering all
these variants, the package builds *derived keys* from a basic key by adding
qualifiers. A derived key has the form

.. code-block:: text

    name[_index][_compartment][_roi]

where every part in square brackets is optional. The underscore is the
separator between the parts of a name, which is how a key can be taken apart
again unambiguously. The qualifiers are also restricted to a fixed
vocabulary:

* the compartment must be one of the notations returned by
  :func:`all_compartments`,
* the ROI must be one of the notations returned by :func:`all_tissues`.

Any other value is rejected when the :class:`Qty` is created.

A :class:`Qty` is created from the parts of a key, and its attribute
:attr:`~Qty.key` returns the full key:

.. code-block:: python

    >>> Qty(name='T1').key
    'T1'
    >>> Qty(name='T1', roi='gm').key
    'T1_gm'
    >>> Qty(name='T1', compartment='e', roi='gm').key
    'T1_e_gm'
    >>> Qty(name='F', index=1, compartment='e').key
    'F_1_e'

The qualifiers have the following meaning.

Index
~~~~~

A number that distinguishes repeated occurrences of the same quantity, for
example the first and second of two injections. It is placed directly after
the name:

.. code-block:: python

    >>> Qty(name='BAT', index=2).key
    'BAT_2'

Compartment
~~~~~~~~~~~

A subvoxel compartment the quantity refers to, written with the short
notation of the compartment. The notations are listed by
:func:`all_compartments`:

.. code-block:: python

    >>> all_compartments()['bl']
    'bile'
    >>> Qty(name='T1', compartment='bl').key
    'T1_bl'

A parameter that describes the exchange from one compartment to another is
labelled with a paired compartment, written as ``comp1`` + ``2`` + ``comp2``
without underscores, where the ``2`` reads as 'to'. Both parts must be valid
compartment notations. For example, ``b2e`` is the transfer from blood
(``b``) to the extracellular space (``e``):

.. code-block:: python

    >>> Qty(name='PS', compartment='b2e').key
    'PS_b2e'

Region of interest (ROI)
~~~~~~~~~~~~~~~~~~~~~~~~

A tissue region the quantity refers to, written with the short notation of
the region. The notations are listed by :func:`all_tissues`:

.. code-block:: python

    >>> all_tissues()['ao']
    'aorta'
    >>> Qty(name='BAT', roi='ao').key
    'BAT_ao'

Some notations, such as ``'b'`` for blood, exist as both a compartment and a
region of interest. Which of the two is meant depends on the position in the
key: the ROI always comes last.

Invalid qualifiers
~~~~~~~~~~~~~~~~~~

A compartment or ROI that is not in the registry raises a ``ValueError`` that
lists the valid options:

.. code-block:: python

    >>> Qty(name='T1', roi='xyz')
    ValueError: 'xyz' is not a valid roi. Options are [...]


Taking keys apart
-----------------

Pass a full key as the first argument to split it into its parts. The key is
read from the end: first a ROI, then a compartment, then an integer index.
Parts that are not present are ``None``:

.. code-block:: python

    >>> q = Qty('T1_e_gm')
    >>> q.name, q.index, q.compartment, q.roi
    ('T1', None, 'e', 'gm')
    >>> q = Qty('F_1_e')
    >>> q.name, q.index, q.compartment, q.roi
    ('F', 1, 'e', None)

A key and explicit parts can be combined. Parts that are given explicitly
override the ones read from the key:

.. code-block:: python

    >>> Qty('T1_e_gm', roi='ao').key
    'T1_e_ao'


Modifying keys
--------------

A :class:`Qty` can be changed after it has been created. The methods below
change the object in place and return it, so calls can be chained.

:meth:`~Qty.set` replaces one or more of the index, compartment and ROI.
Arguments that are not provided are kept:

.. code-block:: python

    >>> Qty('T1_e_gm').set(roi='ao').key
    'T1_e_ao'
    >>> Qty('T1_e').set(index=2).key
    'T1_2_e'

:meth:`~Qty.increment` increases the index by one (or by a chosen amount). A
quantity without an index gets the index 1:

.. code-block:: python

    >>> Qty('F_1_e').increment().key
    'F_2_e'
    >>> Qty('F_e').increment().key
    'F_1_e'

:meth:`~Qty.popindex` removes the index:

.. code-block:: python

    >>> Qty('F_2_e').popindex().key
    'F_e'

Because these methods modify the object, make a new :class:`Qty` if you need
to keep the original.


Looking up the description of a key
-----------------------------------

A :class:`Qty` gives access to the definition of its quantity through
attributes, for basic and derived keys alike. For a derived key, the
description is based on that of the base quantity and adapted to the
qualifiers. Where region-specific or compartment-specific initial values and
bounds are available, they replace the defaults:

.. code-block:: python

    >>> Qty('BAT').desc
    'bolus arrival time'
    >>> Qty('BAT_ao').desc
    'bolus arrival time in the aorta'

The available attributes are:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Attribute
     - Meaning
   * - :attr:`~Qty.value`
     - Default initial value.
   * - :attr:`~Qty.bounds`
     - Lower and upper bounds, or ``None``.
   * - :attr:`~Qty.unit`
     - Unit of measurement, or ``None``.
   * - :attr:`~Qty.group`
     - Group the quantity belongs to.
   * - :attr:`~Qty.desc`
     - Descriptive name.
   * - :attr:`~Qty.dicom`
     - Corresponding DICOM keyword, or ``None``.
   * - :attr:`~Qty.osipi`
     - Corresponding code in the OSIPI CAPLEX lexicon, or ``None`` if the
       quantity has no code yet.

.. code-block:: python

    >>> Qty('dose').unit
    'mL/kg'
    >>> Qty('BAT').group
    'indicator'
    >>> Qty('BAT').osipi
    'Q.BA1.001'
    >>> Qty('dt').dicom is None
    True

An unknown base name raises a ``ValueError`` when the description is looked
up. Quantities that are not in the registry can be supplied through the
``quantities`` argument, a dictionary in the same format:

.. code-block:: python

    >>> extra = {'myparam': {'init': 1.0, 'bounds': (0, 10), 'name': 'my parameter',
    ...                      'unit': 'sec', 'group': 'physiological',
    ...                      'dicom_key': None, 'osipi_key': None}}
    >>> Qty('myparam', quantities=extra).unit
    'sec'


Summary
-------

* A basic quantity is identified by a key and defined by a dictionary in the
  registry (:func:`all_quantities`) with its initial value, bounds, name, unit,
  group and its DICOM and OSIPI equivalents.
* A derived key has the form ``name[_index][_compartment][_roi]``. A
  :class:`Qty` builds it from its parts (:attr:`~Qty.key`) and takes it apart
  again.
* :meth:`~Qty.set`, :meth:`~Qty.increment` and :meth:`~Qty.popindex` change a
  :class:`Qty` in place.
* The attributes :attr:`~Qty.value`, :attr:`~Qty.bounds`, :attr:`~Qty.unit`,
  :attr:`~Qty.group`, :attr:`~Qty.desc`, :attr:`~Qty.dicom` and
  :attr:`~Qty.osipi` return the description of any key.
* :func:`print_quantities` prints quantities as a table or as copy-paste code.
* Names and codes follow the OSIPI CAPLEX lexicon wherever possible.