$pptxPath = "c:\Users\HP\Downloads\The Decision Completeness Engine\HackSprint_Decision_Completeness_Engine.pptx"
$pdfPath = "c:\Users\HP\Downloads\The Decision Completeness Engine\HackSprint_Decision_Completeness_Engine.pdf"

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    Write-Host "PowerPoint COM initialized."
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # 32 = ppSaveAsPDF
    $pres.SaveAs($pdfPath, 32)
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    Write-Host "SUCCESS: PDF created at $pdfPath"
} catch {
    Write-Host "Error: " $_.Exception.Message
}
