#!/bin/bash
# fetch.sh - Unix/Bash HTML fetcher for semantic-stack skill (cross-platform equivalent of fetch.ps1)
# Usage: ./fetch.sh <URL> <OUTDIR> <ID>
# Requires: curl, perl (both preinstalled on macOS and most Linux distributions)
# Outputs four files in $OUTDIR: title_$ID.txt, h1_$ID.txt, h2_$ID.txt, raw_$ID.txt

set -u

URL="${1:-}"
OUTDIR="${2:-}"
ID="${3:-}"

if [ -z "$URL" ] || [ -z "$OUTDIR" ] || [ -z "$ID" ]; then
    echo "FAIL: missing arguments. Usage: fetch.sh <URL> <OUTDIR> <ID>"
    exit 1
fi

# Verify required tools
command -v curl >/dev/null 2>&1 || { echo "FAIL: curl not installed"; exit 1; }
command -v perl >/dev/null 2>&1 || { echo "FAIL: perl not installed"; exit 1; }

mkdir -p "$OUTDIR"

# Fetch HTML to temp file, capture HTTP status
TMP="$OUTDIR/_tmp_$ID.html"
STATUS=$(curl -sSL \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    --max-time 30 \
    -w "%{http_code}" \
    -o "$TMP" \
    "$URL" 2>/dev/null) || STATUS="000"

if [ "$STATUS" != "200" ] && [ "$STATUS" != "201" ] && [ "$STATUS" != "202" ]; then
    rm -f "$TMP"
    echo "FAIL $URL : HTTP $STATUS"
    exit 1
fi

# Title (first <title>...</title>)
perl -0777 -ne '
    if (/<title[^>]*>(.+?)<\/title>/is) {
        my $t = $1;
        $t =~ s/<[^>]+>/ /g;
        $t =~ s/\s+/ /g;
        $t =~ s/^\s+|\s+$//g;
        print "$t\n";
    }
' "$TMP" > "$OUTDIR/title_$ID.txt"

# H1s (one per line)
perl -0777 -ne '
    while (/<h1[^>]*>(.+?)<\/h1>/igs) {
        my $h = $1;
        $h =~ s/<[^>]+>/ /g;
        $h =~ s/\s+/ /g;
        $h =~ s/^\s+|\s+$//g;
        print "$h\n" if length($h);
    }
' "$TMP" > "$OUTDIR/h1_$ID.txt"

# H2s (one per line)
perl -0777 -ne '
    while (/<h2[^>]*>(.+?)<\/h2>/igs) {
        my $h = $1;
        $h =~ s/<[^>]+>/ /g;
        $h =~ s/\s+/ /g;
        $h =~ s/^\s+|\s+$//g;
        print "$h\n" if length($h);
    }
' "$TMP" > "$OUTDIR/h2_$ID.txt"

# Body text (strip HTML, decode entities, collapse whitespace)
perl -0777 -pe '
    s/<script[^>]*>.*?<\/script>//gis;
    s/<style[^>]*>.*?<\/style>//gis;
    s/<nav[^>]*>.*?<\/nav>//gis;
    s/<footer[^>]*>.*?<\/footer>//gis;
    s/<header[^>]*>.*?<\/header>//gis;
    s/<noscript[^>]*>.*?<\/noscript>//gis;
    s/<[^>]+>/ /g;
    s/&nbsp;/ /g;
    s/&amp;/&/g;
    s/&quot;/"/g;
    s/&#39;/\x27/g;
    s/&lt;/</g;
    s/&gt;/>/g;
    s/\s+/ /g;
' "$TMP" > "$OUTDIR/raw_$ID.txt"

rm -f "$TMP"

WORDS=$(wc -w < "$OUTDIR/raw_$ID.txt" | tr -d ' ')
H1_COUNT=$(grep -c . "$OUTDIR/h1_$ID.txt" 2>/dev/null || echo 0)
H2_COUNT=$(grep -c . "$OUTDIR/h2_$ID.txt" 2>/dev/null || echo 0)

echo "OK $STATUS $WORDS ord, H1:$H1_COUNT, H2:$H2_COUNT -> $ID"
