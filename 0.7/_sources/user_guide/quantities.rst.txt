.. _user-guide-quantities:
 
.. currentmodule:: dcmri
 
Quantities
==========
 
Every quantity that appears in the package, from a model parameter such as a
bolus arrival time to a hyperparameter such as the time step, is identified by
a short text **key**. This section explains how keys are built, how to take
them apart again, and how to look up what a key means.
 
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
 
Any other value is rejected when the key is built. Keys are built with
:func:`quantity_key`:
 
.. code-block:: python
 
    >>> quantity_key('T1')
    'T1'
    >>> quantity_key('T1', roi='gm')
    'T1_gm'
    >>> quantity_key('T1', compartment='e', roi='gm')
    'T1_e_gm'
    >>> quantity_key('F', index=1, compartment='e')
    'F_1_e'
 
The qualifiers have the following meaning.
 
Index
~~~~~
 
A number that distinguishes repeated occurrences of the same quantity, for
example the first and second of two injections. It is placed directly after
the name:
 
.. code-block:: python
 
    >>> quantity_key('BAT', index=2)
    'BAT_2'
 
Compartment
~~~~~~~~~~~
 
A subvoxel compartment the quantity refers to, written with the short
notation of the compartment. The notations are listed by
:func:`all_compartments`:
 
.. code-block:: python
 
    >>> all_compartments()['bl']
    'bile'
    >>> quantity_key('T1', compartment='bl')
    'T1_bl'
 
A parameter that describes the exchange from one compartment to another is
labelled with a paired compartment, written as ``comp1`` + ``2`` + ``comp2``
without underscores, where the ``2`` reads as 'to'. Both parts must be valid
compartment notations. For example, ``b2e`` is the transfer from blood
(``b``) to the extracellular space (``e``):
 
.. code-block:: python
 
    >>> quantity_key('PS', compartment='b2e')
    'PS_b2e'
    >>> parse_quantity('PS_b2e')
    {'name': 'PS', 'index': None, 'compartment': 'b2e', 'roi': None}
 
Region of interest (ROI)
~~~~~~~~~~~~~~~~~~~~~~~~
 
A tissue region the quantity refers to, written with the short notation of
the region. The notations are listed by :func:`all_tissues`:
 
.. code-block:: python
 
    >>> all_tissues()['ao']
    'aorta'
    >>> quantity_key('BAT', roi='ao')
    'BAT_ao'
 
Some notations, such as ``'b'`` for blood, exist as both a compartment and a
region of interest. Which of the two is meant depends on the position in the
key: the ROI always comes last.
 
Invalid qualifiers
~~~~~~~~~~~~~~~~~~
 
A compartment or ROI that is not in the registry raises a ``ValueError`` that
lists the valid options:
 
.. code-block:: python
 
    >>> quantity_key('T1', roi='xyz')
    ValueError: 'xyz' is not a valid roi. Options are [...]
 
 
Taking keys apart
-----------------
 
:func:`parse_quantity` is the inverse of :func:`quantity_key`. It splits a key into its
base name and qualifiers, reading from the end: first a ROI, then a
compartment, then an integer index. Qualifiers that are not present are
returned as ``None``:
 
.. code-block:: python
 
    >>> parse_quantity('T1_e_gm')
    {'name': 'T1', 'index': None, 'compartment': 'e', 'roi': 'gm'}
    >>> parse_quantity('F_1_e')
    {'name': 'F', 'index': 1, 'compartment': 'e', 'roi': None}
 
 
Modifying keys
--------------
 
Three helpers change a key without having to take it apart by hand.
 
:func:`modify_quantity` replaces one or more qualifiers. Qualifiers that are not
provided are kept:
 
.. code-block:: python
 
    >>> modify_quantity('T1_e_gm', roi='ao')
    'T1_e_ao'
    >>> modify_quantity('T1_e', index=2)
    'T1_2_e'
 
:func:`increment_quantity` increases the index by one (or by a chosen amount). A
key without an index gets the index 1:
 
.. code-block:: python
 
    >>> increment_quantity('F_1_e')
    'F_2_e'
    >>> increment_quantity('F_e')
    'F_1_e'
 
:func:`popindex_quantity` removes the index:
 
.. code-block:: python
 
    >>> popindex_quantity('F_2_e')
    'F_e'
 
 
Looking up the description of a key
-----------------------------------
 
:func:`quantity_desc` returns the description dictionary for any key, basic or
derived. For a derived key, it starts from the description of the base
quantity and adapts the descriptive name to the qualifiers. Where
region-specific or compartment-specific initial values and bounds are
available, they replace the defaults:
 
