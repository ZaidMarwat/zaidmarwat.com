# zaidmarwat.com

Personal site. One source file, two outputs.

    src/page.html      the source. edit this.
    build.py           wraps it in a real <head> + theme toggle
    public/            what gets deployed. generated; do not edit by hand.

## Change something

    python3 build.py
    npx wrangler pages deploy public --project-name=zaidmarwat

`src/page.html` is also the Claude Artifact source, which is why it has no
doctype or `<head>` of its own. The artifact host supplies those; `build.py`
supplies them for the real site.

## First-time setup

    npx wrangler login          # opens a browser, one time only

## Attaching a custom domain later

1. Buy the domain (Cloudflare Registrar sells at cost).
2. Cloudflare dashboard, Workers & Pages, zaidmarwat, Custom domains, Set up.
3. Update `SITE` in build.py, plus public/robots.txt and public/sitemap.xml,
   then rebuild and redeploy so the canonical and social tags match.
