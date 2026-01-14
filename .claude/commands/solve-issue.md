---
description: "Fetch a GitHub issue and solve it"
argument-hint: "<issue-number>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(gh:*)
  - Bash(git:*)
  - Bash(uv:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - TodoWrite
  - AskUserQuestion
model: sonnet
---

# Solve GitHub Issue

You are tasked with fetching a GitHub issue and implementing a solution for it.

## Step 1: Validate Argument

Check that an issue number was provided:

```
Issue number: $ARGUMENTS
```

If `$ARGUMENTS` is empty or not provided:
- Display: "Error: No issue number provided. Usage: /solve-issue <issue-number>"
- Stop execution immediately

If `$ARGUMENTS` is not a valid number:
- Display: "Error: Invalid issue number. Usage: /solve-issue <issue-number>"
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

## Step 3: Fetch Issue Details

Run the following command to fetch issue details:

```bash
gh issue view $ARGUMENTS --json number,title,body,author,labels,assignees,state,comments,url
```

If the issue is not found:
- Display: "Error: Issue #$ARGUMENTS not found in this repository"
- Stop execution

Parse the JSON response and extract all fields.

## Step 4: Present Issue Context

Display the issue information in a clear format:

```
## Issue #[number]: [title]

**URL:** [url]
**Author:** [author.login]
**State:** [state]
**Labels:** [labels as comma-separated list, or "None"]
**Assignees:** [assignees as comma-separated list, or "Unassigned"]

### Description

[body content]

### Comments

[If comments exist, display each comment with author and body]
[If no comments, display "No comments"]
```

## Step 5: Create Todo List

Analyze the issue body for actionable items:

1. **Parse checklist items**: Look for `- [ ]` or `- [x]` patterns in the issue body
2. **Parse numbered tasks**: Look for numbered list items (1. 2. 3. etc.)
3. **Extract task descriptions**: Pull the text from each item found

Use TodoWrite to create a structured todo list with:

1. All checklist/numbered items found in the issue body (if any)
2. Add these standard workflow items:
   - "Analyze codebase to understand relevant files and architecture"
   - "Implement changes following project conventions"
   - "Run tests to verify implementation"
   - "Verify solution meets issue requirements"

Mark the first item as `in_progress` when starting work.

## Step 6: Read Project Guidelines

Check for and read project guidelines to understand coding standards:

### Global Instructions
Check if `~/.claude/CLAUDE.md` exists. If it does, read it to understand global coding standards and conventions.

### Project Instructions
Check if `./CLAUDE.md` exists in the current directory. If it does, read it to understand project-specific:
- Coding guidelines
- Test requirements
- Commit format conventions
- Quality gates
- Any special instructions

These files contain critical information about how to write code for this project. Follow all conventions specified.

## Step 7: Solving Workflow

### 7.1 Explore the Codebase

- Use Glob to find relevant files based on the issue description
- Use Grep to search for related code patterns, functions, or classes mentioned in the issue
- Read relevant files to understand the current implementation
- Identify all files that need modification

### 7.2 Implement Changes

Following the conventions from CLAUDE.md files:

- Make necessary code changes using Edit or Write tools
- Follow the coding style and patterns used in the project
- Add appropriate type hints if the project requires them
- Add docstrings for any new public functions
- Ensure code is portable across platforms (Linux, Windows, macOS) if required

### 7.3 Run Tests

Execute the project's test suite to verify changes:

- For Python projects: `uv run pytest` or `pytest`
- For Node projects: `npm test`
- Check for any test failures and fix them

If tests fail:
- Analyze the failure
- Fix the issue
- Re-run tests until they pass

### 7.4 Update Progress

As you complete each task:
- Update the todo list using TodoWrite
- Mark completed items as `completed`
- Mark the current task as `in_progress`
- Add any new tasks discovered during implementation

## Step 8: Completion

### Summarize Implementation

Provide a clear summary of:
- What files were modified
- What changes were made
- How the changes address the issue requirements
- Test results

### Offer Next Actions

Use AskUserQuestion to ask the user what they would like to do next:

```
The issue has been solved. What would you like to do next?

1. **Create a commit** - I'll create a commit with a conventional commit message (feat/fix/docs/etc.) summarizing the changes
2. **Add issue comment** - I'll add a comment to the GitHub issue summarizing what was implemented
3. **Close the issue** - I'll close the issue (can be combined with adding a comment)
4. **Review changes first** - Show a diff of all changes before committing
5. **Nothing for now** - End without any git/GitHub actions

Please specify your choice (or multiple choices, e.g., "1 and 3"):
```

Based on user response:

- **For commit**: Use `git add` and `git commit` with conventional commit format from CLAUDE.md (feat:, fix:, docs:, test:, refactor:, chore:)
- **For issue comment**: Run `gh issue comment $ARGUMENTS --body "[summary of implementation]"`
- **For close issue**: Run `gh issue close $ARGUMENTS`
- **For review**: Run `git diff` to show all changes

## Error Handling Reference

Throughout execution, handle these error cases:

| Error Condition | Message |
|----------------|---------|
| gh CLI not installed | "Error: GitHub CLI (gh) not installed. Install from https://cli.github.com/" |
| Not authenticated | "Error: Not authenticated with GitHub. Run `gh auth login` to authenticate." |
| Not in GitHub repo | "Error: Not in a git repository with a GitHub remote." |
| Issue not found | "Error: Issue #[number] not found in this repository" |
| Invalid issue number | "Error: Invalid issue number. Usage: /solve-issue <issue-number>" |
| No argument provided | "Error: No issue number provided. Usage: /solve-issue <issue-number>" |

Always provide actionable guidance when an error occurs.
