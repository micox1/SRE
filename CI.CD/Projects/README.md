# CI/CD Pipelines & GitHub Runner Images: A Project-Based Curriculum

## Course Overview

**Prerequisite Knowledge:** Basic Git operations, familiarity with YAML syntax, a working knowledge of at least one programming language (Python, JavaScript, or Go recommended), and comfort with the Linux command line.

**Philosophy:** This curriculum follows a constructivist learning model. You will not be given answers. Each project presents a real-world scenario, a set of constraints, guiding questions, and references. Your job is to research, experiment, fail, debug, and ultimately build working solutions. The struggle is where the learning happens.

**How to Use This Document:**
- Work sequentially — each project assumes knowledge from the previous ones.
- Maintain a **learning journal** where you document what you tried, what failed, and why.
- Every project includes a "Reflection Checkpoint" — do not skip these. Writing forces you to consolidate understanding.
- Time estimates are for focused work and do not include reading time.

**Grading Your Own Work:** Each project includes "Acceptance Criteria" — a set of observable, testable outcomes your solution must satisfy. If your pipeline does not meet every criterion, it is not complete.

---

## UNIT 1: FOUNDATIONS OF CONTINUOUS INTEGRATION

*Projects 1–5 establish your mental model of what CI/CD is, how GitHub Actions executes workflows, and the vocabulary you will need for everything that follows.*

---

### Project 1: The Anatomy of a Workflow File

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 4–6 hours
**Theme:** *Before you can build pipelines, you must be able to read them.*

#### Scenario

You have just joined a team that maintains an open-source Python library. The repository has a `.github/workflows/ci.yml` file that nobody fully understands. Developers keep pushing changes that break the build, and nobody knows which part of the pipeline is responsible for what. Your manager has asked you to create a comprehensive reference document that maps every keyword in a GitHub Actions workflow file to its function.

#### Your Tasks

1. **Create a new public GitHub repository** with a simple Python project (a calculator module with at least four functions: add, subtract, multiply, divide). Include a `requirements.txt` with `pytest` listed.

2. **Write a workflow file from scratch** (do not copy-paste from a tutorial) that does the following:
   - Triggers on push to `main` and on pull requests targeting `main`
   - Triggers on a cron schedule (research the syntax — pick any weekly schedule)
   - Triggers via manual dispatch with one input parameter
   - Runs on `ubuntu-latest`
   - Has at least three distinct jobs: `lint`, `test`, and `report`
   - The `test` job must depend on `lint` completing successfully
   - The `report` job must run regardless of whether `test` passes or fails
   - Uses environment variables at the workflow, job, and step levels
   - Includes at least one conditional step using an `if` expression

3. **For every single YAML key you use**, write a comment above it explaining what it does and what values it accepts. This is not optional — the act of writing forces you to verify your understanding.

#### Guiding Questions (Do Not Skip)

- What is the difference between `on: push` and `on: pull_request` in terms of *which commit* gets checked out?
- What does `needs:` actually control — ordering, or data flow, or both?
- When you write `if: always()`, what precisely does "always" mean? Does the job still run if the workflow is cancelled?
- What is the difference between `${{ github.event_name }}` and `${{ github.ref }}`? When would you use each?
- Where do environment variables set at the workflow level live versus those set at the step level? Can a step override a job-level variable?

#### Acceptance Criteria

- [ ] Repository is public and contains a valid Python project with tests
- [ ] Workflow triggers correctly on push, PR, cron, and manual dispatch
- [ ] Three jobs exist with correct dependency relationships
- [ ] The `report` job runs even when `test` fails (verify by intentionally breaking a test)
- [ ] Every YAML key has an explanatory comment written in your own words
- [ ] At least one step uses a conditional `if` expression that you can explain

#### Required Reading

- GitHub Docs: "Workflow syntax for GitHub Actions" — read the *entire* page, not just the examples: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- GitHub Docs: "Events that trigger workflows": https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
- GitHub Docs: "Expressions": https://docs.github.com/en/actions/learn-github-actions/expressions

#### Reflection Checkpoint

In your learning journal, write a one-page explanation of the GitHub Actions execution model. Cover: What is a runner? What is a job? What is a step? How does GitHub decide when to start a job? What filesystem does a job have access to? What happens to that filesystem when the job ends?

---

### Project 2: The Matrix Strategy and Build Parallelism

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 5–7 hours
**Theme:** *Real software runs on multiple platforms, multiple versions, and multiple configurations simultaneously.*

#### Scenario

Your Python calculator library from Project 1 is gaining users. Some run Python 3.9, others run 3.10, 3.11, or 3.12. Some are on Ubuntu, others on macOS, and a few brave souls are on Windows. A user has filed a bug that only reproduces on Python 3.9 + Windows. You need a CI pipeline that tests every combination.

#### Your Tasks

1. **Extend your workflow** to use a matrix strategy that tests across:
   - At least three Python versions
   - At least two operating systems (ubuntu-latest and one other)

2. **Add a matrix `include`** entry that adds a specific configuration with an extra environment variable (e.g., a "nightly" Python build or a special flag).

3. **Add a matrix `exclude`** entry that removes one specific combination (document *why* you might exclude it in a comment).

4. **Configure `fail-fast`** behavior — first with it enabled, then with it disabled. Observe and document the difference in behavior when one matrix combination fails.

5. **Add a job that runs *after* all matrix jobs complete** and uses the `needs` context to determine if any matrix job failed. This job should post a summary (just an `echo` statement summarizing pass/fail is sufficient).

#### Guiding Questions

- How many individual jobs does a 3×2 matrix create? How does GitHub count these against your concurrency limits?
- When `fail-fast` is true and one job fails, what happens to jobs that have already started but haven't finished?
- Can two matrix jobs share data with each other? Why or why not?
- What is the `${{ matrix.* }}` context and where is it available?
- If you need to run a step only on a specific matrix combination, how do you write that conditional?

#### Acceptance Criteria

- [ ] Matrix produces the correct number of job combinations
- [ ] At least one `include` and one `exclude` are used correctly
- [ ] `fail-fast: false` is demonstrated with observable different behavior from `fail-fast: true` (screenshot or log evidence in your journal)
- [ ] A downstream summary job correctly reports aggregate pass/fail status
- [ ] You can articulate, without looking at notes, what `fail-fast` does

#### Required Reading

- GitHub Docs: "Using a matrix for your jobs": https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs
- GitHub Docs: "Choosing GitHub-hosted runners": https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners

#### Reflection Checkpoint

