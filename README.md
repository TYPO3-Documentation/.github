# TYPO3 Documentation — Shared Workflows

Reusable GitHub Actions workflows for the
[TYPO3 Documentation](https://github.com/TYPO3-Documentation) organization.

Workflows placed here are automatically available to every repository in the
organization without allow-list configuration.

## Workflows

| Workflow | Status | Purpose |
|----------|--------|---------|
| `reusable-backport.yml` | Production (8 repos) | Backport PRs via labels |
| `reusable-test-documentation.yml` | Available | Documentation rendering test |
| `reusable-apply-precommit.yml` | Available | Auto-fix whitespace via pre-commit |
| `reusable-docs-render.yml` | Available | Render docs with typo3-docs-theme or guides-cli |
| `reusable-php-quality.yml` | Available | CS Fixer + PHPStan + XML lint |
| `reusable-php-tests.yml` | Available | PHP unit/integration test matrix |
| `reusable-php-command.yml` | Available | Generic PHP + Composer command |
| `reusable-node-command.yml` | Available | Generic Node.js + npm command |

**Production** = actively used and proven stable across multiple repos.
**Available** = on main, ready to adopt, not yet used in production.

Each workflow file contains full input/secret documentation in its YAML
`inputs:` and `secrets:` definitions.

## Usage

```yaml
jobs:
  backport:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-backport.yml@main
    with:
      label_pattern: "^backport ([^ ]+)$"
    secrets:
      APP_ID: ${{ secrets.APP_ID }}
      APP_PRIVATE_KEY: ${{ secrets.APP_PRIVATE_KEY }}
```

### Secrets (backport)

| Secret | Required | Description |
|--------|----------|-------------|
| `APP_ID` | no | GitHub App ID for creating backport PRs |
| `APP_PRIVATE_KEY` | no | GitHub App private key (PEM format) |

PRs created with the default `GITHUB_TOKEN` do not trigger CI workflows on the
backport PR. Passing a GitHub App token ensures backport PRs trigger their own CI
checks. Falls back to `GITHUB_TOKEN` if neither secret is provided.

## Migration

1. Identify which shared workflow matches your inline job.
2. Replace the `jobs:` section with a `uses:` call.
3. Pass inputs via `with:` and secrets via `secrets:`.
4. Remove inline `permissions:`, `steps:`, and `runs-on:`.

## Quality gate

Every pull request and push to `main` runs a CI gate over the shared
workflows:

| Check | Tool | Coverage |
|-------|------|----------|
| Lint | [actionlint](https://github.com/rhysd/actionlint) | Workflow syntax, expressions, input references, shellcheck on `run:` blocks |
| Style | [yamllint](https://github.com/adrienverge/yamllint) (`--strict`) | YAML conformance per `.yamllint.yml` |
| Security | [zizmor](https://docs.zizmor.sh/) | Template injection, credential persistence, token misuse, known-vulnerable actions |
| Conformance | `.github/scripts/check_conformance.py` | README table ↔ workflow files in sync, `workflow_call`-only triggers, documented inputs |

Python tools are hash-locked in `.github/requirements.txt`; Dependabot keeps
the action pins and the Python tool versions current (the curl-installed
actionlint binary is bumped manually).

**Consumer contract:** command-style inputs (`command`, `install-command`,
`*-command`) are executed as code. Pass only static literals - never
`github.event.*` data or other untrusted values.

Run the same checks locally before pushing:

```bash
pip install --require-hashes --only-binary ':all:' -r .github/requirements.txt
actionlint
yamllint --strict .github/ .yamllint.yml
zizmor --no-progress .github/
python3 .github/scripts/check_conformance.py
```
