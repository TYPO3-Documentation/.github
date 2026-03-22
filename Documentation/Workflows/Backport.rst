.. include:: /Includes.rst.txt

========
Backport
========

The **Backport** workflow automatically creates backport pull requests when a
merged PR carries a matching label (e.g. ``backport v12``).

It uses the `korthout/backport-action <https://github.com/korthout/backport-action>`__
under the hood and is intended to be called from a ``pull_request_target`` event.

Inputs
------

.. csv-table::
   :header: "Input", "Type", "Default", "Description"

   "label_pattern", "string", "``^backport ([^ ]+)$``", "Regex pattern to match backport labels. Must contain a capture group for the target branch."

The capture group in the regex pattern is used as the target branch name. For
example, a label ``backport v12`` with the default pattern ``^backport ([^ ]+)$``
triggers a backport to the ``v12`` branch.

Secrets
-------

.. csv-table::
   :header: "Secret", "Required", "Description"

   "APP_ID", "no", "GitHub App ID for creating backport pull requests"
   "APP_PRIVATE_KEY", "no", "GitHub App private key (PEM format)"

Pull requests created with the default ``GITHUB_TOKEN`` do not trigger CI
workflows on the resulting backport PR. Passing a GitHub App token ensures that
backport PRs trigger their own CI checks (tests, linting, etc.).

If neither secret is provided the workflow falls back to the default
``GITHUB_TOKEN``.

Permissions
-----------

The workflow requires the following permissions in the calling repository:

*  ``contents: write``
*  ``pull-requests: write``

Usage
-----

.. code-block:: yaml
   :caption: .github/workflows/backport.yml

   name: Backport
   on:
     pull_request_target:
       types: [closed]

   jobs:
     backport:
       uses: TYPO3-Documentation/.github/.github/workflows/reusable-backport.yml@main
       with:
         label_pattern: "^backport ([^ ]+)$"
       secrets:
         APP_ID: ${{ secrets.APP_ID }}
         APP_PRIVATE_KEY: ${{ secrets.APP_PRIVATE_KEY }}
