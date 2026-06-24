param([string]$Url, [string]$OutDir, [string]$Id)
# fetch.ps1 - Windows/PowerShell HTML fetcher for semantic-stack skill
# Usage: .\fetch.ps1 -Url <URL> -OutDir <path> -Id <01..NN>
# Outputs four files in $OutDir: title_$Id.txt, h1_$Id.txt, h2_$Id.txt, raw_$Id.txt

try {
  $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -TimeoutSec 30
  $html = $r.Content

  # Title
  if ($html -match '(?is)<title[^>]*>(.*?)</title>') {
    $matches[1].Trim() | Out-File -Encoding utf8 "$OutDir\title_$Id.txt"
  }

  # H1s
  $h1s = [regex]::Matches($html, '(?is)<h1[^>]*>(.*?)</h1>') |
    ForEach-Object { ($_.Groups[1].Value -replace '<[^>]+>',' ' -replace '\s+',' ').Trim() }
  $h1s | Out-File -Encoding utf8 "$OutDir\h1_$Id.txt"

  # H2s
  $h2s = [regex]::Matches($html, '(?is)<h2[^>]*>(.*?)</h2>') |
    ForEach-Object { ($_.Groups[1].Value -replace '<[^>]+>',' ' -replace '\s+',' ').Trim() }
  $h2s | Out-File -Encoding utf8 "$OutDir\h2_$Id.txt"

  # Body text (strip HTML)
  $text = $html -replace '<script[^>]*?>[\s\S]*?</script>','' `
                -replace '<style[^>]*?>[\s\S]*?</style>','' `
                -replace '<nav[^>]*?>[\s\S]*?</nav>','' `
                -replace '<footer[^>]*?>[\s\S]*?</footer>','' `
                -replace '<header[^>]*?>[\s\S]*?</header>','' `
                -replace '<noscript[^>]*?>[\s\S]*?</noscript>','' `
                -replace '<[^>]+>',' ' `
                -replace '&nbsp;',' ' `
                -replace '&amp;','&' `
                -replace '&quot;','"' `
                -replace '&#39;',"'" `
                -replace '&lt;','<' `
                -replace '&gt;','>' `
                -replace '\s+',' '
  $text | Out-File -Encoding utf8 "$OutDir\raw_$Id.txt"

  $words = ($text -split '\s+' | Where-Object { $_ -ne '' }).Count
  "OK $($r.StatusCode) $words ord, H1:$($h1s.Count), H2:$($h2s.Count) -> $Id"
} catch {
  "FAIL $Url : $($_.Exception.Message)"
}
