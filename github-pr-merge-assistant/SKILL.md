---
name: github-pr-develop-merge-assistant
description: >
  Checks out a GitHub Pull Request branch, diagnoses merge blockers, resolves
  conflicts or obvious code issues, pushes the repaired PR branch, and merges it
  into develop when safe. Use when the user provides a command like
  `gh pr checkout 98`, a PR number, or a PR URL and explicitly wants the PR
  fixed, pushed, and merged into develop. Triggers on: "gh pr checkout <number>",
  "处理 PR", "解决冲突并合并 develop", "merge this PR into develop",
  "fix blockers and push".
allowed-tools: Bash(git:*) Bash(gh:*) Bash(curl:*) Bash(npm:*) Bash(pnpm:*) Bash(yarn:*) Bash(mvn:*) Bash(./gradlew:*) Bash(gradle:*) Bash(pytest:*) Bash(ruff:*) Bash(go:*) Bash(make:*) Read Edit MultiEdit Grep Glob
---

# GitHub PR Develop Merge Assistant

## Purpose

This skill handles a GitHub Pull Request branch that is blocked from merging and needs to be repaired, pushed back to the remote PR branch, and then merged into `develop`.

Typical user input:

```bash
gh pr checkout 98
```

The assistant should understand this as more than a checkout command. It means:

1. Check out the PR branch.
2. Identify the PR branch and its base branch.
3. Sync the latest `develop`.
4. Merge `develop` into the PR branch.
5. Resolve merge conflicts if any.
6. Fix obvious blocking issues such as lint, build, type, or test failures.
7. Commit the fix.
8. Push the repaired code to the remote PR branch.
9. Verify PR checks and mergeability.
10. Merge the PR into `develop` if it is safe and allowed.

The default target branch is `develop` unless the user explicitly specifies another branch.

---

## When to Use

Use this skill when the user provides any of the following:

- A GitHub PR checkout command:

```bash
gh pr checkout 98
```

- A PR number and merge intent:

```text
处理 PR 98，解决冲突后合并到 develop
```

- A PR URL and fix intent:

```text
帮我把这个 PR 修好，并合并到 develop
```

- A branch merge request:

```text
这个分支合并不了，帮我解决阻塞问题，然后推送远程分支并合并 develop
```

- A failed merge or conflict request:

```text
PR 有冲突，帮我解决并推到远程
```

---

## Do Not Use

Do not activate this skill for:

1. General Git questions without intent to modify code.
2. Creating a new PR from scratch.
3. Code review only, unless the user asks to fix or merge.
4. Requests to directly overwrite `main`, `master`, or production branches.
5. Requests that require bypassing protected branch rules, reviews, or CI checks.
6. Repositories where the assistant cannot inspect the current working tree.

---

## Core Principles

1. **Safety first.** Never destroy local work or overwrite remote history without explicit permission.
2. **Minimal change.** Only fix what blocks the PR from merging.
3. **Preserve intent.** Keep the PR author's business logic unless it clearly conflicts with newer `develop` behavior.
4. **Respect `develop`.** Latest `develop` is the source of truth for shared integration code.
5. **Verify before merge.** Run relevant checks whenever possible.
6. **No hidden work.** Report every significant change, conflict, command failure, and unresolved risk.
7. **No direct production push.** Never push to `main`, `master`, release, hotfix, or production branches unless explicitly instructed and safe.

---

## Preconditions

Before making changes, verify the following.

### 1. Current directory is a Git repository

```bash
git rev-parse --show-toplevel
```

If this fails, stop and report:

```text
当前目录不是 Git 仓库，无法处理 PR 分支。
```

### 2. GitHub CLI is available and authenticated

```bash
gh --version
gh auth status
```

If `gh` is not installed or not authenticated, stop and report the exact issue.

### 3. Working tree is clean

```bash
git status --short
```

If there are uncommitted changes, do not continue blindly.

Acceptable handling:

- If the user already gave permission to modify everything, stash local changes first.
- Otherwise stop and report the files.

Suggested message:

```text
当前工作区存在未提交变更。为避免覆盖你的代码，我不会继续合并。
可以选择：stash、提交、或让我停止。
```

Safe stash command if user approves:

```bash
git stash push -u -m "pre-pr-merge-assistant-backup"
```

### 4. Remote is available

```bash
git remote -v
git fetch origin --prune
```

### 5. Target branch exists

Default target branch:

```text
develop
```

Verify:

```bash
git ls-remote --heads origin develop
```

