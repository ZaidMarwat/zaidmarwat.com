# zaidmarwat.com

Personal site. One source file, two outputs.

    src/page.html      the source. edit this.
    build.py           wraps it in a real <head> + theme toggle
    public/            what gets deployed. generated; do not edit by hand.

## Change something

    python3 build.py
    git add -A
    git commit -m "Describe the change"
    git push

Pushing to `main` deploys automatically. Cloudflare Pages (project
`zaidmarwat-com`) is connected to this GitHub repo and runs `python3 build.py`
on every push, then serves `public/`. Build logs are in the Cloudflare
dashboard: Workers & Pages, zaidmarwat-com, Deployments.

Running `build.py` locally before committing keeps `public/` in the repo in
sync with the source, and lets you preview `public/index.html` in a browser.

Pushing to any other branch makes a preview deployment at
`<branch>.zaidmarwat-com.pages.dev` without touching the live site.

`src/page.html` is also the Claude Artifact source, which is why it has no
doctype or `<head>` of its own. The artifact host supplies those; `build.py`
supplies them for the real site.

## Hosting

- Repo: github.com/ZaidMarwat/zaidmarwat.com
- Cloudflare Pages project: `zaidmarwat-com` (zaidmarwat-com.pages.dev)
- Custom domain: zaidmarwat.com, a proxied CNAME to zaidmarwat-com.pages.dev
  in the zaidmarwat.com zone on the same Cloudflare account.

## Changing the domain

1. Cloudflare dashboard, Workers & Pages, zaidmarwat-com, Custom domains, Set up.
2. Update `SITE` in build.py, plus public/robots.txt and public/sitemap.xml,
   then rebuild and push so the canonical and social tags match.
