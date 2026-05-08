# The Things You Can See Only When You Slow Down

A meditation on life in ten movements, by Dr. Non Arkaraprasertkul.
Static HTML. No build step. No framework.

## Files

```
slowdown/
├── index.html        ← the book
├── styles.css        ← typography + layout
├── download.py       ← one-time script to fetch art plates locally
├── img/              ← created by download.py (27 public-domain plates)
└── README.md         ← this file
```

## Local preview

Open `index.html` in any browser. No server required. The first time you
view it, images stream from the Wikimedia CDN; if you've run
`python3 download.py`, they load from `./img/` instantly.

```sh
# optional: serve over a local HTTP origin
python3 -m http.server 8000
# then visit http://localhost:8000/slowdown/
```

## Before deploying — fetch the art plates

For maximum reliability, run the download script once. It pulls 27
public-domain plates (~30–60 MB total) from Wikimedia Commons into
`./img/`:

```sh
python3 download.py
```

Safe to re-run; existing files are skipped. Python 3.6+, standard
library only — no `pip install` needed.

If you skip this step, the site still works: the page tries
`./img/<file>` first, falls back to `upload.wikimedia.org` direct CDN
URLs, then to the legacy Wikimedia redirect. Local files just guarantee
fast, predictable loads from your own host.

## Deploy to GitHub Pages + Cloudflare

The whole `slowdown/` folder is the deployable site.

1. Run `python3 download.py` to populate `img/`.
2. Create a new GitHub repo (e.g. `slow-down-book`).
3. Copy the contents of `slowdown/` to the repo root, OR keep it nested
   and set Pages to serve from `/slowdown`.
4. Commit `img/` along with the HTML — it's only ~50 MB and avoids any
   cold-start CDN dependency on Wikimedia.
5. In **Settings → Pages**, set source to `main` branch.
6. In Cloudflare, add the custom domain and enable proxied DNS.

### Hand-off prompt for Claude Code

Open Claude Code with this folder as the working directory and paste:

> Please deploy the static site in this directory to GitHub Pages with
> Cloudflare in front.
>
> Steps:
> 1. Run `python3 download.py` to fetch all art plates into `./img/`.
>    Verify the directory contains 27 image files when done.
> 2. Initialize a git repo, add a `.gitignore` excluding nothing (we
>    want img/ committed), commit everything, and push to a new public
>    GitHub repo. Ask me for the repo name.
> 3. Enable GitHub Pages on the `main` branch, root directory.
> 4. Ask me for the custom domain, then set up Cloudflare DNS records
>    (CNAME from the apex/subdomain to `<user>.github.io`, proxied).
> 5. Add a `CNAME` file at the root containing the custom domain so
>    GitHub Pages serves it correctly.
> 6. Print the final live URL.
>
> The site is plain HTML/CSS — no build step, no Node, no
> dependencies. The single entry point is `index.html`.

That's all Claude Code needs.

## Image hosting fallback chain

Each `<img>` in the page tries up to four sources before giving up:

1. `./img/<filename>` — your local copy (after `download.py`)
2. `upload.wikimedia.org/wikipedia/commons/thumb/...` — direct CDN
3. `commons.wikimedia.org/wiki/Special:FilePath/...` — legacy redirect
4. CDN retry once more

This means the page degrades gracefully under flaky networks, sandboxed
previews, or Wikimedia rate limits.

## Credits

All artwork is in the public domain. Sources are listed in the
"Sources & Plates" index at the back of the book. If you fork or adapt,
preserve the credit list.
