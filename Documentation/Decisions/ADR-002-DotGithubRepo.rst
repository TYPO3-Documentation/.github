.. include:: /Includes.rst.txt

============================================
ADR-002: Use .github Repo for Shared Workflows
============================================

Status
======
Accepted (supersedes initial placement in t3docs-ci-deploy)

Context
=======
The shared reusable workflows were initially placed in
``TYPO3-Documentation/t3docs-ci-deploy`` (the existing CI/CD pipeline repo).
This required adding ``t3docs-ci-deploy`` to the org's GitHub Actions allow-list
for reusable workflow calls.

GitHub provides a special ``.github`` repository per organization that serves as
the "community health" repo. Reusable workflows placed there are automatically
available to all repositories in the organization without any allow-list
configuration.

Decision
========
Move shared reusable workflows from ``t3docs-ci-deploy`` to
``TYPO3-Documentation/.github``.

This was proposed by @jaapio and implemented by @linawolf.

Consequences
============
*  **Positive:** No org admin action needed — workflows are automatically trusted
*  **Positive:** ``.github`` is the GitHub-conventional location for org-wide
   shared resources (also hosts community health files like CODE_OF_CONDUCT)
*  **Positive:** Clear separation — ``t3docs-ci-deploy`` remains focused on
   build/deploy pipelines
*  **Negative:** The ``.github`` repo has a special role; mixing workflows with
   community health files may cause confusion
*  **Mitigation:** Clear documentation and README explaining the repo's dual purpose
