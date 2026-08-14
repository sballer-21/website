# TBP Website — Webmaster Guide

**MIT Tau Beta Pi, Massachusetts Beta**
Last updated: August 11, 2026

This is the only document you need to run the website. It assumes no prior
knowledge of the site, of Athena, or of git. If something here is wrong or has
drifted, fix it here rather than starting a new document — that is how the
chapter ended up with a decade of scattered notes.

---

## 1. The thirty-second version

| | |
|---|---|
| **Live site** | https://web.mit.edu/tbp/www/ |
| **Lives on** | Athena, in the chapter's AFS locker `/mit/tbp/www` |
| **Source of truth** | GitHub — see §3 |
| **Built with** | Server Side Includes (SSI). No build step, no framework. |
| **Deployed by** | `git pull` on Athena. The working tree *is* the live site. |
| **Changes appear** | Instantly at origin; up to **1 hour** through MIT's CDN |

There is no build system, no CI, no npm, no static site generator. You edit
HTML, you push it, you pull it on Athena. That is the whole pipeline.

---

## 2. Access you need

Get all three before you start. The first two take time to arrange.

**1. An Athena account.** You have one if you're an MIT student — it's your
Kerberos username (the thing before `@mit.edu`).

**2. Membership in `system:tbp-officers`.** This is the AFS group that grants
write access to the locker. Without it you can read the site but not change
it. An existing member adds you:

```bash
blanche tbp-officers -a YOUR_KERBEROS_USERNAME
```

Check whether it worked:

```bash
blanche tbp-officers | grep YOUR_KERBEROS_USERNAME
```

If nobody left in the chapter is a member, IS&T can restore access — contact
them at `computing-help@mit.edu` and reference the locker name `tbp`.

**3. A GitHub account** with access to the chapter's repository. See §3 — the
ownership situation there needs attention and is the one genuinely unresolved
piece of the setup.

---

## 3. Where the code lives

Three copies exist. Keep them in sync.

| Copy | Location | Role |
|---|---|---|
| **Your laptop** | wherever you clone it | Where you edit |
| **GitHub** | `github.com/Tau-Beta-Pi-MIT/website` | Canonical history |
| **Athena** | `/mit/tbp/www` | The live site |

**A note on the GitHub situation.** The chapter's org repository is
`Tau-Beta-Pi-MIT/website`. As of the 2026 reboot, the sitting president had
only *read* access to it, because org ownership sat with alumni who had
graduated. The 2026 work was therefore published from a personal fork
(`sballer-21/website`) rather than the org repo.

**This should be fixed rather than inherited.** Ask a current org owner to
grant the sitting webmaster **owner** rights — not just write — so this doesn't
recur every time a class graduates. Until it is fixed, the fork holds commits
the org repo does not, and you must know which remote you're pushing to.

Remote names differ by machine, which is a reliable source of confusion:

| Machine | Remote name | Points at |
|---|---|---|
| Laptop | `origin` | the org repo |
| Laptop | `fork` | the personal fork |
| **Athena** | **`tbp_origin`** | the org repo |

On Athena the remote is **not** called `origin`. Commands copied from your
laptop will fail there until you change the remote name.

---

## 4. First-time setup

### 4a. Clone the repository

```bash
git clone https://github.com/Tau-Beta-Pi-MIT/website.git
cd website
```

### 4b. Preview it locally

The site uses Server Side Includes, which a plain file-open cannot render — if
you double-click `index.shtml` you'll see an unassembled page. Use the bundled
preview server instead:

```bash
python3 ssi_server.py
```

Then open **http://localhost:8000**. Stop it with `Ctrl+C`. This renders the
includes exactly as Athena's Apache does, so what you see is what you'll ship.

### 4c. Set up passwordless-ish Athena access

Athena accepts a Kerberos ticket but still requires a Duo push, so it cannot be
made fully non-interactive. Connection multiplexing gets you down to
authenticating **once** per session instead of once per command.

Add this to `~/.ssh/config` on your laptop, replacing the username:

```
Host athena athena.dialup.mit.edu
    HostName athena.dialup.mit.edu
    User YOUR_KERBEROS_USERNAME
    GSSAPIAuthentication yes
    GSSAPIDelegateCredentials yes
    ControlMaster auto
    ControlPath ~/.ssh/cm-athena.sock
    ControlPersist 4h
```

Then, once per work session:

```bash
kinit YOUR_KERBEROS_USERNAME@ATHENA.MIT.EDU
ssh athena
```

Approve the Duo push. That connection stays alive for four hours and every
later `ssh athena` reuses it silently.

- Tickets last about 10 hours — `klist` shows the expiry. Re-run `kinit` when
  it lapses.
- Check the shared connection: `ssh -O check athena`
- Close it deliberately: `ssh -O exit athena`

