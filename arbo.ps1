# Fichier : generate-tree.ps1

$startPath = Get-Location
$outputFile = "arborescence.txt"

function Show-Tree {
    param (
        [string]$path,
        [int]$level = 0
    )

    $prefix = "|  " * $level

    Get-ChildItem -LiteralPath $path -Force | Where-Object {
        $_.Name -notmatch '^(node_modules|\.git|dist|build|vendor)$'
    } | ForEach-Object {
        Add-Content -Path $outputFile -Value ("$prefix|-- $($_.Name)")

        if ($_.PSIsContainer) {
            Show-Tree -path $_.FullName -level ($level + 1)
        }
    }
}


# Supprimer l'ancien fichier s'il existe
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

# Ajouter le dossier racine
Add-Content -Path $outputFile -Value "."
Show-Tree -path $startPath

Write-Host "`n✅ Arborescence générée avec succès dans '$outputFile'"
