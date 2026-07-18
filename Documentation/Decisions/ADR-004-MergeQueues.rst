.. include:: /Includes.rst.txt

==================================================
ADR-004: Merge Queue for render-guides
==================================================

Status
======

Accepted — team decision from the documentation team discussion of
2026-07-09 to 2026-07-14.

Context
=======

On 2026-07-09, two individually green pull requests in
`render-guides <https://github.com/TYPO3-Documentation/render-guides>`__
merged past each other:

*  `#1305 <https://github.com/TYPO3-Documentation/render-guides/pull/1305>`__
   changed the inline-code Twig template (merged 14:18 UTC).
*  `#1294 <https://github.com/TYPO3-Documentation/render-guides/pull/1294>`__
   added an integration-test fixture generated against the *old* template.
   Its CI checks had last run before #1305 landed, so they were still green
   when it was merged at 14:36 UTC.

The resulting ``main`` build
(`run 29026096068 <https://github.com/TYPO3-Documentation/render-guides/actions/runs/29026096068>`__)
failed on all PHP versions. ``main`` stayed red for about 70 minutes until
`#1324 <https://github.com/TYPO3-Documentation/render-guides/pull/1324>`__
regenerated the fixture. While ``main`` is red, every open pull request
inherits the failure, and someone has to interrupt their work to repair it.

Nothing in the repository configuration prevents this class of failure:
branch protection on ``main`` requires no status checks, so the
"require branches to be up to date" flag has no effect, and no mechanism
re-tests a pull request against the current ``main`` between approval and
merge.

The documentation team is small and maintains roughly 50 repositories.
Maintainers typically review and merge pull requests in batches. The CI of
most documentation repositories renders full manuals and is slow.

Decision
========

Enable a **merge queue** on the ``main`` branch of **render-guides only**,
as a trial.

A merge queue re-runs the required checks for every queued pull request
against the latest ``main`` (including the pull requests queued ahead of it)
before merging. A pull request that would break ``main`` is rejected from
the queue and blocks only itself; ``main`` stays green and nobody has to
rebase or re-trigger checks manually.

Configuration:

*  A repository ruleset on ``refs/heads/main`` provides the merge queue
   (merge method *squash*, all queue entries must pass) and lists the seven
   checks of the *Main* workflow as required status checks.
*  The classic "require branches to be up to date" flag is dropped as
   redundant: the queue provides the same guarantee without manual
   update-branch round-trips.
*  Workflows that produce required checks carry a ``merge_group`` trigger
   (`render-guides#1326
   <https://github.com/TYPO3-Documentation/render-guides/pull/1326>`__);
   without it, queued merges receive no checks and time out.
*  Repository admins can bypass the ruleset as an emergency path when CI
   itself is broken.

**This decision is explicitly scoped to render-guides.** Other repositories
of the organization do not get a merge queue. For repositories containing
only documentation, changes rarely interact semantically, render CI is slow,
and maintainers batch-merge many pull requests at once — there, the added
per-merge pipeline time is not justified by the rare broken ``main``, which
is cheaper to fix when it happens.

Merge method: *squash* matches the observed practice on ``main`` (all recent
merges are squash merges) and keeps commits signed by GitHub. A merge queue
applies one merge method to every queued pull request, so the per-pull-request
choice between squash and rebase disappears. Switching the queue to *rebase*
(preserving authored commit series, at the cost of re-created unsigned
commits and replayed fix-up commits) remains possible as a separate, later
decision.

Alternatives Considered
=======================

**Required status checks plus "require branches to be up to date" (rejected)**

Prevents the same failure class, but every merge of another pull request
invalidates all remaining approved pull requests: each one must be updated
manually and wait for a full CI run before it can merge. For maintainers who
merge in batches, this serializes the whole batch into manual update/wait
cycles — the merge queue automates exactly this work.

**Merge queues for all repositories of the organization (rejected)**

Documentation-only repositories rarely see semantically conflicting pull
requests, and their full-render CI is slow. The queue's extra CI run per
merge would cost more than the occasional broken ``main`` it prevents.
Revisit per repository if the render-guides failure mode is observed there.
(Technically, the merge-queue rule is only available in repository-level
rulesets, not organization-level ones, so rollout is a per-repository
decision in any case.)

**Status quo (rejected for render-guides)**

render-guides is a tooling repository: template, theme, and rendering
changes interact across pull requests, as the 2026-07-09 incident shows.
Relying on somebody noticing and repairing a broken ``main`` does not scale
for a small team.

Consequences
============

*  Merging changes from "Merge" to "Merge when ready"; GitHub queues the
   pull request once approvals and checks are met. ``gh pr merge --auto``
   and the existing Dependabot auto-merge flow queue the same way.
*  A pull request whose merge group fails is removed from the queue and
   blocks only itself; ``main`` stays green.
*  Each merged pull request costs one additional full CI run (pipeline
   time, not human time).
*  The seven *Main* checks are now enforced as required status checks —
   previously no check was required at all.
*  Workflow refactors must preserve the ``merge_group`` trigger and keep
   the ruleset's required-check contexts in sync with the reported job
   names; a rename without a ruleset update blocks all merges until fixed.
*  Emergency path when CI itself is broken: repository admins bypass the
   ruleset, or disable it (one API call), and restore it afterwards.

Trial review: revisit after about three months, or after five queue
rejections, whichever comes first — weighing queue overhead against
prevented breakage. Extend to other repositories (for example ``.github``,
``t3docs-search-indexer``, ``t3docs-typo3-api``) only if the same failure
mode is observed there.
