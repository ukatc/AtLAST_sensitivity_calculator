Input Files and Formats
-----------------------

The :meth:`read_from_file <atlast_sc.utils.FileHelper.read_from_file>` method of
the :class:`FileHelper <atlast_sc.utils.FileHelper>` class can read input data
from a plain-text, `YAML <https://en.wikipedia.org/wiki/YAML>`__,
or `JSON <https://en.wikipedia.org/wiki/JSON>`__ formatted file.
These are described in more detail below.

Plain-text files
^^^^^^^^^^^^^^^^
Plain-text files should have the extension ``.txt`` or ``.TXT``. Each line of
the file should be of the following format:

.. code-block::

    <param-name> = <value> <unit>

An example file might contain the following lines:

.. code-block::

    t_int = 100 s
    bandwidth = 7.5 GHz
    n_pol = 2

.. note::

    - There must a space between ``<value>`` and ``<unit>``.
    - ``<value>`` must be numeric (integer or float).
    - Spaces around "=" are optional.

YAML files
^^^^^^^^^^

YAML files should have the extension ``yaml``, ``yml``, ``YAML``, or ``YML``.

An example YAML file might contain the following:

.. code-block:: yaml


    ---
    t_int: {value: 100, unit: s}
    bandwidth: {value: 7.5, unit: GHz}
    n_pol: {value: 2}


JSON files
^^^^^^^^^^
JSON files should have the extension ``json`` or ``JSON``.

An example JSON file might contain the following:

.. code-block:: json

    {
      "t_int": {
        "value": 100,
        "unit": "s"
      },
      "bandwidth": {
        "value": 7.5,
        "unit": "GHz"
      },
      "n_pol": {
        "value": 2
      }
    }