---

## 5. Making a change

The full loop, start to finish.

**1. Edit on your laptop.** Find the right file using §6.

**2. Preview.**

```bash
python3 ssi_server.py     # visit localhost:8000
```

Check the page you changed *and* the home page, since most content lives in
shared includes and a change can surface in more than one place.

**3. Commit and push.**

```bash
git add -A
git commit -m "Describe what changed and why"
git push origin main-branch-name
```

**4. Deploy on Athena.**

```bash
kinit YOUR_USERNAME@ATHENA.MIT.EDU
ssh athena
cd /mit/tbp/www
git pull tbp_origin BRANCH
```

**5. Verify.** See §8 — this step is not optional, and there is a specific way
to do it correctly.

---

## 6. How the site is put together

### The include system

Every page is a `.shtml` file that pulls in shared fragments:

```html
<!--#include virtual="includes/header.htm"-->
<!--#include virtual="includes/nav.htm"-->
   ... page content ...
<!--#include virtual="includes/footer.htm"-->
```

Apache assembles these at request time. **Editing one include changes every
page that uses it** — this is a feature, but it means the footer is edited once
rather than ten times.

### Where things are

| File | What it controls |
|---|---|
| `index.shtml` | Home page. Assembles the About / Officers / Contact sections. |
| `includes/header.htm` | `<head>`, stylesheets, page title |
| `includes/nav.htm` | Navigation bar on subpages |
| `includes/home-nav.htm` | Navigation bar on the home page |
| `includes/footer.htm` | Footer, copyright year, **accessibility link** |
| `includes/pages/about.htm` | "About" section of the home page |
| `includes/pages/officers.htm` | **Officer roster** — see §7 |
| `includes/pages/contact.htm` | Contact section and the email button |
| `includes/pastofficers/` | One file per year of past rosters |
| `includes/davincilectures/` | One file per semester of lecture listings |
| `stylesheets/app.css` | All custom styling. Everything else is vendor CSS. |
| `images/officers/` | Officer headshots |

Standalone pages: `advisor.shtml`, `commserve.shtml`, `constitution.shtml`,
`davincilectures.shtml`, `eligibles.shtml`, `events.shtml`,
`pastofficers.shtml`, `tutoring.shtml`.

`stylesheets/foundation*.css` and `javascripts/foundation*.js` are ZURB
Foundation 3, a vendor framework from the original build. **Don't edit them** —
your changes belong in `app.css`, which loads afterwards and overrides.

---

## 7. Common tasks

### Update the officer roster

This is the most frequent job, and it has a trap.

**`includes/pages/officers.htm` lists every officer twice** — once in a table
shown on phones (`id='officer-table'`), and once as the photo cards shown on
desktop. **You must edit both.** If you change only one, the site will show
different rosters depending on screen size, and it will look correct on
whichever device you happen to test.

For each officer you need: name, class year, position, headshot, and a
description of the role.

**Adding a headshot:**

1. Name the file `firstname-lastname.jpg`, all lowercase, hyphen-separated, in
   `images/officers/`. Filenames are **case-sensitive** on the server.
2. Aim for roughly **500×500 pixels**, square. Non-square images are cropped by
   CSS (`object-fit: cover`) rather than squashed, but a head sitting far off
   centre may be cropped badly — check the preview.
3. Reference it with a **relative** path and real alt text:

```html
<img src='images/officers/firstname-lastname.jpg' alt='Firstname Lastname, Position'/>
```

Alt text is an accessibility requirement, not a nicety. Describe who and what,
not "photo".

**At the end of the year**, move the outgoing roster into
`includes/pastofficers/YYYY-YYYY.htm` (copy the structure of an existing file)
and add it to `pastofficers.shtml`.

### Update the footer year

`includes/footer.htm`, one place, all ten pages.

### Add a new page

1. Copy an existing simple page — `tutoring.shtml` is a good template.
2. Keep the `<!--#include-->` lines for header, nav, and footer.
3. Add a link in **both** `includes/nav.htm` and `includes/home-nav.htm`.
4. Use **relative** URLs (`events.shtml`), never absolute
   (`http://web.mit.edu/tbp/www/events.shtml`). Absolute URLs break local
   preview and break again if the site ever moves hosts. This has bitten the
   site before.

### Retire a page

Delete the file, remove it from both nav includes, and grep for stragglers:

```bash
grep -rn "pagename.shtml" --include="*.shtml" --include="*.htm" .
```

Deleting is better than hiding. Anything left in the repository is publicly
fetchable once deployed — `robots.txt` will not save you (see §10).

---

## 8. Verifying a deploy — read this before you panic

MIT's web servers sit behind **Akamai**, a CDN that caches pages for about an
hour. This produces a specific and very confusing symptom: **the site looks
half-updated**, with some pages new and others stale.

