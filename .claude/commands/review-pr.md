---
description: "Review a GitHub Pull Request"
argument-hint: "<pr-number>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(gh:*)
  - Bash(git:*)
  - AskUserQuestion
model: sonnet
---

# GitHub Pull Request Review

You are tasked with reviewing a GitHub Pull Request and providing a comprehensive code review with optional submission.

## Step 1: Validate Argument

Check that a PR number was provided:

```
PR number: $ARGUMENTS
```

If `$ARGUMENTS` is empty or not provided:
- Display: "Error: No PR number provided. Usage: /review-pr <pr-number>"
- Stop execution immediately

If `$ARGUMENTS` is not a valid number:
- Display: "Error: Invalid PR number. Usage: /review-pr <pr-number>"
- Stop execution immediately

## Step 2: Prerequisites Check

### Check GitHub CLI Authentication

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

## Step 3: Fetch PR Details

Run the following command to fetch PR details:

```bash
gh pr view $ARGUMENTS --json number,title,body,author,baseRefName,headRefName,state,labels,reviewRequests,url
```

If the PR is not found:
- Display: "Error: Pull Request #$ARGUMENTS not found in this repository"
- Stop execution

Parse the JSON response and extract all fields.

## Step 4: Present PR Context

Display the PR information in a clear format:

```
## Pull Request #[number]: [title]

**URL:** [url]
**Author:** [author.login]
**State:** [state]
**Base Branch:** [baseRefName] <- **Head Branch:** [headRefName]
**Labels:** [labels as comma-separated list, or "None"]
**Review Requests:** [reviewRequests as comma-separated list, or "None"]

### Description

[body content, or "No description provided"]
```

### Verify PR State

Check the PR state:

If state is `MERGED`:
- Display: "Error: This PR has already been merged. Review is informational only - no review can be submitted."
- Stop execution

If state is `CLOSED`:
- Display: "Error: This PR has been closed without merging. Review is informational only - no review can be submitted."
- Stop execution

## Step 5: Check CI Status

Run: `gh pr checks $ARGUMENTS`

Analyze the output:

**If any checks have FAILED:**
- Display warning:
  ```
  WARNING: CI checks have FAILED

  Failed Checks:
  - [list failed check names]

  Recommendation: Consider requesting changes until CI passes.
  ```
- Continue with code review

**If checks are PENDING:**
- Display notice:
  ```
  Notice: CI checks are still running.

  Pending Checks:
  - [list pending check names]
  ```
- Continue with code review

**If all checks PASSED:**
- Display: "CI Status: All checks passed"
- Continue with code review

**If no checks configured:**
- Display: "CI Status: No CI checks configured for this repository"
- Continue with code review

## Step 6: Get PR Changes

### Fetch the Diff

Run: `gh pr diff $ARGUMENTS`

Store the complete diff for analysis.

### Categorize Changed Files

Run: `gh pr view $ARGUMENTS --json files --jq '.files[].path'`

Categorize each file into:

| Category | File Patterns |
|----------|---------------|
| Code | `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.c`, `.cpp`, `.rb`, etc. |
| Tests | `test_*.py`, `*_test.py`, `*.test.js`, `*.spec.ts`, `tests/`, `__tests__/` |
| Documentation | `.md`, `.rst`, `.txt`, `docs/` |
| Configuration | `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.env*`, `Dockerfile`, `Makefile` |
| Other | Everything else |

Display summary:
```
### Changed Files Summary

**Total files changed:** N

| Category | Count | Files |
|----------|-------|-------|
| Code | N | file1.py, file2.js |
| Tests | N | test_file.py |
| Documentation | N | README.md |
| Configuration | N | pyproject.toml |
| Other | N | ... |
```

## Step 7: Read Project Guidelines

Before analyzing code, understand the project standards:

### Global Instructions
Check if `~/.claude/CLAUDE.md` exists. If it does, read it to understand global coding standards and conventions.

### Project Instructions
Check if `./CLAUDE.md` exists in the current directory. If it does, read it to understand project-specific:
- Coding guidelines
- Test requirements
- Quality gates
- Any special instructions

Use these guidelines to inform your code review.

## Step 8: Analyze Code Quality

Review the diff for the following categories. Base your analysis on the actual changes in the PR.

### 8.1 Code Style Consistency

Check for:
- Naming conventions (variables, functions, classes)
- Formatting consistency with existing code
- Import organization
- Comment style and quality
- Adherence to project's stated style guide (from CLAUDE.md)

### 8.2 Potential Bugs and Anti-patterns

Look for:
- Is the code correct?
- Does it solve what it is meant for?
- Null/undefined reference risks
- Resource leaks (unclosed files, connections)
- Race conditions in async code
- Infinite loops or recursion without base case
- Off-by-one errors
- Hardcoded values that should be configurable
- Dead code or unreachable code
- Copy-paste errors

### 8.3 Security Concerns

