# Reconstruye DOCX + PDF y renderiza todas las páginas a PNG (tools/doc_render).
$ErrorActionPreference = 'Continue'
$root = 'C:\Users\eduar\Downloads\deepseek_test\coach-basket'
$py = 'C:\Users\eduar\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe'
$node = 'C:\Users\eduar\AppData\Local\Programs\DeepSeek Harness\resources\runtime\primary-runtime\dependencies\node\bin\node.exe'
$cli = 'C:\Users\eduar\AppData\Local\Programs\DeepSeek Harness\resources\app.asar.unpacked\dsh\node_modules\@deepseek-ai\libreoffice-kit\lib\cli.js'

& $py "$root\tools\doc_build.py"
if ($LASTEXITCODE -ne 0) { Write-Host "BUILD FAILED"; exit 1 }

$pdf = "$root\docs\Propuesta_Landing_Coach_Basketball.pdf"
Remove-Item $pdf -Force -ErrorAction SilentlyContinue
& $node $cli convert --input "$root\docs\Propuesta_Landing_Coach_Basketball.docx" --output $pdf
if (-not (Test-Path $pdf)) { Write-Host "CONVERT FAILED"; exit 1 }

Remove-Item -Recurse -Force "$root\tools\doc_render" -ErrorAction SilentlyContinue
$manifest = & $node $cli render --input $pdf --output-dir "$root\tools\doc_render"
$j = $manifest | ConvertFrom-Json
Write-Host "PAGES=$($j.pageCount)  MISSING_FONTS=$($j.missingFonts -join ',')"
$j.images | ForEach-Object { "{0,2}  {1,4} KB" -f $_.page, [math]::Round($_.byteLength / 1024) }