That is normal and it resolves itself. It is not a broken deploy.

**Check the plain URL, exactly as a visitor would:**

```bash
curl -s "https://web.mit.edu/tbp/www/" | grep -oE "<title>[^<]*"
```

**Do not add a cache-busting query string** (`?v=123`) when verifying. It
bypasses the CDN and tells you only that the origin server is fine — which
means you can "verify" a deploy that visitors still can't see. This exact
mistake produced a false all-clear during the 2026 reboot.

In the browser, hard-refresh with **`Cmd+Shift+R`** and navigate to the URL
directly rather than clicking a Google result.

**If it's still stale after an hour**, something is genuinely wrong. Only IS&T
can purge the Akamai cache — email `computing-help@mit.edu`.

**Google results lag much longer** — days to weeks — because the search index
updates on Google's own crawl schedule. Nothing you do on the server changes
that.

### Rolling back

The live site is a git working tree, so rollback is a checkout:

```bash
cd /mit/tbp/www
git log --oneline -10        # find the last good commit
git checkout BRANCH_OR_COMMIT
```

---

## 9. Athena gotchas that will cost you an afternoon

**Never run `git stash` in `/mit/tbp/www`.** That working tree is the live
website. Stashing reverts the public site instantly.

**Check `git status` before pulling.** Previous webmasters have left
uncommitted work sitting in the live tree for years. A pull that conflicts with
it will either fail or destroy it. If you find uncommitted changes, preserve
them on a branch first:

```bash
cd /mit/tbp/www
git status
git checkout -b rescue-YYYY-description
git add -A && git commit -m "Preserve uncommitted work found in live tree"
```

**The remote is `tbp_origin`, not `origin`.**

**If git refuses to run, complaining about dubious ownership:**

```bash
git config --global --add safe.directory /afs/athena.mit.edu/activity/t/tbp/www
```

AFS ownership confuses git's safety check. This is harmless to add.

**Watch the disk quota.** The locker is not large and the site has run near the
limit before:

```bash
fs listquota /mit/tbp
```

Large media does not belong in the repository. Put it in the private area (§10)
or on Google Drive and link to it.

---

## 10. Security and privacy — the part that matters most

The 2026 cleanup existed because IS&T found chapter content exposed on the
public internet. The specifics are recorded in the chapter's private status
document; what follows is what you need to *not repeat it*.

### Understand what "public" means here

AFS controls access with per-directory ACLs. The web server reads as the
special user **`system:anyuser`**. So:

> **If a directory grants `system:anyuser` any rights, everything in it is on
> the public internet.**

Inspect a directory:

```bash
fs listacl /mit/tbp/www
```

`system:anyuser rl` means world-readable. Remove that where it doesn't belong:

```bash
fs setacl -dir DIRECTORY -acl system:anyuser none
```

**ACLs are per-directory and are not inherited.** Moving a folder somewhere
private does *not* re-secure its subdirectories. Always check afterwards:

```bash
find DIRECTORY -type d -exec fs listacl {} \; | grep -B3 anyuser
```

### The rules

1. **Never commit personal data.** No resumes, no rosters with contact details,
   no member lists, no application materials. Anything committed is public and
   stays in git history even after deletion.
2. **Never commit credentials.** No passwords, API keys, or database configs.
   A password in a public repository is burned permanently — rotate it, don't
   just delete the line.
3. **`robots.txt` does nothing here.** Crawlers only read it from a domain
   root, and the site is served from a subdirectory of `web.mit.edu`. To keep
   something out of search results, remove it — do not rely on that file.
4. **Sensitive material goes in `/mit/tbp/private/`**, which has no
   `system:anyuser`. Not in the web tree, not "unlinked but present."
5. **Audit annually.** See §12.

### Two specific things to leave alone

**Don't remount `OldFiles`.** AFS keeps a nightly backup volume that can be
mounted inside the locker as `OldFiles`. It is world-readable and read-only, so
its permissions cannot be fixed — while mounted, it publicly serves a complete
snapshot of the old site, *including* anything you thought you had removed. The
mountpoint was deliberately removed in August 2026. The backups still exist and
IS&T can restore from them. Do not run `fs mkmount /mit/tbp/OldFiles`.

**Keep `.git` unreadable.** The live site's own repository directory sits
inside the web root. If it grants `system:anyuser`, standard tooling can
reconstruct the entire history — including every file ever deleted. Verify:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://web.mit.edu/tbp/www/.git/config
```

You want **403**. If you get 200:

```bash
fs setacl -dir /mit/tbp/www/.git -acl system:anyuser none
```

---

## 11. Site conventions

Keep these when editing so the site stays coherent and compliant.

**Colour.** MIT Red is **`#750014`** (per brand.mit.edu/color — it was changed
in a brand refresh, and older values like `#A31F34` are out of date). Use it on
light backgrounds only.

