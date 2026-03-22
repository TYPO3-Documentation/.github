.. include:: /Includes.rst.txt

===========
PHP Quality
===========

The **PHP Quality** workflow runs static analysis tools — PHP CS Fixer, PHPStan,
and optionally XML linting — against a PHP project. Each tool can be toggled on
or off and its invocation command customized.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "php-version", "string", "``8.2``", "PHP version for quality checks."
   "run-cs-fixer", "boolean", "``true``", "Whether to run PHP CS Fixer."
   "cs-fixer-command", "string", "``make test-cs-fixer``", "Command to invoke PHP CS Fixer."
   "run-phpstan", "boolean", "``true``", "Whether to run PHPStan."
   "phpstan-command", "string", "``make test-phpstan``", "Command to invoke PHPStan."
   "run-xml-lint", "boolean", "``false``", "Whether to run XML linting."
   "xml-lint-command", "string", "``make test-xml-lint``", "Command to invoke XML linting."
   "php-extensions", "string", "``""""``", "Space-separated PHP extensions to install."
   "run-environment", "string", "``local``", "Value of the ``RUN_ENVIRONMENT`` env variable passed to each tool."

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/php-quality.yml

   name: PHP Quality
   on: [push, pull_request]

   jobs:
     quality:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-quality.yml@main
       with:
         php-version: "8.2"
         run-cs-fixer: true
         run-phpstan: true
         run-xml-lint: false

Customizing Commands
--------------------

By default the workflow expects ``make`` targets in the consuming repository.
Override the command inputs to use different tooling:

.. code-block:: yaml

   with:
     cs-fixer-command: "vendor/bin/php-cs-fixer fix --dry-run --diff"
     phpstan-command: "vendor/bin/phpstan analyse --no-progress"
