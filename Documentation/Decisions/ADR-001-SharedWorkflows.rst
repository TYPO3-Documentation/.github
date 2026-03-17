.. include:: /Includes.rst.txt

===========================================
ADR-001: Use Shared Reusable Workflows
===========================================

Status
======
Accepted

Context
=======
The TYPO3 Documentation organization maintains ~29 repositories with similar
CI/CD workflows. Each repository maintained its own inline workflow definitions,
leading to:

*  **Maintenance burden** — Action version updates required touching every repo
*  **Inconsistency** — Repos drifted apart in configuration
*  **Incident amplification** — A broken action (e.g. ``m-kuhn/backport@30b6e83``
   missing ``dist/index.js``) required individual fixes in each repo
*  **Allow-list compliance** — The org enforces SHA-pinned actions; composite
   actions like ``ramsey/composer-install`` that internally use tag references
   break all CI runs

Decision
========
Centralize common CI/CD patterns as `reusable workflows
<https://docs.github.com/en/actions/sharing-automations/reusing-workflows>`__
in a single org-owned repository.

Reusable workflows:

*  Execute in their own context, bypassing the caller's action allow-list
*  Provide a single point for action SHA pin management
*  Accept inputs for repo-specific configuration while enforcing consistent
   defaults

Consequences
============
*  **Positive:** One-place updates for action versions, consistent behavior,
   faster incident response
*  **Positive:** Calling repos need only a few lines of YAML
*  **Negative:** Added indirection — debugging requires looking at two repos
*  **Negative:** Breaking changes in shared workflows affect all consumers
*  **Mitigation:** Use ``@main`` ref with careful review; consider tags for
   stability later