**Contrast.** MIT Red on the dark footer measures about 1.5:1, far below the
WCAG AA minimum of 4.5:1. **On dark backgrounds, use white.** If you introduce
a new colour pairing, check it with a contrast checker first. This is a real
accessibility requirement, not a preference.

**The accessibility link is mandatory.** Every MIT site must link to
accessibility.mit.edu. It lives in `includes/footer.htm` and therefore appears
on every page. **Do not remove it.**

**Video and audio must be captioned.** MIT's agreement with the National
Association of the Deaf requires captions on published media. The site
currently has none, which is why nothing is captioned. If you add a video,
caption it *when you post it* — retrofitting is how backlogs form.

**Alt text on every meaningful image.**

**No MIT logo.** Logo use is restricted by brand.mit.edu. The site's identity
is typographic by design.

**Relative URLs only.** See §7.

---

## 12. Annual checklist

Do this at officer transition, every year. It takes under an hour and prevents
every problem described in this document.

- [ ] Update the officer roster — **both** halves of `officers.htm` (§7)
- [ ] Move last year's roster into `includes/pastofficers/`
- [ ] Update the copyright year in `includes/footer.htm`
- [ ] Add the incoming webmaster to `system:tbp-officers`
- [ ] **Remove graduated officers** from `system:tbp-officers` and from any
      individual ACL entries — stale write access to the live site has
      persisted for years at a time
- [ ] Confirm the sitting webmaster has GitHub **owner** rights (§3)
- [ ] Check quota: `fs listquota /mit/tbp`
- [ ] Confirm `.git` returns 403 (§10)
- [ ] Scan for exposure: `fs listacl` on every locker directory; confirm only
      `www` grants `system:anyuser`
- [ ] Click every nav link and check for broken images
- [ ] Remove content for programs no longer running
- [ ] Hand this document to your successor, updated

**Checking who has access:**

```bash
blanche tbp-officers          # group membership
fs listacl /mit/tbp/www       # individual grants on the live site
```

Individual entries accumulate outside the group and are easy to miss. Look at
both.

---

## 13. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Site looks half-updated | Akamai cache | Wait an hour; verify per §8 |
| Change not live after an hour | Didn't pull on Athena, or pulled the wrong branch | `cd /mit/tbp/www && git log --oneline -3` |
| Google shows old content | Search index lag | Wait; nothing to fix server-side |
| Page shows raw `<!--#include-->` | Opened the file directly | Use `python3 ssi_server.py` |
| Includes missing in preview | Renamed a `.shtml` to `.html` | Keep the `.shtml` extension |
| Broken images after a rename | Case mismatch | Filenames are case-sensitive; match exactly |
| Roster differs on phone vs laptop | Edited only one half of `officers.htm` | §7 |
| `Permission denied` on Athena | Not in `system:tbp-officers`, or expired ticket | `blanche tbp-officers`; re-run `kinit` |
| git: "dubious ownership" | AFS ownership | `safe.directory` command in §9 |
| `fs: You don't have the required access rights` | Missing admin bit on that directory | Ask a member with `a` rights, or IS&T |
| Site suddenly reverted | Someone ran `git stash` or checked out an old commit | `git log --oneline`, check out the right commit |

---

## 14. Who to contact

| For | Contact |
|---|---|
| Athena, lockers, ACLs, DNS, CDN purges | `computing-help@mit.edu` |
| Web accessibility | accessibility.mit.edu |
| Branding | brand.mit.edu |
| Student group administration | ASA — `asa-exec@mit.edu` |
| Chapter officers | `tbp-officers@mit.edu` |

---

## 15. History worth knowing

The site was built around 2011–2013 on ZURB Foundation 3 and maintained
sporadically until roughly 2021, after which it went dormant. In August 2026,
IS&T contacted the chapter about content that had escaped onto the public
internet and asked for a cleanup under threat of taking the locker offline.

The resulting reboot removed a career fair that was no longer running, a
fellowships page still advertising a 2022 deadline, a member portal wired to a
dead API, a contact form posting to a server that no longer existed, a 2013
photo gallery, and roughly ninety orphaned images. Locker usage fell from 79%
to 59% of quota. The site was brought up to current MIT branding and
accessibility requirements, and several directories that were publicly readable
by accident were closed.

**The lesson worth carrying forward:** none of that was one person's mistake.
It accumulated because nobody looked for years, and because each webmaster
inherited scattered notes instead of a single current document. The annual
checklist in §12 exists to break that cycle. Twenty minutes a year is the whole
cost.

Keep this document current. Then delete the old notes.
