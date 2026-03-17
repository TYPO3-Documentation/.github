.. include:: /Includes.rst.txt

===================================================
ADR-003: Versioning Strategy for Shared Workflows
===================================================

Status
======

Proposed — requesting feedback from maintainers

Context
=======

The shared reusable workflows in this repository are referenced by consumer
repositories using GitHub's ``uses:`` syntax:

.. code-block:: yaml

   uses: TYPO3-Documentation/.github/.github/workflows/reusable-backport.yml@<ref>

GitHub supports three reference types:

1. **Branch** (``@main``) — always uses the latest version
2. **Tag** (``@v1``, ``@v1.2.0``) — uses a specific release
3. **SHA** (``@bfd07ddb...``) — uses an exact commit

The current PRs use ``@main``. One already-merged workflow uses a full SHA pin.
A clear strategy is needed for consistency.

Decision
========

**Recommended: Use ``@main`` for all consumer references.**

Use tags (``@v1``, ``@v2``) only if breaking changes are introduced, following
semantic versioning:

*  **Patch/minor changes** (action version bumps, bug fixes): consumers on
   ``@main`` receive updates automatically — this is the primary benefit.
*  **Breaking changes** (renamed inputs, removed workflows): create a new major
   tag, update consumers explicitly.

**Avoid SHA-pinning shared workflows.** SHA pins reintroduce the exact problem
shared workflows solve:

.. csv-table::
   :header: "Approach", "Action update effort", "Consumer update effort", "Total"

   "Inline workflows", "N/A", "Update each repo", "O(repos)"
   "Shared + @main", "Update once", "None (automatic)", "O(1)"
   "Shared + @SHA", "Update once", "Update each repo's SHA", "O(repos)"

With SHA-pinning, a workflow change requires updating the SHA in every consumer
repository — the same per-repo maintenance burden as inline workflows.

Alternatives Considered
=======================

**SHA-pinning (rejected)**

Provides maximum reproducibility but defeats the core value proposition:

*  When ``actions/checkout`` releases a new version, the shared workflow is
   updated once, and all ``@main`` consumers benefit immediately.
*  With SHA pins, every consumer must update its pin — requiring the same
   multi-repo maintenance we are trying to eliminate.

**Tag-only (partially adopted)**

Tags provide a middle ground but add ceremony:

*  Every change requires creating a tag.
*  Non-breaking changes (the vast majority) do not benefit from versioning.
*  Tags are appropriate for breaking changes but overkill for routine updates.

Consequences
============

*  **Positive:** Consumers receive fixes and action updates automatically.
*  **Positive:** Zero maintenance burden for non-breaking changes across ~29
   repos.
*  **Positive:** Incident response is immediate — fix the shared workflow, all
   repos benefit.
*  **Negative:** A broken push to ``main`` breaks all consumers immediately.
*  **Mitigation:** Require PR review for all changes to this repository.
   Consider branch protection rules.
*  **Negative:** No version pinning for reproducibility.
*  **Mitigation:** GitHub Actions logs record the exact commit SHA used for
   each run, enabling post-hoc debugging.
