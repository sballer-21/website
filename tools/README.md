# tools/

Not part of the website. These files exist so the constitution page and the
downloadable PDF stay in agreement.

## The constitution lives in three places

| Where | What it is |
|---|---|
| `tools/constitution.md` | **The source.** Edit this first. |
| `constitution.shtml` | The web page — hand-written HTML mirroring the source |
| `TauBetaPiConstitution.pdf` | The download link at the foot of that page |

Before October 2026, the PDF still said a $50 initiation fee and a 5-member
minimum while the page had moved on. Anyone who clicked "Download PDF" got
different rules from the ones they had just read. Hence this folder.

## When the constitution changes

1. Update `tools/constitution.md` with the newly adopted text, including the
   `Updated: <date>` line.
2. Regenerate the PDF:

   ```bash
   python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install reportlab
   /tmp/pdfenv/bin/python tools/make_constitution_pdf.py \
       tools/constitution.md TauBetaPiConstitution.pdf
   ```

3. Update `constitution.shtml` to match. It is hand-written rather than
   generated, so this step is manual — work through the source article by
   article.
4. Check the page and the PDF agree on the numbers that tend to change: the
   initiation fee, the membership minimum, and the vote thresholds.

Keeping the page hand-written is deliberate: it uses the site's own markup and
Foundation classes, and generating it would mean generating the whole template.
