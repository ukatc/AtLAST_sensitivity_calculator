Outputs Files and Formats
-------------------------

The :meth:`write_to_file <atlast_sc.utils.FileHelper.write_to_file>` method of
the :class:`FileHelper <atlast_sc.utils.FileHelper>` class writes all input
parameters and calculated values to a file of a specified format. The writer
supports plain-text, `YAML <https://en.wikipedia.org/wiki/YAML>`__,
or `JSON <https://en.wikipedia.org/wiki/JSON>`__ formats.

The structure of the output file for a given format is the same as the
input file of the same format, as described in the previous section.