In your journal, draw a diagram (by hand is fine) showing the execution timeline of a 3×2 matrix with `fail-fast: false` where the (Python 3.9, Windows) combination fails at minute 3 of a 5-minute test suite. Label what happens to every other combination.

---

### Project 3: Secrets, Contexts, and the Security Boundary

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 5–7 hours
**Theme:** *A CI/CD pipeline is a security-critical execution environment. Treat it as such.*

#### Scenario

Your library now needs to publish to PyPI on every tagged release. This requires API tokens. A junior developer on your team suggests "just putting the token in the YAML file." You need to build the correct, secure approach and write documentation explaining *why* the secure approach matters.

#### Your Tasks

1. **Create a GitHub Actions secret** in your repository called `PYPI_API_TOKEN` (use a dummy value for now — do not use a real token until you are confident in your pipeline).

2. **Write a new workflow** (`release.yml`) that:
   - Triggers only on push of a tag matching `v*` (e.g., `v1.0.0`)
   - Has a job that accesses the secret and uses it as an environment variable
   - Has a step that deliberately tries to `echo` the secret value and observe what happens in the logs
   - Uses `${{ secrets.GITHUB_TOKEN }}` for a different purpose (e.g., creating a GitHub Release)

3. **Create an environment** called `production` in your repository settings. Configure it with:
   - Required reviewers (add yourself)
   - A deployment branch rule that only allows `main`

4. **Modify your release workflow** so the publish job uses this environment. Push a tag and observe the approval gate.

5. **Write a security analysis document** (a `SECURITY_ANALYSIS.md` in your repo) that covers:
   - What happens if a secret is printed to logs
   - The difference between repository secrets and environment secrets
   - Why pull requests from forks cannot access secrets by default
   - What `GITHUB_TOKEN` permissions are and how to restrict them

#### Guiding Questions

- If you reference a secret that doesn't exist, does the workflow fail or does it silently use an empty string?
- What is the `permissions` key in a workflow, and what is the principle of least privilege as applied to `GITHUB_TOKEN`?
- Can a workflow in one repository access secrets from another repository? Under what circumstances?
- What is a "poisoned pull request" attack, and how do environments with required reviewers mitigate it?
- What is the security difference between `pull_request` and `pull_request_target` events?

#### Acceptance Criteria

- [ ] Release workflow triggers correctly on version tags and nowhere else
- [ ] Secret is used but never exposed in logs (verified by checking the run logs)
- [ ] Environment with required reviewer approval gate is functional
- [ ] `SECURITY_ANALYSIS.md` exists and covers all five topics listed in Task 5
- [ ] Workflow uses explicit `permissions` to restrict `GITHUB_TOKEN` scope

#### Required Reading

- GitHub Docs: "Using secrets in GitHub Actions": https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
- GitHub Docs: "Security hardening for GitHub Actions": https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- GitHub Docs: "Managing environments for deployment": https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment
- GitHub Blog: "Keeping your GitHub Actions and workflows secure": https://github.blog/security/supply-chain-security/keeping-your-github-actions-and-workflows-secure-part-1-preventing-pwn-requests/

#### Reflection Checkpoint

Write a one-page "threat model" for a CI/CD pipeline. Identify at least three attack vectors and explain how GitHub's security features mitigate each one. Consider: malicious pull requests, compromised dependencies, leaked secrets, and supply chain attacks on Actions themselves.

---

### Project 4: Artifacts, Caching, and Inter-Job Communication

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 6–8 hours
**Theme:** *Jobs are isolated by default. Everything shared must be explicit.*

#### Scenario

Your test suite now generates a coverage report (an HTML file), and your build process produces a distributable package (a `.whl` file). You need the test job to pass its coverage report to a reporting job, and you need the build artifact to be downloadable from the GitHub Actions UI. Your builds are also slow because dependencies are downloaded fresh every time.

#### Your Tasks

1. **Implement dependency caching** for your Python project:
   - Use the `actions/cache` action to cache pip dependencies
   - Use a cache key that invalidates when `requirements.txt` changes
   - Add logging that tells you whether the cache was hit or missed
   - Measure and document the time difference between a cached and uncached run

2. **Generate a test coverage report** (use `pytest-cov` to produce an HTML report) and **upload it as an artifact** using `actions/upload-artifact`.

