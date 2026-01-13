$ErrorActionPreference = "Stop"

$input_json = [Console]::In.ReadToEnd()
$data = $input_json | ConvertFrom-Json
$command = $data.tool_input.command

if (-not $command) { exit 0 }

function Deny-Heredoc {
    $denial = @{
        hookSpecificOutput = @{ permissionDecision = "deny" }
        systemMessage = "BLOCKED: Creating files via heredoc is forbidden. Use TodoWrite for task tracking, or use the Write tool for legitimate file creation. See CLAUDE.md."
    }
    $denial | ConvertTo-Json -Compress | Write-Error
    exit 2
}

# Check for heredoc marker pattern
$heredocPattern = '<<-?\s*[''"]?[A-Za-z_][A-Za-z0-9_]*[''"]?'
$hasHeredoc = $command -match $heredocPattern

if ($hasHeredoc) {
    # Pattern 1: cat/tee with heredoc and file redirect
    if ($command -match '^\s*(cat|tee)\s') {
        if ($command -match '>\s*[A-Za-z0-9_./-]') { Deny-Heredoc }
        if ($command -match 'tee\s+[A-Za-z0-9_./-]') { Deny-Heredoc }
    }

    # Pattern 2: Pipe to tee
    if ($command -match '\|\s*tee\s+[A-Za-z0-9_./-]') { Deny-Heredoc }

    # Pattern 3: Any heredoc writing to planning-like files
    if ($command -match '\.(md|txt|log|json)[\s"''>]' -or $command -match '\.(md|txt|log|json)$') {
        Deny-Heredoc
    }
}

exit 0