.. code-block:: python
 
    >>> quantity_desc('BAT')['name']
    'bolus arrival time'
    >>> quantity_desc('BAT_ao')['name']
    'bolus arrival time in the aorta'
 
Unknown base names raise a ``ValueError``. The returned dictionary is a copy
and can be modified freely without affecting the registry.
 
Single entries can also be read with dedicated functions, which accept the
same keys:
 
.. code-block:: python
 
    >>> quantity_unit('dose')
    'mL/kg'
    >>> quantity_group('BAT')
    'indicator'
    >>> quantity_osipi('BAT')
    'Q.BA1.001'
    >>> quantity_dicom('dt') is None
    True
 
The function :func:`quantity_osipi` returns the code in the OSIPI CAPLEX lexicon, or ``None``
if the quantity has no code yet.
 
 
Printing quantities
-------------------
 
To print a quantity table in readable form, use :func:`print_quantities`.
The table has one row per quantity, with the columns key, value, unit, name,
group, bounds, DICOM keyword and OSIPI code. Rows are grouped by the group of
the quantity (groups in alphabetical order) and sorted alphabetically by key
within each group.
 
The quantities can be given in three ways: as a set of keys, as a dictionary
that maps keys to values, or as a dictionary that maps keys to complete
quantity descriptions. The value column shows the initial value of the
quantity if only keys are given, and the given value otherwise.
 
Print a table from a set of keys:
 
.. code-block:: python
 
    >>> print_quantities({'dt', 'tmax', 'BAT', 'dose'})
    +------------------------------------------------------------------------------------------------------+
    |                                              Quantities                                              |
    +------+-------+-------+-----------------------------+-----------------+-----------+-------+-----------+
    | Key  | Value | Unit  | Name                        | Group           | Bounds    | DICOM | OSIPI     |
    +------+-------+-------+-----------------------------+-----------------+-----------+-------+-----------+
    | dt   | 0.5   | sec   | pseudo-continuous time step | hyperparameters |           |       |           |
    | tmax | 240   | sec   | maximum time point          | hyperparameters |           |       |           |
    +------+-------+-------+-----------------------------+-----------------+-----------+-------+-----------+
    | BAT  | 30    | sec   | bolus arrival time          | indicator       | (-30, 30) |       | Q.BA1.001 |
    | dose | 0.1   | mL/kg | contrast agent dose         | indicator       | (0, 0.2)  |       |           |
    +------------------------------------------------------------------------------------------------------+
 
Give the table a title (the default title is ``Quantities``):
 
.. code-block:: python
 
    >>> print_quantities({'BAT', 'bdel', 'dose'}, title='Indicator quantities')
    +------------------------------------------------------------------------------------------------------+
    |                                         Indicator quantities                                         |
    +------+-------+-------+-----------------------------+-----------------+-----------+-------+-----------+
    | Key  | Value | Unit  | Name                        | Group           | Bounds    | DICOM | OSIPI     |
    +------+-------+-------+-----------------------------+-----------------+-----------+-------+-----------+
    | BAT  | 30    | sec   | bolus arrival time          | indicator       | (-30, 30) |       | Q.BA1.001 |
    | bdel | 30    | sec   | delay in a double injection | indicator       | (-30, 30) |       |           |
    | dose | 0.1   | mL/kg | contrast agent dose         | indicator       | (0, 0.2)  |       |           |
    +------------------------------------------------------------------------------------------------------+
 
Pass a dictionary to show your own values next to the descriptions, for
instance the result of a fit:
 
.. code-block:: python
 
    >>> values = {'BAT': 12.3456, 'dose': 0.1234, 'tmax': 240}
    >>> print_quantities(values, title='Fitted values')
    +------------------------------------------------------------------------------------------------+
    |                                         Fitted values                                          |
    +------+---------+-------+---------------------+-----------------+-----------+-------+-----------+
    | Key  | Value   | Unit  | Name                | Group           | Bounds    | DICOM | OSIPI     |
    +------+---------+-------+---------------------+-----------------+-----------+-------+-----------+
    | tmax | 240     | sec   | maximum time point  | hyperparameters |           |       |           |
    +------+---------+-------+---------------------+-----------------+-----------+-------+-----------+
    | BAT  | 12.3456 | sec   | bolus arrival time  | indicator       | (-30, 30) |       | Q.BA1.001 |
    | dose | 0.1234  | mL/kg | contrast agent dose | indicator       | (0, 0.2)  |       |           |
    +------------------------------------------------------------------------------------------------+
 
