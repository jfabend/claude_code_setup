---
description: "Create a GitHub Pull Request from current branch"
argument-hint: "[base-branch]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(gh:*)
  - Bash(git:*)
  - AskUserQuestion
model: sonnet
---

# Create GitHub Pull Request

Create a GitHub Pull Request from the current branch, with automatic title and body generation based on commits and changes.

## Step 1: Prerequisites Check

Before proceeding, verify the environment is properly configured:

### Check gh CLI Authentication

Run: `gh auth status`

If the command fails or gh is not installed:
- Display: "Error: GitHub CLI (gh) not installed. Install from https://cli.github.com/"
- Stop execution

If not authenticated:
- Display: "Error: Not authenticated with GitHub. Run `gh auth login` to authenticate."
- Stop execution

### Verify GitHub Repository

Run: `gh repo view`

If this fails:
- Display: "Error: Not in a git repository with a GitHub remote. Ensure you're in a valid GitHub repository."
- Stop execution

### Check for Uncommitted Changes

Run: `git status --porcelain`

If there are uncommitted changes (output is not empty):
- Use AskUserQuestion to prompt the user:
  ```
  You have uncommitted changes in your working directory:

  [list of changed files]

  What would you like to do?

  1. Commit changes before creating PR - I'll help you create a commit first
  2. Stash changes - Temporarily stash changes and proceed
  3. Continue anyway - Create PR with only committed changes
  4. Cancel - Stop and let me handle changes manually

  Please select an option (1-4):
  ```

Based on user response:
- **Option 1**: Guide user through commit creation, then continue
- **Option 2**: Run `git stash` and continue
- **Option 3**: Continue with PR creation
- **Option 4**: Display "PR creation cancelled." and stop execution

## Step 2: Branch Validation

### Get Current Branch

Run: `git branch --show-current`

Store the current branch name.

If on `main` or `master`:
- Display: "Error: Cannot create PR from the default branch. Switch to a feature branch first."
- Stop execution

### Determine Base Branch

Check `$ARGUMENTS` for base branch:

```
Base branch argument: $ARGUMENTS
```

**If $ARGUMENTS is provided and not empty:**
- Use the provided value as the base branch
- Verify it exists: `git rev-parse --verify origin/$ARGUMENTS`
- If not found, display: "Error: Base branch '$ARGUMENTS' not found on remote."
- Stop execution if not found

**If $ARGUMENTS is empty:**
- Detect default branch: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
- Use the detected default branch (typically `main` or `master`)

### Verify Branch Difference

Run: `git log [base-branch]..HEAD --oneline`

If no commits are found (output is empty):
- Display: "Error: No commits found between '[base-branch]' and current branch '[current-branch]'. Make some commits first."
- Stop execution

### Check Remote Tracking

Run: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null`

Store whether the branch has an upstream set:
- If command succeeds: Branch is tracked remotely
- If command fails: Branch needs to be pushed

## Step 3: Analyze Changes

### Get Commit Information

Run: `git log [base-branch]..HEAD --oneline`

Store the list of commits for analysis.

Run: `git log [base-branch]..HEAD --format="%s"` to get commit messages.

### Get Diff Statistics

Run: `git diff [base-branch]...HEAD --stat`

Store the diff statistics showing files changed.

Run: `git diff [base-branch]...HEAD --numstat | wc -l` to count files changed.

### Get Full Diff for Analysis

Run: `git diff [base-branch]...HEAD`

Analyze the diff to understand:
- What types of files were changed (source, tests, docs, config)
- The nature of changes (additions, modifications, deletions)

### Detect Change Type

Analyze commit messages and file changes to determine the primary change type:

1. **Check commit message prefixes** for conventional commits:
   - `feat:` or `feature:` -> Feature
   - `fix:` or `bugfix:` -> Bug Fix
   - `docs:` -> Documentation
   - `test:` -> Tests
   - `refactor:` -> Refactor
   - `chore:` -> Chore
   - `style:` -> Style
   - `perf:` -> Performance

2. **Check file patterns** if no conventional commit found:
   - Changes in `test/`, `tests/`, `*_test.*`, `*_spec.*` -> Tests
   - Changes in `docs/`, `*.md`, `*.rst` -> Documentation
   - Changes in `*.yml`, `*.yaml`, `*.json`, `*.toml` (config files) -> Chore
   - New files with significant code -> Feature
   - Modifications to existing code -> Could be fix or refactor

3. **Use branch name** as fallback:
   - Branch starting with `feat/`, `feature/` -> Feature
   - Branch starting with `fix/`, `bugfix/`, `hotfix/` -> Bug Fix
   - Branch starting with `docs/` -> Documentation
   - Branch starting with `refactor/` -> Refactor
   - Branch starting with `chore/` -> Chore

## Step 4: Generate PR Content

### Generate Title

Create a PR title using this priority:

1. **If single commit**: Use the commit message (cleaned up)
2. **If multiple commits with common prefix**: Use "[type]: Summary of changes"
3. **From branch name**: Convert `feat/add-user-auth` to "Add user auth"

Title formatting rules:
- Capitalize first letter
- Remove conventional commit prefixes (feat:, fix:, etc.) from display
- Keep under 72 characters
- Make it descriptive but concise

### Generate Body

Create a PR body with the following structure:

```markdown
## Summary