3. **Create a downstream job** that downloads the artifact and performs some action on it (e.g., parses the coverage percentage from the report and fails if it's below a threshold).

4. **Upload your built package** (`.whl` file) as a separate artifact with a retention period of 5 days.

5. **Implement job outputs**: Have the `test` job set an output variable containing the coverage percentage. Have the downstream job read this output and use it in a conditional.

#### Guiding Questions

- What is the difference between an artifact and a cache? When would you use each?
- What happens to artifacts after their retention period expires?
- Can two jobs running in parallel both write to the same artifact name?
- What is the `actions/cache` restore key fallback mechanism, and why is it useful?
- When you set a job output with `echo "name=value" >> $GITHUB_OUTPUT`, where does that data physically live? How does a downstream job access it?
- What are the storage limits for artifacts and caches? Who pays when those limits are exceeded?

#### Acceptance Criteria

- [ ] Dependency caching is functional with measurable time savings (document the numbers)
- [ ] Coverage HTML report is uploaded and downloadable from the Actions UI
- [ ] A downstream job successfully downloads and processes the coverage artifact
- [ ] Built package is uploaded with a 5-day retention policy
- [ ] Job outputs are used to pass data between jobs
- [ ] You can explain the difference between artifacts, caches, and job outputs without looking at notes

#### Required Reading

- GitHub Docs: "Caching dependencies to speed up workflows": https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- GitHub Docs: "Storing workflow data as artifacts": https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- GitHub Docs: "Defining outputs for jobs": https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs

#### Reflection Checkpoint

Create a data flow diagram for your pipeline. Show every piece of data that moves between jobs, how it moves (artifact vs. output vs. cache), and the lifetime of each piece of data. Include filesystem boundaries — which data exists on which runner, and when is it deleted?

---

### Project 5: Reusable Workflows and Composite Actions

**Difficulty:** ★★★★☆ (Moderate-Hard)
**Estimated Time:** 7–9 hours
**Theme:** *Don't Repeat Yourself applies to infrastructure, not just application code.*

#### Scenario

Your organization now has five Python repositories, all with nearly identical CI workflows. Every time you need to update the CI logic (e.g., adding a new Python version to the matrix), you have to edit five files. This is unsustainable. Your tech lead has asked you to centralize the CI logic.

#### Your Tasks

1. **Create a composite action** in a new repository called `my-actions`:
   - The action should encapsulate: checking out code, setting up Python, installing dependencies, and running tests
   - It should accept inputs for: Python version, requirements file path, and test command
   - It should set outputs for: test result and coverage percentage

2. **Create a reusable workflow** in a repository called `shared-workflows`:
   - The workflow should accept inputs via `workflow_call` for: Python version matrix, operating system matrix, and whether to publish artifacts
   - It should contain the complete CI pipeline: lint, test (matrix), build, and optional artifact upload
   - It should accept secrets via `secrets: inherit` or explicitly declared secrets

3. **Consume both** in your original calculator repository:
   - One workflow that calls the reusable workflow
   - One workflow that uses the composite action directly

4. **Document the trade-offs** between composite actions and reusable workflows in a `ARCHITECTURE.md` file in your shared-workflows repository. Cover: when to use each, limitations of each, how versioning works for each.

#### Guiding Questions

- A composite action runs *within* the calling job's runner. A reusable workflow runs as a *separate* job (or set of jobs). What are the practical implications of this difference for filesystem access, secret access, and billing?
- How do you version a composite action? What does `uses: my-org/my-actions/setup-python@v1` mean, and what are the different ways `v1` can be resolved?
- What are the limits on nesting? Can a reusable workflow call another reusable workflow? Can a composite action use another composite action?
- How does `secrets: inherit` work, and what are the security implications?
- If a reusable workflow defines a matrix, does the calling workflow see individual matrix jobs or a single job?

#### Acceptance Criteria

- [ ] Composite action is published in its own repository and is callable with `uses:`
- [ ] Reusable workflow is published and can be called with `workflow_call`
- [ ] Both are consumed successfully in the calculator repository
- [ ] `ARCHITECTURE.md` covers trade-offs with specific examples
- [ ] Versioning is implemented (at minimum, a `v1` tag on the composite action)
- [ ] You can explain the execution model difference between composite actions and reusable workflows

#### Required Reading

- GitHub Docs: "Creating a composite action": https://docs.github.com/en/actions/creating-actions/creating-a-composite-action
- GitHub Docs: "Reusing workflows": https://docs.github.com/en/actions/using-workflows/reusing-workflows
- GitHub Docs: "About custom actions": https://docs.github.com/en/actions/creating-actions/about-custom-actions

#### Reflection Checkpoint

Write a decision matrix: given a specific scenario (e.g., "I need to share a setup step," "I need to share an entire pipeline," "I need to share logic that requires its own secrets"), which approach is correct and why? Include at least five scenarios.

---

## UNIT 2: CONTINUOUS DELIVERY AND DEPLOYMENT PATTERNS

*Projects 6–10 shift focus from "did the code build?" to "how does the code reach users?"*

---

### Project 6: Multi-Environment Deployment Pipeline

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Code that isn't in production isn't delivering value. But code that breaks production is delivering negative value.*

#### Scenario

Your calculator has evolved into a web API (use Flask or FastAPI). It needs to be deployed to three environments: `development`, `staging`, and `production`. Each environment has different configuration, different approval requirements, and different rollback procedures.

#### Your Tasks

1. **Containerize your application** using Docker. Write a `Dockerfile` that builds a production-ready image. The image should be small (use multi-stage builds), run as a non-root user, and accept configuration via environment variables.

2. **Create three GitHub environments**: `development`, `staging`, `production`. Configure:
   - `development`: No approval required, deploys on every push to `main`
   - `staging`: No approval required, deploys only when development deployment succeeds
   - `production`: Requires manual approval, deploys only when staging deployment succeeds and all tests pass

3. **Write a deployment workflow** that:
   - Builds the Docker image and tags it with the Git SHA
   - Pushes the image to GitHub Container Registry (GHCR)
   - Deploys to each environment sequentially with appropriate gates
   - Passes environment-specific configuration (e.g., API URL, log level) without hardcoding

4. **Implement a smoke test** that runs after each deployment. The smoke test should make an HTTP request to the deployed API and verify it responds correctly. If the smoke test fails in staging, the pipeline should not proceed to production.

5. **Implement a rollback mechanism**: If the production smoke test fails, automatically redeploy the previous known-good image tag.

#### Guiding Questions

- What is the difference between "continuous delivery" and "continuous deployment"? Which does your pipeline implement, and why?
- Why should you tag Docker images with Git SHAs rather than `latest`?
- What is the "environment promotion" pattern, and how does it differ from "branch-based deployment"?
- How do you handle database migrations in a multi-environment deployment? (You don't need to implement this, but you must be able to discuss it.)
- What happens if someone approves a production deployment, but the staging environment has changed since the approval was requested?

#### Acceptance Criteria

- [ ] Application is containerized with a multi-stage Dockerfile
- [ ] Image is pushed to GHCR with SHA-based tags
- [ ] Three environments are configured with correct approval gates
- [ ] Deployment proceeds sequentially: dev → staging → production
- [ ] Smoke tests run after each deployment
- [ ] Failed smoke test in staging blocks production deployment
- [ ] Rollback mechanism is documented and testable

#### Required Reading

- GitHub Docs: "Publishing Docker images": https://docs.github.com/en/actions/publishing-packages/publishing-docker-images
- GitHub Docs: "Managing environments": https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment
- Docker Docs: "Multi-stage builds": https://docs.docker.com/build/building/multi-stage/
- Martin Fowler: "Continuous Delivery" (overview): https://martinfowler.com/bliki/ContinuousDelivery.html

#### Reflection Checkpoint

Draw the state machine for your deployment pipeline. Each state is an environment + status (e.g., "staging-deploying," "staging-smoke-testing," "staging-passed," "production-awaiting-approval"). Show every transition and what triggers it. Identify which transitions are automatic and which require human action.

---

### Project 7: Building and Publishing a Custom GitHub Action

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *The GitHub Actions marketplace is an ecosystem. Understanding how actions work internally makes you a better consumer of them.*

#### Scenario

Your team frequently needs to post deployment notifications to a webhook (e.g., Slack or Discord). The existing marketplace actions don't quite fit your needs. You've been asked to build a custom JavaScript action that can be reused across all your organization's repositories.

#### Your Tasks

1. **Build a JavaScript Action** (not a Docker action, not a composite action — a native JavaScript action) that:
   - Accepts inputs: `webhook-url`, `status` (success/failure/cancelled), `environment`, `message` (optional custom message)
   - Reads the GitHub context to automatically include: repository name, commit SHA, actor (who triggered it), run URL
   - Makes an HTTP POST request to the webhook URL with a formatted payload
   - Sets outputs: `response-status-code`, `notification-sent` (boolean)
   - Handles errors gracefully (network failures, invalid URLs) without crashing the workflow

2. **Write the `action.yml` metadata file** with complete descriptions for every input and output. Include branding (icon and color).

3. **Write unit tests** for your action logic using Jest. Mock the HTTP requests and the GitHub context. Aim for at least 80% code coverage.

4. **Write an integration test workflow** (`.github/workflows/test.yml`) that runs on every push and tests the action against a real webhook endpoint (use a service like webhook.site or a simple echo server).

5. **Publish a release** with semantic versioning. Set up the major version tag (`v1`) to track the latest `v1.x.x` release.

6. **Use your action** in the calculator repository's deployment workflow from Project 6.

#### Guiding Questions

- What is the `@actions/core` package, and what functions does it provide? Why should you use `core.setFailed()` instead of `process.exit(1)`?
- What is the `@actions/github` package, and how does it differ from using `${{ github.* }}` in YAML?
- Why does GitHub recommend committing `node_modules` (or using a bundler like `ncc`) for JavaScript actions?
- How does the major version tag pattern (`v1` pointing to `v1.2.3`) work, and why is it the convention?
- What is the security model for third-party actions? What does `actions/checkout@v4` actually mean — where is that code, and what permissions does it have?

#### Acceptance Criteria

- [ ] JavaScript action is functional with all specified inputs and outputs
- [ ] `action.yml` is complete with descriptions and branding
- [ ] Unit tests exist with mocked dependencies and pass
- [ ] Integration test workflow runs successfully
- [ ] Action is released with semantic versioning and major version tag
- [ ] Action is consumed in another repository's workflow

#### Required Reading

- GitHub Docs: "Creating a JavaScript action": https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action
- GitHub Docs: "Metadata syntax for GitHub Actions": https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
- GitHub Docs: "Publishing actions in GitHub Marketplace": https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace
- `@actions/toolkit` repository: https://github.com/actions/toolkit

#### Reflection Checkpoint

Compare and contrast the three action types: JavaScript, Docker, and Composite. For each, explain: startup time, supported operating systems, language constraints, access to the runner filesystem, and how dependencies are managed. Then create a table showing which type you'd choose for five different use cases.

---

### Project 8: Container-Based CI with Service Containers

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Real applications don't exist in isolation. They depend on databases, caches, message queues, and other services.*

#### Scenario

Your API now requires a PostgreSQL database and a Redis cache. Your CI pipeline needs to test against real instances of these services, not mocks. You also want to run your own custom service (a mock payment processor) as a container during CI.

#### Your Tasks

1. **Extend your API** to use PostgreSQL (any ORM or raw SQL is fine) and Redis (for caching). Write integration tests that require both services.

2. **Configure service containers** in your workflow:
   - PostgreSQL with a specific version, custom database name, and credentials
   - Redis with a specific version
   - Map the correct ports and set health checks so your tests don't run before services are ready

3. **Build a custom service container**: Create a simple Docker image (a Flask app that returns mock payment responses) and use it as a service container in your workflow. This requires either building the image in a prior job or referencing it from a registry.

4. **Handle service container networking**: Research and document the difference between how service containers are accessed when the job runs directly on the runner versus when the job runs inside a container itself (the `container:` key).

5. **Write a comprehensive test suite** that:
   - Tests database migrations run correctly
   - Tests API endpoints that read/write to PostgreSQL
   - Tests caching behavior with Redis
   - Tests payment processing against your mock service
   - Cleans up test data between test runs

#### Guiding Questions

- When you define a service container, what Docker network does it join? How does the job's runner communicate with it?
- What is the difference between `localhost:5432` and `postgres:5432` for accessing the PostgreSQL service container? When is each one correct?
- What happens if a service container crashes during the job? Does the job fail immediately?
- How do health checks work for service containers, and why are they important?
- What are the resource limits on service containers in GitHub-hosted runners?

#### Acceptance Criteria

- [ ] PostgreSQL and Redis service containers are configured and accessible
- [ ] Custom mock service container is built and used in the pipeline
- [ ] Integration tests pass against real service containers
- [ ] Networking differences between runner-based and container-based jobs are documented
- [ ] Health checks prevent premature test execution
- [ ] Tests include proper setup and teardown

#### Required Reading

- GitHub Docs: "About service containers": https://docs.github.com/en/actions/using-containerized-services/about-service-containers
- GitHub Docs: "Creating PostgreSQL service containers": https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers
- GitHub Docs: "Creating Redis service containers": https://docs.github.com/en/actions/using-containerized-services/creating-redis-service-containers
- Docker Docs: "Networking overview": https://docs.docker.com/network/

#### Reflection Checkpoint

Write a comparison of three testing strategies: (1) mocking all external services, (2) using service containers in CI, and (3) testing against shared development servers. For each, discuss: reliability, speed, cost, similarity to production, and maintenance burden. Conclude with your recommendation for when to use each.

---

### Project 9: Building a Complete CI/CD Pipeline with Branch Protection and Status Checks

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *CI/CD is not just about automation — it's about establishing quality gates that protect your users.*

#### Scenario

Your team has grown to five developers. Code is being merged without review, tests are being skipped, and a broken deployment went to production last week. Leadership has mandated that you implement a branch protection strategy with automated enforcement.

#### Your Tasks

1. **Implement a Git branching strategy**:
   - `main` is the production branch — only deployable code lives here
   - `develop` is the integration branch — features merge here first
   - Feature branches follow the pattern `feature/<description>`
   - Release branches follow the pattern `release/v<version>`
   - Write a `CONTRIBUTING.md` that documents this strategy

2. **Configure branch protection rules** for `main`:
   - Require pull requests with at least one approval
   - Require status checks to pass before merging (specify which checks)
   - Require branches to be up to date before merging
   - Require signed commits (research what this means and how to set it up)
   - Disallow force pushes
   - Require linear history (research the implications)

3. **Create a comprehensive status check workflow** that is required for merging:
   - Code linting (use a real linter for your language)
   - Unit tests with coverage threshold (fail if coverage drops below a threshold you define)
   - Security vulnerability scanning (use a tool like `safety` for Python or `npm audit` for Node.js)
   - Build verification (the artifact must build successfully)
   - Documentation check (verify that changed files have corresponding documentation updates — this is intentionally vague; figure out how to implement it)

4. **Create a pull request workflow** that adds automated feedback:
   - Post a comment with the coverage report on every PR
   - Add labels based on which files changed (e.g., `documentation`, `tests`, `api-change`)
   - Run a different set of checks for different file changes (e.g., skip backend tests if only docs changed — use path filters)

5. **Create a merge queue configuration** (if available on your plan) or document how you would use one and why.

#### Guiding Questions

- What is the difference between "required" and "non-required" status checks? What happens if a non-required check fails?
- Why does "require branches to be up to date" exist, and what problem does it solve? What are its downsides?
- What is the difference between merge commits, squash merging, and rebase merging? Which does "require linear history" enforce?
- How do you ensure a status check name is *stable* so branch protection can reference it? What happens if a matrix job's name changes?
- What is CODEOWNERS, and how does it interact with required reviewers?

#### Acceptance Criteria

- [ ] Branch protection rules are configured and enforced on `main`
- [ ] At least five distinct status checks are required for merging
- [ ] PRs receive automated comments with coverage information
- [ ] Path-based filtering correctly skips irrelevant checks
- [ ] `CONTRIBUTING.md` documents the branching strategy
- [ ] A CODEOWNERS file exists and is functional
- [ ] You can demonstrate that a PR with failing checks cannot be merged

#### Required Reading

- GitHub Docs: "Managing a branch protection rule": https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule
- GitHub Docs: "About required status checks": https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging
- GitHub Docs: "About code owners": https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Atlassian Git Tutorial: "Comparing Git Workflows": https://www.atlassian.com/git/tutorials/comparing-workflows

#### Reflection Checkpoint

Imagine you are writing a policy document for a 50-person engineering team. Draft a one-page "CI/CD Standards" document that specifies: minimum required checks, branching rules, review requirements, and deployment approval processes. Justify each requirement.

---

### Project 10: Self-Hosted Runner — Setup, Configuration, and Hardening

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 10–14 hours
**Theme:** *GitHub-hosted runners are convenient. Self-hosted runners are powerful. Both require understanding.*

#### Scenario

Your company has specific requirements that GitHub-hosted runners cannot meet: you need GPU access for ML model testing, you have compliance requirements for data residency, and your builds require access to internal services behind a firewall. You've been tasked with setting up, securing, and maintaining self-hosted runners.

#### Your Tasks

1. **Set up a self-hosted runner** on a Linux machine (a VM, a cloud instance, or even your local machine — but document the choice and its implications):
   - Register it with your repository (not organization-level yet)
   - Configure it with custom labels (e.g., `gpu`, `linux-x64`, `internal`)
   - Verify it appears in the repository settings and can pick up jobs

2. **Configure the runner as a systemd service** so it starts automatically on boot, restarts on failure, and runs as a dedicated non-root user.

3. **Implement runner security hardening**:
   - The runner should be ephemeral — configure it to only accept one job and then re-register (research the `--ephemeral` flag)
   - Workspace cleanup between jobs (what directories need to be cleaned, and why?)
   - Network isolation research — document what network access the runner needs and what it should NOT have access to
   - File system permissions — the runner user should have minimal permissions

4. **Write a workflow that targets your self-hosted runner** using `runs-on: [self-hosted, linux-x64]` and have it do something that a GitHub-hosted runner cannot (e.g., access a local file, use a custom tool you installed).

5. **Create a runner health monitoring workflow** that:
   - Runs on a schedule (every hour)
   - Checks if the self-hosted runner is online (use the GitHub API)
   - Sends a notification (using your action from Project 7) if the runner is offline

6. **Document the total cost of ownership** comparison between GitHub-hosted and self-hosted runners. Include: compute costs, maintenance time, security responsibility, and scaling considerations.

#### Guiding Questions

- What is the security risk of using self-hosted runners with public repositories? Why does GitHub recommend against it?
- What does the `--ephemeral` flag do, and why is it a security best practice? What is the alternative, and what risks does it carry?
- How does the runner communicate with GitHub? What network ports and domains does it need to reach?
- What happens if a job modifies the runner's environment (e.g., installs a global package or changes a system setting)? How does this affect subsequent jobs?
- How do runner groups work at the organization level, and how do you control which repositories can use which runners?
- What is the runner application itself — is it open source? What language is it written in? Where does it store its configuration?

#### Acceptance Criteria

- [ ] Self-hosted runner is registered and visible in repository settings
- [ ] Runner is configured as a systemd service with auto-restart
- [ ] Ephemeral mode is configured and documented
- [ ] A workflow successfully runs on the self-hosted runner
- [ ] Health monitoring workflow runs on schedule and can detect offline runners
- [ ] Security hardening document covers at least five specific measures
- [ ] TCO comparison document exists with real or estimated numbers

#### Required Reading

- GitHub Docs: "About self-hosted runners": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners
- GitHub Docs: "Adding self-hosted runners": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners
- GitHub Docs: "Security hardening for self-hosted runners": https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#hardening-for-self-hosted-runners
- GitHub Docs: "Using self-hosted runners in a workflow": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/using-self-hosted-runners-in-a-workflow
- GitHub Runner Images (open source): https://github.com/actions/runner-images

#### Reflection Checkpoint

Write a risk assessment for self-hosted runners. Structure it as a table with columns: Risk, Likelihood, Impact, Mitigation. Include at least eight distinct risks. Then write a one-paragraph recommendation for when an organization should adopt self-hosted runners.

---

## UNIT 3: ADVANCED PATTERNS AND RUNNER IMAGE ENGINEERING

*Projects 11–15 take you from practitioner to architect. You will build custom runner images, implement advanced pipeline patterns, and tackle the operational complexity of CI/CD at scale.*

---

### Project 11: Custom GitHub Runner Images with Packer

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 12–16 hours
**Theme:** *A runner image is the foundation of your entire CI/CD system. Design it intentionally.*

#### Scenario

Your self-hosted runners from Project 10 need 20 minutes of setup at the start of every job to install tools, download models, and configure the environment. This is unacceptable. You need to build custom runner images with everything pre-installed.

#### Your Tasks

1. **Study the official GitHub runner images repository** (https://github.com/actions/runner-images). Read the Packer templates and understand how they are structured. Do not proceed until you can explain what Packer does and how HCL templates work.

2. **Build a custom runner image using Packer** that includes:
   - The GitHub Actions runner application (specific version, not latest)
   - Your language runtime (Python, Node.js, or Go) at specific versions
   - Common tools: Docker, Docker Compose, git, curl, jq
   - Your project-specific tools (e.g., `terraform`, `kubectl`, a specific linter)
   - A pre-warmed dependency cache (pre-install your project's dependencies)
   - Proper cleanup to minimize image size (clear caches, remove temp files)

3. **Implement image versioning**: The Packer template should produce images with version tags that include a date stamp and a content hash. Document how you would manage the lifecycle of these images (when to build new ones, when to retire old ones).

4. **Create a CI pipeline for your Packer template** — yes, a pipeline that builds your pipeline infrastructure:
   - Validate the Packer template on every PR
   - Build the image on every merge to main
   - Run basic tests on the built image (e.g., verify all expected tools are present)
   - Store the image in a registry (Docker Hub, GHCR, or a cloud provider's registry)

5. **Measure and document the impact**: Compare job startup time and total job duration before and after using the custom image. Record these numbers.

#### Guiding Questions

- What is the difference between a Packer builder, provisioner, and post-processor? How do they compose?
- Why does the official runner images repository use multiple provisioner scripts instead of one giant script?
- What is the "golden image" pattern in infrastructure, and how does it apply to runner images?
- How do you test a runner image? What constitutes a valid test for "this image contains everything a job needs"?
- What is image sprawl, and how do you prevent it? How many different images should one organization maintain?
- What is the security implication of pre-installing tools in a runner image versus installing them at job time?

#### Acceptance Criteria

- [ ] Packer template produces a working runner image
- [ ] Image includes the GitHub Actions runner, language runtimes, and project tools
- [ ] Image is versioned with date and content hash
- [ ] CI pipeline builds and tests the image automatically
- [ ] Before/after performance metrics are documented
- [ ] You can explain every section of your Packer template

#### Required Reading

- HashiCorp Packer: "Getting Started": https://developer.hashicorp.com/packer/tutorials/docker-get-started
- HashiCorp Packer: "HCL Templates": https://developer.hashicorp.com/packer/docs/templates/hcl_templates
- GitHub Actions Runner Images source: https://github.com/actions/runner-images
- GitHub Docs: "About GitHub-hosted runners — preinstalled software": https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners#preinstalled-software

#### Reflection Checkpoint

Write a "Runner Image Architecture Decision Record" (ADR). An ADR documents a significant architectural decision, the context, the options considered, and the rationale for the chosen option. Your ADR should cover: why you chose a custom image over other approaches (e.g., setup steps, Docker-in-Docker), what you included and excluded, and how you will maintain it over time.

---

### Project 12: Auto-Scaling Self-Hosted Runners with Actions Runner Controller (ARC)

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 14–18 hours
**Theme:** *Fixed infrastructure doesn't scale. Kubernetes does.*

#### Scenario

Your organization now has 30 developers and over 100 CI jobs per day. Fixed self-hosted runners cannot keep up during peak hours, and they sit idle at night. You need auto-scaling runners that spin up on demand and shut down when idle.

#### Your Tasks

1. **Set up a Kubernetes cluster** (use Minikube, Kind, k3s, or a cloud provider — document your choice and the trade-offs). You need enough understanding of Kubernetes to deploy workloads, but you do not need to be a Kubernetes expert.

2. **Deploy Actions Runner Controller (ARC)** to your cluster:
   - Install using Helm (read the Helm chart values and understand each one)
   - Configure a `RunnerDeployment` or `RunnerSet` that targets your repository
   - Set autoscaling parameters: minimum runners, maximum runners, and scale-down delay
   - Use your custom runner image from Project 11

3. **Implement scale-to-zero**: Configure the autoscaler so that when there are no queued jobs, the runner count drops to zero. When a job is queued, a runner should spin up within a reasonable time.

4. **Implement runner groups**: Configure at least two different runner groups — one for "standard" jobs and one for "high-resource" jobs (larger resource requests).

5. **Implement monitoring and observability**:
   - How many runners are currently active?
   - How many jobs are queued?
   - What is the average time from "job queued" to "runner started"?
   - Set up at least one alert (can be a simple script) for when queue depth exceeds a threshold

6. **Perform a load test**: Write a workflow that triggers 20 parallel matrix jobs simultaneously. Observe how the autoscaler responds. Document the scale-up time and any queuing delays.

#### Guiding Questions

- What is the difference between `RunnerDeployment` and `RunnerSet` in ARC? When would you use each?
- How does ARC know when to scale up? What mechanism does it use to detect queued jobs?
- What is the cold start problem for auto-scaled runners, and how can you mitigate it?
- What happens if a Kubernetes node runs out of resources while scaling up runners?
- How does runner image pull time affect scaling? What strategies exist to reduce it (e.g., pre-pulling, using local registries)?
- What is the difference between the webhook-based scaler and the polling-based scaler? What are the trade-offs?

#### Acceptance Criteria

- [ ] ARC is deployed to a Kubernetes cluster and manages runners
- [ ] Autoscaling is configured with minimum and maximum runner counts
- [ ] Scale-to-zero is functional (verify with no jobs queued)
- [ ] At least two runner groups exist with different resource profiles
- [ ] Monitoring provides visibility into runner count and queue depth
- [ ] Load test results are documented with scale-up timing
- [ ] You can explain the ARC architecture without looking at documentation

#### Required Reading

- GitHub Docs: "About Actions Runner Controller": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/about-actions-runner-controller
- GitHub Docs: "Quickstart for Actions Runner Controller": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/quickstart-for-actions-runner-controller
- GitHub Docs: "Deploying runner scale sets with ARC": https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller
- Kubernetes Docs: "Overview": https://kubernetes.io/docs/concepts/overview/

#### Reflection Checkpoint

Design an auto-scaling runner infrastructure for a hypothetical company with 200 developers, 1000 CI jobs per day, peak hours of 9am–5pm, and a mix of fast lint jobs (2 minutes) and slow integration test jobs (30 minutes). Specify: how many runner groups, what scaling parameters, what image strategy, and what monitoring you would implement. Include estimated costs.

---

### Project 13: Pipeline Performance Engineering

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 10–14 hours
**Theme:** *A slow pipeline is a broken pipeline. Developer time waiting for CI is expensive.*

#### Scenario

Your CI pipeline takes 25 minutes. Developers are complaining. Product management is complaining. Everyone is complaining. Your goal is to get it under 10 minutes without sacrificing any quality gates.

#### Your Tasks

1. **Profile your existing pipeline**: For every step in your pipeline, record:
   - Wall clock time
   - What it's waiting for (network, CPU, disk, or another job)
   - Whether it could run in parallel with anything else
   - Whether the output is cached or computed fresh each time

2. **Implement at least five distinct optimizations** from this list (choose based on what your pipeline actually needs):
   - **Dependency caching**: Optimize cache keys and restore keys for maximum hit rates
   - **Docker layer caching**: Use buildx with cache-to/cache-from to avoid rebuilding unchanged layers
   - **Test splitting and parallelism**: Split your test suite across multiple matrix jobs using a test-splitting tool (research `pytest-split`, `circleci tests split`, or `knapsack`)
   - **Sparse checkout**: If your repository is large, check out only the directories your job needs
   - **Conditional job execution**: Skip jobs entirely when irrelevant files changed (use path filters and `dorny/paths-filter` or similar)
   - **Build artifact reuse**: Build once, test the built artifact, don't rebuild in every job
   - **Incremental testing**: Only run tests affected by changed files (research test impact analysis)
   - **Concurrency control**: Use the `concurrency` key to cancel redundant runs (e.g., when a new commit is pushed to the same PR)

3. **Implement concurrency controls** to prevent resource waste:
   - Cancel in-progress runs when a new commit is pushed to the same branch
   - Prevent multiple deployments from running simultaneously
   - Document the `concurrency` key's group and cancel-in-progress behavior

4. **Create a dashboard or report** (can be a simple markdown file generated by your pipeline) that tracks:
   - Pipeline duration over time
   - Cache hit rates
   - Most time-consuming steps
   - How often jobs are cancelled due to concurrency

5. **Document each optimization** with before/after measurements. Not estimates — real measurements.

#### Guiding Questions

- What is the critical path of your pipeline? Which jobs are on it, and which are not?
- If you parallelize your test suite across 4 jobs, does the total duration become 1/4? Why or why not?
- What is the cold cache problem, and how does it affect the *first* run after a cache invalidation?
- When you cancel an in-progress run, what happens to artifacts and caches from that run?
- What is the trade-off between more granular caching (higher hit rate but more cache management) and coarser caching (simpler but more cache misses)?
- What is "test flakiness" and why does parallelism sometimes reveal it?

#### Acceptance Criteria

- [ ] Pipeline duration is reduced by at least 50% (document before and after)
- [ ] At least five distinct optimizations are implemented with measurements
- [ ] Concurrency controls prevent redundant runs
- [ ] A performance report is generated automatically
- [ ] Each optimization is documented with before/after data
- [ ] You can explain the critical path concept and identify it in your pipeline

#### Required Reading

- GitHub Docs: "Using concurrency": https://docs.github.com/en/actions/using-jobs/using-concurrency
- GitHub Docs: "Usage limits, billing, and administration": https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration
- Docker Docs: "Optimizing builds with cache management": https://docs.docker.com/build/cache/
- Semaphore: "CI/CD Pipeline Performance": https://semaphoreci.com/blog/ci-cd-pipeline-performance

#### Reflection Checkpoint

Write a "Pipeline Performance Budget" — similar to a web performance budget. Define maximum acceptable times for: total pipeline, any single job, checkout step, dependency installation, test execution, and deployment. For each, explain why that threshold was chosen and what you would do if a future change exceeds it.

---

### Project 14: Advanced Container Image Pipeline — Multi-Architecture, Signing, and SBOM

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 12–16 hours
**Theme:** *Container images are not just build artifacts. They are security boundaries with supply chain implications.*

#### Scenario

Your application is being deployed to both AMD64 and ARM64 servers (common in mixed cloud environments). Security has mandated that all container images must be signed, must include a Software Bill of Materials (SBOM), and must be scanned for vulnerabilities before deployment.

#### Your Tasks

1. **Build multi-architecture images** using `docker buildx`:
   - Build for both `linux/amd64` and `linux/arm64`
   - Push a manifest list to GHCR so that `docker pull` automatically selects the correct architecture
   - Research and document the three approaches to multi-arch builds: QEMU emulation, cross-compilation, and native builders
   - Implement at least one approach in your pipeline

2. **Implement container image signing with cosign**:
   - Install and configure `sigstore/cosign`
   - Sign your images using keyless signing (OIDC-based, tied to your GitHub Actions identity)
   - Verify the signature in a subsequent step
   - Research and document what cosign's keyless signing actually proves — what identity is attested, and what does a verifier learn?

3. **Generate and attach a Software Bill of Materials (SBOM)**:
   - Use a tool like `syft` or `trivy` to generate an SBOM in SPDX or CycloneDX format
   - Attach the SBOM to the container image as an attestation
   - Document what an SBOM contains and why it matters for security

4. **Implement vulnerability scanning**:
   - Scan the built image using `trivy` or `grype`
   - Configure the scanner to fail the pipeline if critical or high vulnerabilities are found
   - Generate a vulnerability report and upload it as an artifact
   - Research the difference between OS-level vulnerabilities and application-level vulnerabilities

5. **Implement an image promotion pipeline**: Images are first pushed with a SHA tag. After passing all security checks, the image is re-tagged with a release version and promoted to a "production" registry (or a different tag pattern). Only promoted images can be deployed to production.

#### Guiding Questions

- What is a container manifest list (also called a "fat manifest"), and how does it enable multi-architecture support?
- What does QEMU emulation cost in terms of build time? When is cross-compilation better?
- What does "keyless signing" mean in the context of Sigstore? Where is the trust rooted?
- What is the difference between an SBOM and a vulnerability scan? Why do you need both?
- What is a "base image vulnerability" and who is responsible for fixing it?
- What is the "time of check, time of use" (TOCTOU) problem in vulnerability scanning, and how does image promotion mitigate it?

#### Acceptance Criteria

- [ ] Multi-architecture images are built and pushed as a manifest list
- [ ] Images are signed with cosign keyless signing
- [ ] Signature verification works in a separate step
- [ ] SBOM is generated and attached to the image
- [ ] Vulnerability scanning fails the pipeline on critical findings
- [ ] Image promotion pipeline separates "scanned" from "deployable" images
- [ ] All security tools and their purposes are documented

#### Required Reading

- Docker Docs: "Multi-platform builds": https://docs.docker.com/build/building/multi-platform/
- Sigstore/Cosign documentation: https://docs.sigstore.dev/signing/quickstart/
- Anchore/Syft: "Generate SBOMs": https://github.com/anchore/syft
- Aqua Security/Trivy: "Container scanning": https://aquasecurity.github.io/trivy
- CISA: "Software Bill of Materials": https://www.cisa.gov/sbom

#### Reflection Checkpoint

Write a "Container Image Supply Chain Security Policy" for a hypothetical company. The policy should specify: what base images are allowed, how often they must be rebuilt, what scanning is required, what signing is required, how SBOMs are managed, and what the incident response procedure is if a vulnerability is discovered in a deployed image. This should be 2–3 pages.

---

### Project 15: Full-Stack CI/CD Platform — The Capstone

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 20–30 hours
**Theme:** *Everything comes together. This is the project where you prove you understand CI/CD as a system, not a collection of YAML files.*

#### Scenario

You are building the CI/CD platform for a small startup with three microservices (frontend, backend API, worker service), a shared library, and infrastructure-as-code (Terraform or Pulumi). Each has its own repository. You must design and implement a complete CI/CD system from scratch.

#### Your Tasks

1. **Design the architecture** before writing any code. Produce an architecture document that covers:
   - Repository structure (monorepo vs. polyrepo — make a choice and defend it)
   - Pipeline topology: which pipelines exist, what triggers them, and how they interact
   - Environment strategy: how many environments, how code flows through them
   - Runner strategy: GitHub-hosted, self-hosted, or hybrid — with justification
   - Secret management strategy: where secrets live, how they're rotated
   - Monitoring and alerting strategy: how you know when the CI/CD system itself is broken

2. **Implement shared CI infrastructure**:
   - A shared composite action or reusable workflow for common steps (lint, test, build, scan)
   - A custom GitHub Action for deployment notifications
   - A custom runner image with all required tools
   - A shared Terraform module (or equivalent) for creating GitHub environments programmatically

3. **Implement per-service pipelines** for at least two of the three services:
   - CI: lint, test (with coverage), build, security scan
   - CD: deploy to dev → staging → production with appropriate gates
   - Each service should use the shared CI infrastructure
   - Services should be independently deployable

4. **Implement cross-service integration testing**:
   - When a shared library changes, all downstream services must be tested
   - Use `repository_dispatch` or `workflow_dispatch` to trigger cross-repo workflows
   - Implement a "deploy all" workflow that deploys all services in the correct order with dependency awareness

5. **Implement operational features**:
   - Automatic rollback on failed health checks
   - Deployment tracking (which version of each service is in each environment)
   - Cost monitoring (track GitHub Actions minutes usage)
   - Incident response workflow: a manual workflow that can quickly roll back any service to a specified version

6. **Write a comprehensive operations runbook** (`RUNBOOK.md`) that covers:
   - How to add a new service to the platform
   - How to update the shared CI infrastructure
   - How to debug a failed deployment
   - How to perform an emergency rollback
   - How to rotate secrets
   - How to update the runner image

#### Guiding Questions

- What is "pipeline coupling," and how do you avoid it when services share CI infrastructure?
- What is the "diamond dependency problem" in microservice deployment, and how do integration tests help?
- How do you handle database schema changes in a multi-service deployment? (Research: expand-and-contract pattern)
- What is "drift" between environments, and how do you detect and prevent it?
- How do you balance "deploy fast" with "deploy safely" when you have multiple services?
- If the CI/CD platform itself has a bug, how do you fix it without the CI/CD platform?

#### Acceptance Criteria

- [ ] Architecture document exists and covers all six areas listed in Task 1
- [ ] Shared CI infrastructure is implemented and consumed by multiple services
- [ ] At least two services have complete CI/CD pipelines
- [ ] Cross-service integration testing is triggered automatically when shared dependencies change
- [ ] Cross-repo triggering works via `repository_dispatch` or equivalent
- [ ] Rollback mechanism is functional and documented
- [ ] Deployment tracking shows which version is in which environment
- [ ] Operations runbook covers all six topics listed in Task 6
- [ ] A team member (or peer) can follow your runbook to perform any listed task

#### Required Reading

- GitHub Docs: "Creating a repository dispatch event": https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch
- GitHub Docs: "Using the GitHub API in workflows": https://docs.github.com/en/actions/using-workflows/using-github-cli-in-workflows
- Martin Fowler: "Microservices": https://martinfowler.com/articles/microservices.html
- Charity Majors: "Deploy vs Release" (the concept): https://charity.wtf/2018/08/19/shipping-software-should-not-be-scary/
- Google SRE Book, Chapter 8: "Release Engineering": https://sre.google/sre-book/release-engineering/
- Thoughtworks Technology Radar (review CI/CD-related entries): https://www.thoughtworks.com/radar

#### Reflection Checkpoint — Final Capstone Reflection

Write a 3–5 page retrospective covering your entire journey through these 15 projects. Address:

1. **Conceptual growth**: What is CI/CD to you now versus what it was when you started? How has your mental model changed?

2. **Hardest lessons**: What were the three most difficult problems you encountered, and what did they teach you?

3. **Design philosophy**: If you were advising a startup that has no CI/CD, what would you tell them to implement first, second, and third? Why that order?

4. **Trade-offs**: Describe three trade-offs you had to make during this curriculum (e.g., speed vs. safety, simplicity vs. flexibility). For each, explain both sides and why you chose what you chose.

5. **What you'd do differently**: If you started over, what would you change about your approach?

6. **Gaps**: What do you still not understand? What would you study next?

---

## Appendix A: Glossary of Terms You Must Be Able to Define

Do not look these up until you've encountered them naturally in the projects. Then write your own definition — not a copied one.

- **CI (Continuous Integration)** — Project 1
- **CD (Continuous Delivery vs. Continuous Deployment)** — Project 6
- **Pipeline** — Project 1
- **Workflow** — Project 1
- **Job** — Project 1
- **Step** — Project 1
- **Runner** — Project 1
- **GitHub-hosted runner** — Project 2
- **Self-hosted runner** — Project 10
- **Runner image** — Project 11
- **Matrix strategy** — Project 2
- **Artifact** — Project 4
- **Cache** — Project 4
- **Secret** — Project 3
- **Environment** — Project 3
- **Branch protection** — Project 9
- **Status check** — Project 9
- **Composite action** — Project 5
- **Reusable workflow** — Project 5
- **Service container** — Project 8
- **Container registry** — Project 6
- **Image manifest** — Project 14
- **SBOM (Software Bill of Materials)** — Project 14
- **Cosign / Sigstore** — Project 14
- **Packer** — Project 11
- **Actions Runner Controller (ARC)** — Project 12
- **Ephemeral runner** — Project 10
- **Concurrency control** — Project 13
- **Repository dispatch** — Project 15
- **Rollback** — Project 6
- **Smoke test** — Project 6
- **Golden image** — Project 11
- **Expand-and-contract migration** — Project 15

---
