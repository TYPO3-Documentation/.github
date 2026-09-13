.. include:: /Includes.rst.txt

==================================================
ADR-005: Inline CI workflows for render-guides
==================================================

Status
======

Accepted — decision of 2026-09-13, recorded from the discussion in
`render-guides#1196
<https://github.com/TYPO3-Documentation/render-guides/pull/1196>`__.

Context
=======

This repository provides shared reusable workflows for the organization.
Three of them are documentation-oriented and widely adopted:
``reusable-backport.yml``, ``reusable-apply-precommit.yml`` and
``reusable-test-documentation.yml`` are called from roughly a dozen manual
repositories.

Three others target PHP projects: ``reusable-php-tests.yml``,
``reusable-php-quality.yml`` and ``reusable-php-command.yml``. They provide
the boilerplate around a command — checkout, ``setup-php``, Composer cache,
``composer install`` — and take the project-specific parts as inputs.

`render-guides#1196
<https://github.com/TYPO3-Documentation/render-guides/pull/1196>`__ proposed
migrating the ``main.yaml`` workflow of
`render-guides <https://github.com/TYPO3-Documentation/render-guides>`__ to
those three PHP workflows, replacing about 130 lines of inline job
definitions with six ``uses:`` calls.

At the time of the decision:

*  The PHP workflows have **no callers**. The only mention of
   ``reusable-php-tests`` anywhere in the organization is the ``README.md``
   of this repository. render-guides would be the sole consumer.
*  The inline jobs in ``main.yaml`` SHA-pin every action, and Dependabot
   keeps those pins current. They are *ahead* of the pins in the shared
   workflows: ``shivammathur/setup-php`` 2.37.2 versus 2.37.1, and
   ``actions/cache`` v6.1.0 versus v5.0.3.
*  The migration referenced the shared workflows at ``@main``.
*  A called workflow reports its checks as ``<job name> / <inner job
   name>``, so six of the seven required status checks would be renamed.
*  Three steps of the ``Quality`` job — ``composer normalize --dry-run``,
   ``make test-docs`` and ``make test-rendertest`` — do not fit the inputs
   of ``reusable-php-quality.yml`` and would become separate jobs. They are
   gated today by virtue of being steps inside a required check; as separate
   jobs they are gated only if the ruleset lists them.
*  render-guides runs a merge queue on ``main`` (ADR-004), which gates on
   exactly those context names.

Decision
========

**render-guides keeps its CI jobs defined inline in** ``main.yaml`` **for
now.** The shared PHP workflows are not adopted there yet.

This is a decision about amortisation, not about the shared workflows
themselves. "Maintained in one place instead of once per repository"
requires a second repository to amortise against. With a single consumer,
the migration splits one workflow definition across two repositories,
returns the same maintenance work, and adds coupling: a push to ``main`` of
this repository would change the CI of render-guides without review there.

Two costs would be incurred immediately for a benefit that does not exist
yet:

*  **Action pinning would regress.** render-guides would move from
   SHA-pinned actions that Dependabot keeps current to a floating ``@main``
   reference to this repository, and to three action versions that are
   currently older than its own.
*  **The merge-queue ruleset would churn.** Six of seven required contexts
   rename, and three previously implicit checks must be added explicitly or
   they silently stop gating. There is no ordering of the ruleset change and
   the merge that keeps the gate closed throughout, so the switch needs a
   deliberate quiet window.

render-guides is also the repository that renders every other manual in the
organization. Where the trade is close, the preference there is for fewer
moving parts owned elsewhere.

**Revisit when a second PHP repository adopts the shared PHP workflows.**
At that point the amortisation argument holds, and render-guides should
follow rather than remain the exception.

Alternatives Considered
=======================

**Migrate now as proposed (rejected)**

Incurs the pinning regression and the ruleset window described above, in
exchange for centralisation that has no second consumer to benefit from it.

**Migrate, but pin the shared workflows to a tag or SHA (rejected for now)**

Removes the ``@main`` coupling and is what adoption should look like
eventually. It does not address the core point: with one consumer, the
indirection costs more than it saves. Tag releases with Dependabot bumping
consumers are a precondition for adoption, not a reason for it.

**Extend** ``reusable-php-quality.yml`` **with a generic extra-commands
input (deferred)**

Would let ``composer normalize``, ``make test-docs`` and ``make
test-rendertest`` stay inside the ``Quality`` job, reducing the ruleset
change from seven contexts to five and keeping those checks gated by
construction. Worth doing when render-guides or another PHP repository
adopts the workflows; it does not by itself make adoption worthwhile today.

**Retire the PHP workflows (rejected)**

They are small, correct, and cost nothing while unused. A second PHP
repository may well appear.

Consequences
============

*  ``main.yaml`` in render-guides keeps roughly 130 lines of duplicated
   setup boilerplate. Dependabot maintains its action pins, as it does
   today.
*  The seven required status-check contexts of render-guides stay as they
   are; no merge-queue coordination window is needed.
*  The shared PHP workflows remain without a consumer. They are not removed.
*  If the organization later standardises PHP CI across several
   repositories, render-guides is expected to follow, and this ADR is
   superseded rather than cited as a permanent exemption.
*  render-guides calls none of the shared workflows today.
   ``reusable-apply-precommit.yml`` and ``reusable-backport.yml`` are a
   plausible fit there and can be evaluated independently of this decision.
