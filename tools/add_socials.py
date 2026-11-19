"""Add Faunora's social accounts (icons in the site's line style + @fau.nora) to a site's index.html and style.css.
Usage: python add_socials.py <site_dir> [--v2]. Safe to run once per site; it refuses to run twice."""
import sys
from pathlib import Path

ACCOUNTS = [
    ("instagram", "Instagram", "https://www.instagram.com/fau.nora/"),
    ("threads", "Threads", "https://www.threads.com/@fau.nora"),
    ("tiktok", "TikTok", "https://www.tiktok.com/@fau.nora"),
]
HANDLE = "@fau.nora"

# 24x24 line icons, drawn to sit with the site's other stroke icons (stroke comes from CSS).
SYMBOLS = """
  <!-- Social icons (line style, stroke from CSS) -->
  <symbol id="s-instagram" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.7"/><circle cx="16.9" cy="7.1" r=".6" fill="currentColor"/></symbol>
  <symbol id="s-threads" viewBox="0 0 24 24"><path d="M16.9 8.4C15.9 6.3 14.1 5.2 11.9 5.2 8.1 5.2 5.6 8 5.6 12s2.5 6.8 6.4 6.8c3 0 5.2-1.7 5.4-4.2.2-2.5-1.8-3.9-4.4-3.9-2.1 0-3.6 1-3.6 2.4 0 1.3 1.1 2.1 2.5 2.1 2.4 0 3.5-1.9 3.5-4.6"/></symbol>
  <symbol id="s-tiktok" viewBox="0 0 24 24"><path d="M13.4 4.5v10.3a3.3 3.3 0 1 1-3.3-3.3"/><path d="M13.4 4.5c.5 2.4 2.1 3.9 4.6 4.2"/></symbol>
"""

CSS = """
/* ---------- Social accounts ---------- */
.socials { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; justify-content: center; gap: .55rem; }
.socials a {
  display: inline-flex; align-items: center; gap: .55rem; padding: .38rem 1rem .38rem .4rem; border-radius: 99px;
  border: 1px solid var(--line); background: rgba(250, 248, 240, .65); color: var(--ink); text-decoration: none;
  font-size: .88rem; line-height: 1.15; transition: border-color .3s var(--ease), background .3s var(--ease), transform .3s var(--ease);
}
.socials a:hover { border-color: var(--sage-deep); background: #fff; transform: translateY(-2px); }
.socials svg {
  flex: none; width: 32px; height: 32px; padding: 6px; border-radius: 50%; background: rgba(169, 183, 154, .32); color: var(--sage-deep);
  fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round;
}
.socials span { display: grid; text-align: left; }
.socials small { font-size: .66rem; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-soft); }
.socials.icons a { padding: 0; border-color: transparent; background: none; }
.socials.icons span { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.socials.icons svg { width: 40px; height: 40px; padding: 9px; background: rgba(250, 248, 240, .8); box-shadow: 0 0 0 1px rgba(79, 75, 67, .15); }
.socials.icons a:hover svg { background: #fff; color: var(--ink); }
.follow { margin: 1.6rem 0 .7rem; font-size: .72rem; letter-spacing: .22em; text-transform: uppercase; color: var(--ink-soft); }
.follow b { font-weight: 500; letter-spacing: .06em; text-transform: none; font-size: .9rem; color: var(--sage-deep); }
"""


def links(icons_only=False):
    items = "".join(
        f'<li><a href="{url}" target="_blank" rel="noopener" aria-label="Faunora on {name}, {HANDLE}">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#s-{key}"/></svg>'
        f'<span><small>{name}</small>{HANDLE}</span></a></li>' for key, name, url in ACCOUNTS)
    return f'<ul class="socials{" icons" if icons_only else ""}">{items}</ul>'


def sub(text, old, new):
    assert text.count(old) == 1, f"expected one match for: {old[:70]!r} (found {text.count(old)})"
    return text.replace(old, new)


def main(site, v2):
    index, css = site / "index.html", site / "style.css"
    html = index.read_text(encoding="utf-8")
    if 's-instagram' in html:
        sys.exit("socials already added")
    html = sub(html, "  </defs>\n", "  </defs>\n" + SYMBOLS)
    footer_block = f'<p class="follow">Follow us <b>{HANDLE}</b></p>\n  {links()}\n  '
    html = sub(html, '<p class="credit">', footer_block + '<p class="credit">')
    if v2:
        step = '      <span class="bracket"><button class="btn" type="button" data-go="consult">Step inside</button></span>\n    </div>\n'
        html = sub(html, step, step + f'    <div class="hero-social">{links(icons_only=True)}<span>{HANDLE}</span></div>\n')
        html = sub(html, '    <button class="nav-cta" type="button" data-open="consult">Book a session</button>\n',
                   '    <button class="nav-cta" type="button" data-open="consult">Book a session</button>\n'
                   f'    <div class="nav-social">{links(icons_only=True)}</div>\n')
    else:
        html = sub(html, '        <a class="btn ghost" href="#shop">Visit the shop</a>\n      </div>',
                   '        <a class="btn ghost" href="#shop">Visit the shop</a>\n      </div>\n'
                   f'      <div class="hero-social"><span>Follow {HANDLE}</span>{links(icons_only=True)}</div>')
    index.write_text(html, encoding="utf-8")
    css.write_text(css.read_text(encoding="utf-8").rstrip() + "\n" + CSS, encoding="utf-8")
    print("socials added to", site)


if __name__ == "__main__":
    main(Path(sys.argv[1]), "--v2" in sys.argv)