If `develop` does not exist, inspect PR base branch using `gh pr view` and use that base branch only if it is reasonable.

---

## Input Parsing

The user may provide one of these forms.

### Form A: GitHub CLI checkout command

```bash
gh pr checkout 98
```

Extract:

```text
pr_number = 98
```

### Form B: Natural language with PR number

```text
帮我处理 PR 98
```

Extract:

```text
pr_number = 98
```

### Form C: GitHub PR URL

```text
https://github.com/<owner>/<repo>/pull/98
```

Extract:

```text
owner
repo
pr_number
```

If no PR number or URL can be found, ask for the PR number or PR URL.

---

## Standard Workflow

### Step 1: Inspect repository state

Run:

```bash
git rev-parse --show-toplevel
git status --short
git branch --show-current
git remote -v
gh auth status
```

Expected output to collect:

- Repository root
- Current branch
- Dirty files, if any
- Remote name and URL
- GitHub authentication status

Stop if the working tree is dirty and the user did not permit stashing or committing.

---

### Step 2: Checkout PR branch

If the user gave a checkout command, run it directly:

```bash
gh pr checkout <PR_NUMBER>
```

Example:

```bash
gh pr checkout 98
```

Then inspect:

```bash
git branch --show-current
git status --short
```

If checkout fails, report the command output and likely cause:

- PR does not exist.
- User lacks permission.
- Local branch already exists with conflicts.
- `gh` is not authenticated.
- Remote fetch failed.

---

### Step 3: Fetch PR metadata

Run:

```bash
gh pr view <PR_NUMBER> --json number,title,url,state,isDraft,headRefName,headRepositoryOwner,baseRefName,mergeable,reviewDecision,statusCheckRollup
```

Record:

- PR number
- PR title
- PR URL
- PR state
- Draft status
- PR branch name: `headRefName`
- Base branch name: `baseRefName`
- Mergeable state
- Review decision
- Status checks

If the base branch is not `develop`, do not assume. Report it:

```text
这个 PR 的 base 分支是 <baseRefName>，不是 develop。用户目标是 develop，我会优先按 develop 处理；如果仓库规则要求使用 PR base 分支，需要改用 <baseRefName>。
```

If user explicitly wants `develop`, continue with `develop`.

---

### Step 4: Inspect PR diff scope

Get changed files:

```bash
gh pr diff <PR_NUMBER> --name-only
```

Also inspect stats:

```bash
git diff --stat origin/develop...HEAD || true
```

Use the changed file list to keep fixes scoped. The assistant may edit files outside the PR diff only when required to resolve conflicts or compile failures caused by the merge, and must report why.

---

### Step 5: Sync latest develop

Run:

```bash
git fetch origin --prune
```

Update local `develop` safely:

```bash
git checkout develop
git pull --ff-only origin develop
```

If local `develop` does not exist:

```bash
git checkout -B develop origin/develop
```

Return to PR branch:

```bash
git checkout <PR_BRANCH>
```

Verify:

```bash
git branch --show-current
git status --short
```

---

### Step 6: Merge develop into PR branch

Run:

```bash
git merge origin/develop
```

Possible outcomes:

#### Outcome A: Merge succeeds

Continue to checks.

#### Outcome B: Merge conflict

Run:

```bash
git status --short
git diff --name-only --diff-filter=U
```

List conflicted files.

#### Outcome C: Merge fails for non-conflict reason

Examples:

- Dirty working tree.
- Local branch problem.
- Unrelated histories.
- Git hook failure.

Stop and report the exact error.

---

## Conflict Resolution Strategy

### General rules

When resolving conflict markers:

```text
<<<<<<< HEAD
PR branch code
=======
develop branch code
>>>>>>> origin/develop
```

Use this priority:

1. Preserve behavior from `develop` if it contains shared integration changes, dependency changes, API changes, schema changes, or security fixes.
2. Preserve PR-specific functionality unless it is obsolete or incompatible with `develop`.
3. Combine both sides when both are valid.
4. Do not delete tests unless the test is clearly obsolete due to the merged behavior.
5. Do not disable lint, type checks, or build checks merely to pass locally.
6. Do not use `git checkout --ours` or `git checkout --theirs` blindly across all files.

### File-specific guidance

#### Source code files

Resolve by reading surrounding context. Keep imports, method signatures, types, and behavior consistent with latest `develop`.

#### Test files

Preserve meaningful assertions. Update expected values only when behavior genuinely changed.

#### Lock files

Use the package manager to regenerate lock files when possible.

Examples:

```bash
npm install
pnpm install
yarn install
```

Do not hand-edit complex lock conflicts unless the format is simple and obvious.

#### Generated files

If files are generated by build tools, prefer regenerating them using the repository's standard command.

#### Configuration files

Be conservative. Do not change CI, deployment, infrastructure, or environment config unless the conflict is directly related and the resolution is obvious.

---

## Mechanical Conflict Handling Helpers

Use these only after inspecting file intent.

Show conflicted regions:

```bash
grep -R "<<<<<<<\|=======\|>>>>>>>" -n .
```

Show conflicted file names:

```bash
git diff --name-only --diff-filter=U
```

Accept PR side for one file only when correct:

```bash
git checkout --ours <file>
```

Accept develop side for one file only when correct:

```bash
git checkout --theirs <file>
```

After resolving:

```bash
grep -R "<<<<<<<\|=======\|>>>>>>>" -n . || true
git add <resolved-files>
git status --short
```

Complete merge commit:

```bash
git commit -m "Resolve conflicts with develop for PR #<PR_NUMBER>"
```

If Git has an existing merge commit message, it is acceptable to use:

```bash
git commit --no-edit
```

---

## Detect Project Type

After conflicts are resolved, identify the project stack.

### Node.js / Frontend

Indicators:

```text
package.json
pnpm-lock.yaml
yarn.lock
package-lock.json
vite.config.*
next.config.*
tsconfig.json
```

Inspect scripts:

```bash
cat package.json
```

Prefer package manager by lock file:

```text
pnpm-lock.yaml     -> pnpm
yarn.lock          -> yarn
package-lock.json  -> npm
```

Common commands:

```bash
pnpm lint
pnpm test
pnpm build
```

or:

```bash
npm run lint
npm test
npm run build
```

or:

```bash
yarn lint
yarn test
yarn build
```

### Java / Maven

Indicator:

```text
pom.xml
```

Commands:

```bash
mvn test
mvn package -DskipTests
```

If full tests are expensive, at minimum run:

```bash
mvn -q -DskipTests compile
```

### Java / Gradle

Indicators:

```text
build.gradle
build.gradle.kts
gradlew
settings.gradle
```

Commands:

```bash
./gradlew test
./gradlew build
```

If wrapper is unavailable:

```bash
gradle test
gradle build
```

### Python

Indicators:

```text
pyproject.toml
requirements.txt
pytest.ini
setup.py
```

Commands:

```bash
pytest
ruff check .
```

If available:

```bash
ruff check . --fix
```

### Go

Indicators:

```text
go.mod
go.sum
```

Commands:

```bash
go test ./...
go vet ./...
```

### Makefile-based project

Indicator:

```text
Makefile
```

Inspect:

```bash
make help || true
```

Common commands:

```bash
make test
make build
```

---

## Check Selection Rules

Run checks in this order when available:

1. Dependency install only if required.
2. Format or lint check.
3. Type check.
4. Unit tests.
5. Build.
6. Repository-specific validation command.

Prefer commands already defined in the repository.

For Node projects, inspect `package.json` scripts before guessing.

Example:

```bash
cat package.json | grep -E '"(lint|test|build|typecheck|check)"'
```

Do not invent commands that are not defined.

If checks are too expensive or require unavailable services, run the most relevant lightweight check and report the limitation.

---

## Fixing Blocking Issues

### CI failure

Inspect status:

```bash
gh pr checks <PR_NUMBER>
```

If a failed check has a log URL, inspect it with `gh` or `curl` if accessible.

General approach:

1. Identify exact failed command.
2. Reproduce locally if possible.
3. Fix the smallest code path causing the failure.
4. Re-run the failed command.
5. Commit only relevant changes.

### Lint failure

Prefer automatic fix if the repository defines it:

```bash
pnpm lint --fix
npm run lint -- --fix
ruff check . --fix
```

Then inspect diff:

```bash
git diff
```

Commit if changes are safe.

### Test failure

Rules:

1. Do not weaken assertions just to pass.
2. Do not delete failing tests unless obsolete and justified.
3. Prefer updating implementation over changing tests when the PR broke expected behavior.
4. Prefer updating tests when `develop` intentionally changed behavior.
5. If external services are missing, report the environment dependency.

### Build failure

Common causes:

- Missing import.
- Type mismatch after conflict resolution.
- API changed in `develop`.
- Dependency version conflict.
- Lock file conflict.

Fix the direct cause and re-run build.

---

## Commit Rules

Use clear commit messages.

Acceptable messages:

