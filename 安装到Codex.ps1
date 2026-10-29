$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
if ($null -eq $codexCommand) {
    throw '未发现 Codex CLI。请先在有 Codex CLI 的电脑运行，或按开始使用.md导入本地插件。'
}
$marketplaceRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $marketplaceRoot '.agents\plugins\marketplace.json'))) {
    throw '包不完整：缺少本地 marketplace.json。请完整解压后重试。'
}
Write-Host '注册观象知易本地来源。若同名来源已存在，请检查其位置，不要覆盖其他来源。'
& $codexCommand.Source plugin marketplace add $marketplaceRoot --json
if ($LASTEXITCODE -ne 0) { throw '来源注册未成功。若已注册，请直接运行开始使用.md中的 plugin add 命令。' }
& $codexCommand.Source plugin add 'guanxiang-divination@guanxiang-local' --json
if ($LASTEXITCODE -ne 0) { throw '插件安装未成功，请检查上面的Codex错误。' }
Write-Host '安装完成。下一轮对话使用 $guanxiang-divination；若未刷新，重新打开Codex。'
