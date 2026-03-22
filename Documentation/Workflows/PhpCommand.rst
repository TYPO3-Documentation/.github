.. include:: /Includes.rst.txt

===========
PHP Command
===========

The **PHP Command** workflow is a generic building block that sets up PHP,
installs Composer dependencies, and runs a single arbitrary command. It is useful
for one-off tasks that do not fit the specialized quality or test workflows —
for example generating API documentation, running database migrations, or
executing custom scripts.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "php-version", "string", "``8.2``", "PHP version to install."
   "command", "string", "*(required)*", "Command to run after ``composer install``."
   "php-extensions", "string", "``""""``", "Space-separated PHP extensions to install."
   "composer-args", "string", "``--no-interaction --no-progress --prefer-dist``", "Arguments passed to ``composer install``."
   "run-environment", "string", "``local``", "Value of the ``RUN_ENVIRONMENT`` env variable."

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/generate-docs.yml

   name: Generate API docs
   on: [push]

   jobs:
     generate:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-command.yml@main
       with:
         php-version: "8.3"
         command: "vendor/bin/generate-api-docs"

Custom Composer Arguments
-------------------------

Override the default Composer arguments when you need dev dependencies or a
different install strategy:

.. code-block:: yaml

   with:
     command: "vendor/bin/rector process --dry-run"
     composer-args: "--no-interaction --no-progress"