```bash
git commit -m "Resolve conflicts with develop for PR #98"
git commit -m "Fix lint issues after develop merge"
git commit -m "Fix tests after merging develop into PR #98"
git commit -m "Update lockfile after develop merge"
```

Avoid:

```text
AI fixed stuff
misc changes
update
fix
```

Before committing:

```bash
git status --short
git diff --stat
git diff --check
```

Then:

```bash
git add <files>
git commit -m "<message>"
```

If there are no changes after running checks, do not create an empty commit unless the user explicitly wants one.

---

## Push Rules

Push repaired PR branch only after:

1. Conflicts are resolved.
2. There are no conflict markers.
3. Relevant checks have passed or limitations are reported.
4. Changes are committed.

Identify upstream:

```bash
git branch -vv
```

Default push:

```bash
git push
```

If upstream is missing:

```bash
git push origin HEAD:<PR_BRANCH>
```

Never use this by default:

```bash
git push --force
```

Only use this with explicit permission:

```bash
git push --force-with-lease origin HEAD:<PR_BRANCH>
```

If push is rejected because the remote branch moved, run:

```bash
git fetch origin
git status
git log --oneline --decorate --graph --max-count=20 --all
```

Then decide whether to merge/rebase based on repository policy. Do not force-push without confirmation.

---

## Verify PR After Push

Run:

```bash
gh pr view <PR_NUMBER> --json number,title,state,isDraft,mergeable,reviewDecision,statusCheckRollup,headRefName,baseRefName,url
```

Run:

```bash
gh pr checks <PR_NUMBER>
```

Interpretation:

- `PASS`: safe to proceed if other rules pass.
- `PENDING`: report pending checks; do not merge unless user accepts.
- `FAIL`: inspect and fix if possible.
- `SKIPPING`: acceptable only if repository rules allow it.

If PR is draft, do not merge. Report:

```text
PR 当前是 Draft 状态，不应合并到 develop。
```

If review is required and missing, do not bypass. Report:

```text
PR 仍需要 Review，通过本地命令不能绕过仓库规则。
```

---

## Merge into develop

Merge into `develop` only when all are true:

1. User requested final merge into `develop`.
2. PR branch has been pushed.
3. No unresolved conflict remains.
4. Relevant local checks passed, or limitations are explicitly reported.
5. PR is not draft.
6. Required GitHub checks are passing or repository policy allows merge.
7. The assistant has permission to push to `develop` or use PR merge.

### Preferred merge path: GitHub PR merge

If the repository uses protected branches or PR workflows, prefer:

```bash
gh pr merge <PR_NUMBER> --merge
```

If the project uses squash merge:

```bash
gh pr merge <PR_NUMBER> --squash
```

If the project uses rebase merge:

```bash
gh pr merge <PR_NUMBER> --rebase
```

Use the repository's standard merge strategy.

### Alternative merge path: local merge into develop

Only use this when direct push to `develop` is allowed and appropriate.

```bash
git checkout develop
git pull --ff-only origin develop
git merge --no-ff <PR_BRANCH> -m "Merge PR #<PR_NUMBER> into develop"
git push origin develop
```

If the merge fails:

```bash
git merge --abort
```

Then report the conflict and do not push.

---

## Rollback and Recovery

### Abort a merge conflict attempt

Use only when the merge cannot be resolved safely:

```bash
git merge --abort
```

### Restore stashed user work

If a stash was created at the beginning and the PR process is complete:

```bash
git stash list
git stash pop
```

Only pop the stash if returning to the original branch and it is safe.

### Avoid destructive cleanup

Never run automatically:

```bash
git reset --hard
git clean -fd
git branch -D <branch>
```

unless the user explicitly authorizes it after being told the risk.

---

## Safety Constraints

### Never do without explicit permission

```bash
git reset --hard
git clean -fd
git push --force
git push --force-with-lease
git rebase origin/develop
git branch -D <branch>
git push origin --delete <branch>
```

### Never bypass repository rules

Do not bypass:

- Required reviews.
- Required checks.
- Branch protection.
- Signed commit rules.
- CODEOWNERS approval rules.

### Do not hide failures

Never report success if:

- Checks failed.
- Push failed.
- Merge failed.
- PR is still not mergeable.
- Develop was not actually updated.

---

## Interaction Rules

### Before making changes

Briefly state:

1. PR number.
2. Current branch.
3. Target branch.
4. Whether the working tree is clean.
5. Planned operation.

Example:

