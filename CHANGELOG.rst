=========
Changelog
=========

Version 0.1
===========

- Initial development.
- 2021-02-10
  - Added options to `pycarta.hyperthought.schema.load`
    - `strict`: Only data that matches the requirements of a schema element are
      read. Overrides force.
    - `force`: Read data into the most viable container. If all fail, read only
      valid data.
    - If neither `strict` nor `force` are True, then attempt to use a variant
      of the best schema, but do not reread with only valid data.