[2-4 bullet points summarizing the key changes]

- [Primary change description]
- [Secondary change description]
- [Additional notable changes]

## Changes

[Brief description of what was changed and why]

### Files Changed

[List of key files modified, grouped by type if many]

## Test Plan

- [ ] [Relevant test step 1]
- [ ] [Relevant test step 2]
- [ ] [Manual verification steps if applicable]

## Commits

[List of commits in this PR]

---
*Generated by create-pr command*
```

For the Summary section:
- Analyze the diff and commits
- Extract the main purpose of changes
- Create concise bullet points

For the Test Plan section:
- If test files were modified: Include "Automated tests added/updated"
- If source files changed: Include "Run test suite to verify changes"
- Add relevant manual testing steps based on the nature of changes

## Step 5: User Preview and Confirmation

Display the proposed PR content to the user:

```
Pull Request Preview
====================

Title: [generated title]

Base: [base-branch] <- [current-branch]

Commits: [number of commits]

Body:
-----
[generated body content]
-----

Files to be included: [count] files changed
```

Use AskUserQuestion to get user confirmation:

```
Review the proposed Pull Request above.

What would you like to do?

1. Create PR - Create the Pull Request with this content
2. Edit title - Provide a different title
3. Edit body - Provide a different body
4. Edit both - Provide both a new title and body
5. Cancel - Cancel PR creation

Please select an option (1-5):
```

Based on user response:

- **Option 1**: Proceed to Step 6
- **Option 2**: Use AskUserQuestion to get new title, then return to preview
- **Option 3**: Use AskUserQuestion to get new body, then return to preview
- **Option 4**: Use AskUserQuestion to get new title and body, then return to preview
- **Option 5**: Display "PR creation cancelled." and stop execution

## Step 6: Create Pull Request

### Push Branch if Needed

If the branch has no upstream tracking (from Step 2):

Run: `git push -u origin [current-branch]`

If push fails:
- Display the error message from git
- Display: "Error: Failed to push branch. Check your permissions and try again."
- Stop execution

If push succeeds with upstream already set, optionally run: `git push` to ensure latest commits are pushed.

### Create the Pull Request

Run the gh CLI command to create the PR:

```bash
gh pr create \
  --base "[base-branch]" \
  --title "[final-title]" \
  --body "$(cat <<'EOF'
[final-body-content]
EOF
)"
```

If PR creation fails:
- Display the error message from gh CLI
- Check for common issues:
  - "A pull request already exists" -> Display the existing PR URL
  - Permission denied -> Suggest checking repository permissions
- Display: "Error: Failed to create Pull Request. See error message above."
- Stop execution

### Display Success

On successful creation, display:

```
Pull Request Created Successfully!
==================================

PR URL: [URL returned by gh pr create]

Title: [final-title]
Base: [base-branch] <- [current-branch]
Files Changed: [count]
Commits: [count]

Next steps:
- Review the PR: [URL]
- Request reviewers if needed: gh pr edit [number] --add-reviewer [username]
- Add labels if needed: gh pr edit [number] --add-label [label]
```

## Error Handling Reference

Throughout execution, handle these error cases:

| Error Condition | Message |
|----------------|---------|
| gh CLI not installed | "Error: GitHub CLI (gh) not installed. Install from https://cli.github.com/" |
| Not authenticated | "Error: Not authenticated with GitHub. Run `gh auth login` to authenticate." |
| Not in GitHub repo | "Error: Not in a git repository with a GitHub remote." |
| On default branch | "Error: Cannot create PR from the default branch. Switch to a feature branch first." |
| Base branch not found | "Error: Base branch '[branch]' not found on remote." |
| No commits to PR | "Error: No commits found between '[base]' and current branch '[branch]'. Make some commits first." |
| Push failed | "Error: Failed to push branch. Check your permissions and try again." |
| PR already exists | "A Pull Request already exists for this branch: [existing PR URL]" |
| PR creation failed | "Error: Failed to create Pull Request. See error message above." |
| No argument (optional) | Use detected default branch automatically |

Always provide actionable guidance when an error occurs.
