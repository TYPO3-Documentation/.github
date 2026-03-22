.. include:: /Includes.rst.txt

=======================
Documentation Rendering
=======================

The **Documentation Rendering** workflow renders TYPO3 documentation using
either the Python-based ``typo3-docs-theme`` or the Composer-based
``typo3/guides-cli``, depending on which is available in the project.

The workflow automatically detects the rendering tool:

*  If ``composer.json`` contains ``typo3/guides-cli``, Composer dependencies are
   installed and ``vendor/bin/guides`` is used.
*  Otherwise, ``typo3-docs-theme`` is installed via pip and used to render.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "python-version", "string", "``3.12``", "Python version used when rendering via ``typo3-docs-theme``."

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/docs-render.yml

   name: Render documentation
   on: [push, pull_request]

   jobs:
     render:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-docs-render.yml@main
       with:
         python-version: "3.12"