Round the numbers to a number of decimal places:
 
.. code-block:: python
 
    >>> print_quantities(values, title='Fitted values', decimals=2)
    +----------------------------------------------------------------------------------------------+
    |                                        Fitted values                                         |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | Key  | Value | Unit  | Name                | Group           | Bounds    | DICOM | OSIPI     |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | tmax | 240   | sec   | maximum time point  | hyperparameters |           |       |           |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | BAT  | 12.35 | sec   | bolus arrival time  | indicator       | (-30, 30) |       | Q.BA1.001 |
    | dose | 0.12  | mL/kg | contrast agent dose | indicator       | (0, 0.2)  |       |           |
    +----------------------------------------------------------------------------------------------+
 
or to a number of significant digits:
 
.. code-block:: python
 
    >>> print_quantities(values, title='Fitted values', digits=3)
    +----------------------------------------------------------------------------------------------+
    |                                        Fitted values                                         |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | Key  | Value | Unit  | Name                | Group           | Bounds    | DICOM | OSIPI     |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | tmax | 240.0 | sec   | maximum time point  | hyperparameters |           |       |           |
    +------+-------+-------+---------------------+-----------------+-----------+-------+-----------+
    | BAT  | 12.3  | sec   | bolus arrival time  | indicator       | (-30, 30) |       | Q.BA1.001 |
    | dose | 0.123 | mL/kg | contrast agent dose | indicator       | (0, 0.2)  |       |           |
    +----------------------------------------------------------------------------------------------+
 
If both ``decimals`` and ``digits`` are given, ``decimals`` is used. Arrays
and dictionaries are not printed in full: an array is shown as its shape, for
example ``array (3, 3)``, and a dictionary as its number of entries.
 
To print the quantities as Python code instead of a table, use
``as_dict=True``. The output is a dictionary assignment that can be copied
into a script. The entries are grouped by quantity group, with the group as a
comment, sorted alphabetically by key within each group, and the unit as a
trailing comment. All three input forms are accepted. Nothing is returned.
 
.. code-block:: python
 
    >>> print_quantities({'dt', 'tmax', 'BAT', 'dose'}, as_dict=True)
    p = {
        # hyperparameters
        'dt': 0.5,    # sec
        'tmax': 240,  # sec
 
        # indicator
        'BAT': 30,    # sec
        'dose': 0.1,  # mL/kg
    }
 
With a dictionary of values, the printed code contains those values:
 
.. code-block:: python
 
    >>> print_quantities(values, as_dict=True)
    p = {
        # hyperparameters
        'tmax': 240,     # sec
 
        # indicator
        'BAT': 12.3456,  # sec
        'dose': 0.1234,  # mL/kg
    }
 
In this mode ``title``, ``decimals`` and ``digits`` have no effect, and the
values are printed as they are.
 
 
Saving and loading quantities
-----------------------------
 
Dictionaries of quantity values, keyed by quantity keys, can be written to
JSON files. The JSON format supports nested dictionaries and numpy arrays,
which are restored when the file is read back:
 
.. code-block:: python
 
    >>> values = {'dt': 0.5, 'tmax': 240}
    >>> quantity_to_json('params.json', values)
    >>> quantity_from_json('params.json')
    {'dt': 0.5, 'tmax': 240}
 
A flat dictionary of scalar values can also be saved to a two-column CSV file
(``key``, ``value``). Nested values and arrays are not supported in this
format and raise a ``TypeError``:
 
.. code-block:: python
 
    >>> quantity_to_csv('params.csv', values)
 
Note that a CSV file stores all values as text, so numbers are not converted
back to numbers automatically when the file is read with another tool.
 
 
Summary
-------
 
* A basic quantity is identified by a key and defined by a dictionary with its
  initial value, bounds, name, unit, group and its DICOM and OSIPI
  equivalents.
* A derived key has the form ``name[_index][_compartment][_roi]`` and is built
  with :func:`quantity_key`.
* :func:`parse_quantity`, :func:`modify_quantity`, :func:`increment_quantity` and
  :func:`popindex_quantity` take keys apart and change them.
* :func:`quantity_desc` and its shortcuts (:func:`quantity_unit`, :func:`quantity_group`,
  :func:`quantity_osipi`, :func:`quantity_dicom`) return the description of any key.
* :func:`print_quantities` prints quantities as a table or as copy-paste code.
* Names and codes follow the OSIPI CAPLEX lexicon wherever possible.
 