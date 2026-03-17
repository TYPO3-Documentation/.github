.. include:: /Includes.rst.txt

========================================
TYPO3 Documentation — Shared Workflows
========================================

.. contents:: Table of Contents
   :depth: 2
   :local:

Introduction
============

This repository provides shared reusable GitHub Actions workflows for the
`TYPO3 Documentation <https://github.com/TYPO3-Documentation>`__ organization.

By centralizing workflow definitions, documentation repositories benefit from:

*  **Single point of maintenance** — Action versions and configurations are
   updated in one place.
*  **Consistent behavior** — All repositories that adopt these workflows
   behave identically.
*  **Reduced boilerplate** — Calling repos need only a few lines of YAML
   instead of duplicating entire job definitions.

.. toctree::
   :caption: Workflows
   :titlesonly:

   Workflows/Backport
   Workflows/TestDocumentation
   Workflows/ApplyPrecommit
   Workflows/PhpQuality
   Workflows/PhpTests
   Workflows/PhpCommand
   Workflows/DocsRender

.. toctree::
   :caption: Architecture Decisions
   :titlesonly:

   Decisions/Index

Migration Guide
===============

To migrate an existing inline workflow to a shared reusable workflow:

1. Identify which shared workflow matches your current inline job.
2. Replace the ``jobs:`` section with a ``uses:`` call to the shared workflow.
3. Pass any required inputs via ``with:``.
4. Remove inline ``permissions:``, ``steps:``, and ``runs-on:`` — these are
   defined in the shared workflow.

.. code-block:: yaml
   :caption: Example: Migrating backport workflow

   # Before (inline)
   jobs:
     backport:
       if: github.event.pull_request.merged == true
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@...
         - uses: korthout/backport-action@...

   # After (shared)
   jobs:
     backport:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-backport.yml@main
