# MIT Athena Locker-hosted Website
Want to see these guides each on their own page?  Please check out our [wiki](https://github.com/Tau-Beta-Pi-MIT/website/wiki)!

## Overview
This repository contains HTML, CSS, and JavaScript code along with images for our website, hosted at [web.mit.edu/tbp/www](http://web.mit.edu/tbp/www/).  This code can be edited and pushed to our Athena server by individuals with appropriate credentials.

## Previewing locally
From the repository root:

```
python3 ssi_server.py
```

Then open <http://localhost:8000>.  The port is always 8000 — the script ignores any port argument.  `Ctrl-C` to stop.

**Caveat:** `includes/nav.htm` uses absolute `http://web.mit.edu/tbp/www/` links, so clicking nav links from a sub-page in local preview will take you to the *live* site.  Only `index.shtml` (which uses `home-nav.htm`) navigates locally.  To preview a sub-page, type its `localhost:8000` URL directly.

## Installation/Requirements
The only capabilities you'll need on your machine are `ssh` and `git`.  Once you have these set up, you'll be ready to make modifications to the site as you see fit!

## Navigating to our code on the Athena server
Our codebase is hosted in an MIT's athena locker, which is accessible through remote login via `ssh`.  You can navigate to our codebase on the Athena server by following these instructions:

1. Make sure you’re on the moira mailing list tbp-officers@mit.edu.

2. `ssh` into the Athena server: 

`ssh <kerb>@athena.dialup.mit.edu`

**PW**: your kerb password + Duo Authentication (1 for Duo Push)

3. Navigate to our directory where our codebase is hosted:

`cd /mit/tbp/www`

## Website Structure
At a high level, this website uses SSI, HTML, and CSS.  We'll discuss the specifics of how SSI and CSS are used to augment the repository's HTML.  

### Server Side Includes (SSI)
This website uses the [server side includes (SSI)](https://en.wikipedia.org/wiki/Server_Side_Includes) scripting language for formatting and repeating different blocks of html.  Code used for each web page (e.g. header, footer, navigation, home navigation) is contained in the `includes/` directory.  The contents of these files can be added to a separate `.shtml` web page through the following command:

`<!--#include virtual="includes/home-nav.htm"-->`

(In this case, the above command would include the code page for `home-nav.htm` in the new web page.)  If you plan on creating a new web page with a header, navigation bar, and footer, you should use the following piece of code as a template:

```
<!--#include virtual="includes/header.htm"-->
<!--#include virtual="includes/home-nav.htm"-->

<!--BODY OF CODE GOES HERE-->

<!--#include virtual="includes/footer.htm"-->
<!--#include virtual="includes/bottom.htm"-->
```

These commands are parsed using `ssi_server.py` and `ssi.py` in this repository.  It is strongly advised **NOT** to edit these SSI server files.  (Note: on the live Athena server, SSI is expanded by the web server itself — the Python scripts exist only for local preview.)

### CSS
CSS is also used throughout this codebase to format objects, text, and images.  The main sources of CSS can be found in `stylesheets/app.css` and `stylesheets/foundation.css`.

### Web Page Directories
The contents of the website's home page are given by `index.shtml`.  All other main navigation files (e.g. web pages) can be found in the same directory as `index.shtml`.  Files used as components of a web page (e.g. `officers.htm`) can be found in the `includes/pages/` directory.

## Eligibles portal (retired)
The site used to have a self-service eligibles portal (`eligibles_portal.shtml`, `eligibles_landing_page.shtml`) that read requirement progress from a published Google Sheet behind a single shared, hardcoded password.  It was **removed during the 2026 chapter reboot**: it was wired to a 2022 spreadsheet, and it used the Google Sheets v3 API, which Google shut down in 2021.

`eligibles.shtml` now simply says that eligibles are contacted by email each term.  The old files are recoverable from git history if the portal is ever rebuilt — but if it is, do not reintroduce a shared password committed to a public repo.

## Suggested workflow for making changes ([feature/branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)):
1. Create a branch on the GitHub repository for the feature you’d like to add (e.g. a button for logging tutoring hours):

`git checkout -b name_of_your_branch`

2. Make changes to this codebase on the new branch on your local machine.  Once you're ready to commit and push your changes:

`git add .`

`git commit -m "your_commit_statement"`

`git push -u origin name_of_your_branch`

3. Now navigate to the repository on the Athena server, by following the instructions in the section above ("Navigating to our code on the Athena server").  Once there, fetch the new branch using a git fetch of this syntax: `git fetch <remote-repo> <remote-branch>:<local-branch>` (give it the same name for simplicity):

`git fetch tbp_origin name_of_your_branch:name_of_your_branch`

**Two Athena gotchas:**

- The remote on the Athena checkout is named **`tbp_origin`**, not `origin`.  Run `git remote -v` there if in doubt — copying the `origin` commands from your laptop will fail.
- AFS ownership trips git's dubious-ownership check.  If git refuses to run, you need:

  `git config --global --add safe.directory /afs/athena.mit.edu/activity/t/tbp/www`

  (Already configured for `sballer`.)

**Also:** the Athena checkout's working tree *is* the live website.  Never `git stash` there — it would revert the live site.  If you find uncommitted changes on the server, commit them to a rescue branch before pulling.

4. Now checkout the new branch on the Athena server:

`git checkout name_of_your_branch`

5. Next, inspect the website at [web.mit.edu/tbp/www](http://web.mit.edu/tbp/www/) to make sure your changes appear as you'd expect and are free of bugs.  **NOTE**: Changes don't always appear immediately, so if nothing seems to have changed, give it a little more time.  You can also preview locally first — see "Previewing locally" above.

6. Once you're satisfied with how everything looks, perform a merge pull request on the GitHub repo (this is accomplished most effectively by just doing this through [GitHub online](https://github.com/)).  Integrate your new changes with the master branch (or have other members of the development team review your changes, and then pull) and then (on both your local machine and the Athena server), switch back to the master branch and pull:

`git checkout master`

`git pull`

7. Finally, after you pull again on both your local computer and the remote Athena server, verify that the website looks as you'd expect it to and is free of bugs!

## Site conventions

- **MIT red is `#A31F34`** ([brand.mit.edu](https://brand.mit.edu)).  Don't reintroduce the old `#b40132`.
- Every page must reach the footer through `includes/footer.htm`, which carries the required link to [accessibility.mit.edu](https://accessibility.mit.edu).  Don't inline a copy of the header or footer in a page — if a page needs its own `<head>` content, add it to the shared include behind a condition instead.
- Don't add content under a `web_scripts/`-style directory or point at `tbp.scripts.mit.edu`.  Stale content served that way is what got the locker flagged by IS&T.

Feel free to email [tbp-officers@mit.edu](mailto:tbp-officers@mit.edu) with any questions about this workflow or the website.
