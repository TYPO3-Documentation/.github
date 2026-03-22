.. include:: /Includes.rst.txt

==================
Test Documentation
==================

The **Test Documentation** workflow renders the project documentation inside a
Docker container using the official
`render-guides <https://github.com/TYPO3-Documentation/render-guides>`__ image.
It verifies that documentation builds without warnings and can optionally be
restricted to a specific repository when triggered on a schedule.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "render-flags", "string", "``--no-progress --minimal-test``", "Additional flags passed to ``render-guides`` (e.g. ``--fail-on-log``)."
   "schedule-repository", "string", "``""""``", "Repository name to restrict scheduled runs. Leave empty to always run."

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/test-documentation.yml

   name: Test documentation
   on:
     push:
       branches:
         - main
     pull_request:
     schedule:
       - cron: '0 6 * * 1'

   jobs:
     test-docs:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-test-documentation.yml@main
       with:
         render-flags: "--no-progress --fail-on-log"
         schedule-repository: "TYPO3-Documentation/my-docs"

Schedule Filtering
------------------

When the workflow is triggered via ``schedule``, the ``schedule-repository``
input can limit execution to a single repository. This is useful when a shared
workflow file is inherited by many forks but the scheduled run should only
execute in the upstream repository.