```text
我会处理 PR #98：先检出 PR 分支，合并最新 develop，解决冲突并运行项目检查。通过后推送 PR 分支，再按仓库规则合并到 develop。
```

### During work

Report important findings:

- Conflicted files.
- Failed checks.
- Files modified.
- Any command that blocks progress.

### When uncertain

Stop and ask only for high-risk ambiguity, such as:

- Business logic conflict cannot be inferred.
- A test failure requires product decision.
- Force push is needed.
- Protected branch rule blocks merge.
- The fix touches deployment, database migration, or security-sensitive config.

For straightforward conflicts, make a best-effort safe fix.

---

## Output Format

After successful completion, respond in Chinese using this structure:

```text
已处理 PR #<PR_NUMBER>。

处理结果：
- PR 标题：<title>
- PR 分支：<pr_branch>
- 目标分支：develop
- 冲突文件：<count> 个
- 修复内容：<summary>
- 本地检查：通过 / 部分通过 / 未执行，原因：<reason>
- 已推送 PR 分支：是 / 否
- 已合并 develop：是 / 否
- 合并方式：gh pr merge / local git merge / 未合并

关键提交：
- <commit_hash> <commit_message>

遗留问题：
- 无
```

If unable to complete safely:

```text
PR #<PR_NUMBER> 暂时无法安全合并。

阻塞原因：
- <reason 1>
- <reason 2>

已完成：
- <completed step 1>
- <completed step 2>

当前状态：
- 当前分支：<branch>
- 工作区状态：<clean/dirty>
- 是否已推送：是 / 否
- 是否已合并 develop：否

需要人工确认：
- <specific decision needed>
```

If checks are pending:

```text
PR #<PR_NUMBER> 已完成本地修复并推送远程分支，但 GitHub 检查仍在运行。

当前状态：
- 本地检查：通过
- 远程检查：Pending
- 已合并 develop：否

建议等 GitHub Checks 全部通过后再执行合并。
```

---

## Example Full Flow

User input:

```bash
gh pr checkout 98
```

Assistant command flow:

```bash
# Validate repo and auth
git rev-parse --show-toplevel
git status --short
gh auth status

# Checkout PR
gh pr checkout 98

# Inspect metadata
gh pr view 98 --json number,title,url,state,isDraft,headRefName,baseRefName,mergeable,reviewDecision,statusCheckRollup

# Fetch latest develop
git fetch origin --prune
git checkout develop
git pull --ff-only origin develop

# Merge develop into PR branch
git checkout <PR_BRANCH>
git merge origin/develop

# If conflicts exist
git diff --name-only --diff-filter=U
grep -R "<<<<<<<\|=======\|>>>>>>>" -n . || true

# Resolve files manually using Read/Edit/MultiEdit
# Then:
git add <resolved-files>
git diff --check
git commit -m "Resolve conflicts with develop for PR #98"

# Run checks according to project type
pnpm lint || npm run lint || true
pnpm test || npm test || true
pnpm build || npm run build || true

# Commit additional fixes if needed
git status --short
git add <files>
git commit -m "Fix issues blocking PR #98 merge"

# Push PR branch
git push origin HEAD:<PR_BRANCH>

# Verify PR
gh pr checks 98
gh pr view 98 --json mergeable,state,isDraft,reviewDecision,statusCheckRollup

# Merge via PR workflow if safe
gh pr merge 98 --merge
```

---

## Project-Specific Customization Section

Add repository-specific rules here when known.

```md
## Repository Rules

- Default target branch: develop
- Preferred merge strategy: merge commit / squash / rebase
- Package manager: pnpm / npm / yarn / Maven / Gradle
- Required local checks:
  - <command 1>
  - <command 2>
- Forbidden changes:
  - deployment config
  - database migration
  - CI pipeline
- Protected branches:
  - develop
  - main
- Push policy:
  - Push PR branch allowed
  - Direct push to develop allowed / not allowed
```

---

## Recommended User Prompt

The user can trigger this skill with:

```text
使用 github-pr-develop-merge-assistant 技能处理：

gh pr checkout 98

目标：
1. 检出 PR 分支；
2. 合并最新 develop；
3. 解决冲突和阻塞问题；
4. 运行项目检查；
5. 推送修复后的 PR 分支；
6. 检查通过后合并到 develop。
```

---

## Final Notes

This skill should behave as a merge operator, not as a broad refactoring assistant.

It should prefer repository conventions, small diffs, clear commits, and branch protection compliance. If a safe merge is impossible, it must stop with a precise blocker report instead of forcing the merge.
