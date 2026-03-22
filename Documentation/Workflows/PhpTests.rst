.. include:: /Includes.rst.txt

=========
PHP Tests
=========

The **PHP Tests** workflow runs unit and integration tests across a matrix of
PHP versions. The matrix is defined as a JSON array, allowing callers to test
against any combination of PHP releases.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "php-versions", "string (JSON)", "``[""8.2"", ""8.3"", ""8.4"", ""8.5""]``", "JSON array of PHP versions to test against."
   "dependency-versions", "string", "``locked``", "Composer dependency resolution strategy (``locked``, ``highest``, or ``lowest``)."
   "test-unit-command", "string", "``make test-unit``", "Command to run unit tests. Set empty to skip."
   "test-integration-command", "string", "``""""``", "Command to run integration tests. Leave empty to skip."
   "php-extensions", "string", "``""""``", "Space-separated PHP extensions to install."
   "run-environment", "string", "``local``", "Value of the ``RUN_ENVIRONMENT`` env variable."

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/php-tests.yml

   name: PHP Tests
   on: [push, pull_request]

   jobs:
     tests:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-tests.yml@main
       with:
         php-versions: '["8.2", "8.3", "8.4"]'
         test-unit-command: "make test-unit"
         test-integration-command: "make test-integration"

Matrix Strategy
---------------

The workflow uses ``fail-fast: false`` so that a failure in one PHP version does
not cancel the remaining matrix jobs. This ensures you get a complete picture of
compatibility across all targeted versions.
