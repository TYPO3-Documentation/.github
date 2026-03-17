# TYPO3 Documentation — Shared Workflows

This repository provides **reusable GitHub Actions workflows** for the
[TYPO3 Documentation](https://github.com/TYPO3-Documentation) organization.

Placing workflows in the `.github` repository makes them automatically available
to every repository in the organization without allow-list configuration.

## Available Workflows

### reusable-backport.yml

Creates backport pull requests when a merged PR carries a matching label.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `label_pattern` | string | `^backport ([^ ]+)$` | Regex pattern to match backport labels. Must contain a capture group for the target branch. |

| Secret | Required | Description |
|--------|----------|-------------|
| `APP_ID` | no | GitHub App ID for creating backport pull requests |
| `APP_PRIVATE_KEY` | no | GitHub App private key (PEM format) |

> **Note:** PRs created with the default `GITHUB_TOKEN` do not trigger CI
> workflows on the backport PR. Passing a GitHub App token ensures backport PRs
> trigger their own CI checks. If neither secret is provided the workflow falls
> back to the default `GITHUB_TOKEN`.

```yaml
# .github/workflows/backport.yml
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
```

### reusable-test-documentation.yml

Renders documentation inside a Docker container using the official
[render-guides](https://github.com/TYPO3-Documentation/render-guides) image and
verifies it builds without warnings.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `render-flags` | string | `--no-progress --minimal-test` | Additional flags passed to `render-guides` |
| `schedule-repository` | string | `""` | Repository name to restrict scheduled runs (empty = always run) |

```yaml
# .github/workflows/test-documentation.yml
name: Test documentation
on: [push, pull_request]

jobs:
  test-docs:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-test-documentation.yml@main
    with:
      render-flags: "--no-progress --fail-on-log"
```

### reusable-apply-precommit.yml

Runs [pre-commit](https://pre-commit.com) hooks across the repository and opens
a pull request with any resulting fixes. Designed for scheduled runs.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python-version` | string | `3.x` | Python version used to run pre-commit |
| `pr-title` | string | `Fix whitespace issues` | Title of the auto-generated pull request |
| `pr-body` | string | `This PR automatically applies whitespace fixes.` | Body text of the auto-generated pull request |

```yaml
# .github/workflows/apply-precommit.yml
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
```

### reusable-php-quality.yml

Runs static analysis tools (PHP CS Fixer, PHPStan, XML linting) against a PHP
project. Each tool can be toggled and customized.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `php-version` | string | `8.2` | PHP version for quality checks |
| `run-cs-fixer` | boolean | `true` | Whether to run PHP CS Fixer |
| `cs-fixer-command` | string | `make test-cs-fixer` | Command to invoke PHP CS Fixer |
| `run-phpstan` | boolean | `true` | Whether to run PHPStan |
| `phpstan-command` | string | `make test-phpstan` | Command to invoke PHPStan |
| `run-xml-lint` | boolean | `false` | Whether to run XML linting |
| `xml-lint-command` | string | `make test-xml-lint` | Command to invoke XML linting |
| `php-extensions` | string | `""` | Space-separated PHP extensions to install |
| `run-environment` | string | `local` | Value of the `RUN_ENVIRONMENT` env variable |

```yaml
# .github/workflows/php-quality.yml
name: PHP Quality
on: [push, pull_request]

jobs:
  quality:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: "8.2"
      run-cs-fixer: true
      run-phpstan: true
```

### reusable-php-tests.yml

Runs unit and integration tests across a matrix of PHP versions.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `php-versions` | string (JSON) | `["8.2", "8.3", "8.4", "8.5"]` | JSON array of PHP versions to test against |
| `dependency-versions` | string | `locked` | Composer dependency resolution strategy |
| `test-unit-command` | string | `make test-unit` | Command to run unit tests (empty to skip) |
| `test-integration-command` | string | `""` | Command to run integration tests (empty to skip) |
| `php-extensions` | string | `""` | Space-separated PHP extensions to install |
| `run-environment` | string | `local` | Value of the `RUN_ENVIRONMENT` env variable |

```yaml
# .github/workflows/php-tests.yml
name: PHP Tests
on: [push, pull_request]

jobs:
  tests:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-tests.yml@main
    with:
      php-versions: '["8.2", "8.3", "8.4"]'
      test-unit-command: "make test-unit"
```

### reusable-php-command.yml

A generic workflow that sets up PHP, installs Composer dependencies, and runs a
single arbitrary command. Useful for one-off tasks that do not fit the
specialized quality or test workflows.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `php-version` | string | `8.2` | PHP version |
| `command` | string | *(required)* | Command to run after `composer install` |
| `php-extensions` | string | `""` | Space-separated PHP extensions to install |
| `composer-args` | string | `--no-interaction --no-progress --prefer-dist` | Additional `composer install` arguments |
| `run-environment` | string | `local` | Value of the `RUN_ENVIRONMENT` env variable |

```yaml
# .github/workflows/generate-docs.yml
name: Generate API docs
on: [push]

jobs:
  generate:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-php-command.yml@main
    with:
      php-version: "8.3"
      command: "vendor/bin/generate-api-docs"
```

### reusable-docs-render.yml

Renders TYPO3 documentation using either the Python-based `typo3-docs-theme` or
the Composer-based `typo3/guides-cli`, auto-detecting which is available.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python-version` | string | `3.12` | Python version used when rendering via `typo3-docs-theme` |

```yaml
# .github/workflows/docs-render.yml
name: Render documentation
on: [push, pull_request]

jobs:
  render:
    uses: TYPO3-Documentation/.github/.github/workflows/reusable-docs-render.yml@main
    with:
      python-version: "3.12"
```

## Migration

To migrate an existing inline workflow to a shared reusable workflow:

1. Identify which shared workflow matches your current inline job.
2. Replace the `jobs:` section with a `uses:` call to the shared workflow.
3. Pass any required inputs via `with:`.
4. Remove inline `permissions:`, `steps:`, and `runs-on:` -- these are defined
   in the shared workflow.

## Documentation

Full RST documentation is available in the [Documentation/](Documentation/)
directory and can be rendered with
[render-guides](https://github.com/TYPO3-Documentation/render-guides).
