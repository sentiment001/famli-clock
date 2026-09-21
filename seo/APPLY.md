# How to get this into sentiment001/famli-clock

The session that built this could clone and read the repo but the sandbox proxy refused
every write, with or without a personal access token: *"not in this session's authorized
repository set"*. So the commit exists, fully built and tested, but unpushed.

Three ways to land it, easiest first.

## 1. The bundle, if you want the exact commit with its message

`famliclock-seo.bundle` carries one commit on top of `9aa35dc`.

```bash
git clone https://github.com/sentiment001/famli-clock.git
cd famli-clock
git fetch /path/to/famliclock-seo.bundle main:seo-build
git merge --ff-only seo-build
git push origin main
```

`--ff-only` will refuse if `main` has moved since `9aa35dc`. If it does, see section 3.

## 2. Copy the files, if the bundle is inconvenient

Everything in `site/` goes to the repo root. Everything in `source/` goes to `seo/`.
Then add `seo` to `.vercelignore`, add the `Cache-Control` key to the catch-all block in
`vercel.json` (both shown in PUSH_ORDER.md section 2 and 3), and regenerate `version.txt`:

```bash
printf 'sha256 %s\nbytes  %s\nbuilt  %s\n' \
  "$(sha256sum index.html | cut -d' ' -f1)" "$(wc -c < index.html)" \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > version.txt
```

**Read PUSH_ORDER.md section 1 before you copy `index.html` over anything.**

## 3. If main has moved since 9aa35dc

Do not paste `site/index.html` over a newer file. Rebuild it:

```bash
node seo/run_examples.js index.html > seo/examples.json
python3 seo/build.py --out .
python3 seo/patch_index.py --in index.html --out index.html
python3 seo/qa.py --dir .
node seo/browser_qa.js .
```

The patcher asserts every anchor, so it either applies cleanly to the newer file or names
the anchor that moved. It never half-applies.

## Then, in this order

1. Confirm the tool still works: 12 / 12 / 780000 / biweekly returns a 2027 total of
   **$3,510.00** at 0.45%.
2. Confirm the H1 **after the app has loaded** still reads "Maryland FAMLI calculator: …".
   Check again after 29 September, when the phase changes and a different string paints.
3. Confirm the print report is still five sheets, with the nav and the new content block
   absent from the preview.
4. Add the Google Search Console property and submit `sitemap.xml`.
5. Fetch `famliclock.com/robots.txt` and confirm it is the file from this build and not
   Cloudflare's managed one. On 21 September 2026 it was Cloudflare's.
