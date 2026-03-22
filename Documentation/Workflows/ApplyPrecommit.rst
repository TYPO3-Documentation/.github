.. include:: /Includes.rst.txt

================
Apply Pre-commit
================

The **Apply Pre-commit** workflow runs `pre-commit <https://pre-commit.com>`__
hooks across the entire repository and, if any files are modified, opens a pull
request with the fixes. It is designed to be called on a schedule so that
whitespace and formatting issues are cleaned up automatically.

The workflow only runs in repositories owned by the ``TYPO3-Documentation``
organization.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "python-version", "string", "``3.x``", "Python version used to run pre-commit."
   "pr-title", "string", "``Fix whitespace issues``", "Title of the auto-generated pull request."
   "pr-body", "string", "``This PR automatically applies whitespace fixes.``", "Body text of the auto-generated pull request."

Permissions
-----------

The workflow requires the following permissions in the calling repository:

*  ``contents: write``
*  ``pull-requests: write``

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/apply-precommit.yml

   name: Apply pre-commit fixes
   on:
     schedule:
       - cron: '0 4 * * 1'

   jobs:
     precommit:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-apply-precommit.yml@main
       with:
         python-version: "3.x"
         pr-title: "Fix whitespace issues"
         pr-body: "This PR automatically applies whitespace fixes."

Behavior
--------

1. Pre-commit hooks run with ``--all-files --hook-stage=manual``.
2. If any files are changed, the workflow checks for an existing open PR with
   the same title to avoid duplicates.
3. A new branch ``fix/whitespace-<timestamp>`` is created and pushed.
4. A pull request targeting the triggering branch is opened automatically.