Check for OWASP Top 10 and common security issues:
- Hardcoded secrets, API keys, passwords
- SQL injection vulnerabilities
- Command injection risks
- Path traversal vulnerabilities
- Cross-site scripting (XSS) vectors
- Insecure deserialization
- Missing input validation
- Sensitive data exposure in logs
- Insecure cryptographic practices

### 8.4 Test Coverage

Analyze test changes:
- Are tests added for new functionality?
- Are tests updated for changed behavior?
- Do tests cover edge cases?
- Are tests meaningful (not just coverage padding)?
- Test naming clarity

If code is added but no tests:
- Flag as concern if project requires tests (check CLAUDE.md for test requirements)

### 8.5 Documentation

Check for:
- Docstrings on new public functions/classes
- Updated README if behavior changes
- Inline comments for complex logic
- API documentation updates if applicable
- Type hints present (if project requires them)

### 8.6 Architecture and Design

Consider:
- SOLID principles adherence
- Appropriate abstraction levels
- Separation of concerns
- Code duplication
- Breaking changes
- Performance implications

## Step 9: Generate Review Report

Compile findings into a structured report:

```
# Code Review Report

## Summary

[2-3 sentence summary of what this PR does]

## Findings

### Critical Issues (Must Fix)

[Issues that should block merge - bugs, security issues, breaking changes]

1. **[File:Line]** - [Description of issue]
   - Why: [Explanation]
   - Suggestion: [How to fix]

[If none: "No critical issues found."]

### Suggestions (Nice to Have)

[Non-blocking improvements that would enhance the code]

1. **[File:Line]** - [Description]
   - Suggestion: [Improvement idea]

[If none: "No suggestions."]

### Questions (Need Clarification)

[Things that are unclear or may need discussion]

1. **[File:Line]** - [Question]

[If none: "No questions."]

### Praise (Good Practices)

[Highlight things done well - encourages good practices]

1. **[File:Line]** - [What was done well]

[If none: Skip this section]

## CI Status

[Pass/Fail/Pending summary from Step 5]

## Overall Assessment

[One of the following:]
- **Approve**: Code looks good, no critical issues, ready to merge
- **Request Changes**: Critical issues must be addressed before merge
- **Comment Only**: Questions need answers or suggestions provided for consideration
```

## Step 10: User Decision

If the PR is still open (not merged or closed), use AskUserQuestion:

```
Review complete. How would you like to proceed?

1. **Approve** - Submit approval with the review summary
2. **Request Changes** - Submit review requesting changes (use if critical issues found)
3. **Comment** - Submit as comment only (use for questions/suggestions without blocking)
4. **Cancel** - Exit without submitting a review

Enter your choice (1-4):
```

If the PR is merged or closed:
- Display: "PR is [merged/closed]. Skipping review submission."
- End execution

## Step 11: Submit Review

Based on user's choice, submit the review:

### For Approve (Choice 1)

```bash
gh pr review $ARGUMENTS --approve --body "$(cat <<'EOF'
## Code Review: Approved

[Summary from report]

### Highlights

[Praise items if any, or general positive comments]

### Minor Suggestions (Optional)

[Non-critical suggestions if any]

---
*Reviewed with Claude Code*
EOF
)"
```

### For Request Changes (Choice 2)

```bash
gh pr review $ARGUMENTS --request-changes --body "$(cat <<'EOF'
## Code Review: Changes Requested

[Summary from report]

### Critical Issues

[List all critical issues with file:line references]

### Additional Suggestions

[Other suggestions if any]

---
*Reviewed with Claude Code*
EOF
)"
```

### For Comment (Choice 3)

```bash
gh pr review $ARGUMENTS --comment --body "$(cat <<'EOF'
## Code Review: Feedback

[Summary from report]

### Questions

[Questions that need clarification]

### Suggestions

[Suggestions for improvement]

---
*Reviewed with Claude Code*
EOF
)"
```

### For Cancel (Choice 4)

- Display: "Review cancelled. No submission made."
- End execution

## Step 12: Confirmation

After successful submission, display:

```
Review Submitted Successfully

PR: #[number] - [title]
URL: [pr url]
Review Type: [Approved / Changes Requested / Comment]

Your review has been posted to the pull request.
```

## Error Handling Reference

Throughout execution, handle these error cases:

| Error Condition | Message |
|----------------|---------|
| gh CLI not installed | "Error: GitHub CLI (gh) not installed. Install from https://cli.github.com/" |
| Not authenticated | "Error: Not authenticated with GitHub. Run `gh auth login` to authenticate." |
| Not in GitHub repo | "Error: Not in a git repository with a GitHub remote." |
| PR not found | "Error: Pull Request #[number] not found in this repository" |
| Invalid PR number | "Error: Invalid PR number. Usage: /review-pr <pr-number>" |
| No argument provided | "Error: No PR number provided. Usage: /review-pr <pr-number>" |
| Permission denied | "Error: You do not have permission to review this PR. Check your repository access." |
| Network error | "Error: Unable to reach GitHub. Check your internet connection and try again." |
| Review submission failed | "Error: Failed to submit review. [gh error message]" |

Always provide actionable guidance when an error occurs.
