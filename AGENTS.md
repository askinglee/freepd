# FreePD - AI Agent Guide

## Project Overview

**FreePD** (https://freepd.cn) is a Chinese-language static website offering:
1. **Free Commercial Font Downloads** - Curated collection of free Chinese fonts with clear licensing info
2. **Online PDF Tools** - Client-side PDF processing tools (preview, merge, convert, compress)

The site is built with **Hugo** static site generator using the **PaperMod** theme, and deployed to **Cloudflare Pages**.

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Static Site Generator | Hugo | 0.149.2 (via hugo-bin) |
| Theme | PaperMod | MIT License |
| Build Tool | npm / Node.js | - |
| Deployment | Cloudflare Wrangler | ^3.114.0 |
| Search | Fuse.js | Client-side |
| PDF Processing | PDF.js | CDN (3.11.174) |
| Analytics | Google Analytics + Baidu Tongji | G-LWML4535XW |

---

## Project Structure

```
freepd/
├── hugo.toml                 # Main Hugo configuration (Chinese, SEO, menus)
├── package.json              # npm scripts and dependencies
├── wrangler.jsonc            # Cloudflare deployment config
├── content/                  # All website content (Markdown)
│   ├── _index.md            # Homepage with hero section
│   ├── fonts/               # Font detail pages (10+ fonts)
│   │   ├── alibaba-puhuiti.md
│   │   ├── harmonyos-sans.md
│   │   ├── lxgw-wenkai.md
│   │   └── ...
│   ├── tools/               # PDF tool pages (6 tools)
│   │   ├── pdf-preview.md   # PDF viewer with PDF.js
│   │   ├── merge-pdf.md
│   │   ├── pdf-to-word.md
│   │   └── ...
│   ├── about/               # About and legal pages
│   │   ├── _index.md        # About FreePD
│   │   └── license.md       # Copyright disclaimer
│   └── search.md            # Search page (uses Fuse.js)
├── layouts/                  # Custom Hugo templates
│   ├── index.html           # Homepage layout override
│   ├── fonts/
│   │   └── list.html        # Custom font listing with category filter
│   ├── shortcodes/          # Reusable components
│   │   ├── rawhtml.html     # Allow raw HTML in Markdown
│   │   ├── homepage_hero.html
│   │   └── ...
│   └── partials/
│       └── extend_head.html # Baidu verification + analytics
├── assets/
│   └── css/extended/
│       └── custom.css       # Custom styles for category navigation
├── static/                   # Static assets (copied as-is)
│   ├── images/fonts/        # Font preview images
│   ├── favicon.png
│   └── robots.txt
├── themes/PaperMod/         # Hugo theme (do not modify)
├── archetypes/              # Content templates
│   ├── default.md
│   ├── fonts.md            # Template for new font pages
│   └── tools.md            # Template for new tool pages
└── scripts/
    └── baidu_push.py       # SEO: Baidu URL submission script
```

---

## Build Commands

```bash
# Install dependencies
npm install

# Build the site (outputs to /public)
npm run build
# or: hugo

# Build and deploy to Cloudflare
npm run deploy
# or: hugo && wrangler deploy

# Development server
hugo server -D
```

---

## Content Management

### Creating a New Font Page

```bash
hugo new content fonts/new-font-name.md
```

The `archetypes/fonts.md` template provides the standard frontmatter:

```yaml
---
title: "Font Name"
date: 2026-01-28
description: "Font description for SEO"
slug: font-name
tags: ["可商用", "黑体"]
categories: ["中文字体", "免费字体"]
weight: 100                    # Lower = higher in list
font_license: "SIL Open Font License 1.1"
author_url: "https://..."
download_url: "https://..."
preview_image: "/images/fonts/font-name-preview.png"
showToc: true
tocOpen: true
---
```

**Required font page sections:**
1. 字体简介 (Font introduction)
2. 字体预览 (Preview image)
3. 应用场景 (Use cases)
4. 字体授权说明 (License details - critical!)
5. 下载地址 (Download links)

### Creating a New PDF Tool Page

```bash
hugo new content tools/new-tool.md
```

PDF tools embed HTML/JS directly in Markdown using the `rawhtml` shortcode:

```markdown
{{< rawhtml >}}
<div class="pdf-tool-container">
  <!-- Tool UI and logic here -->
</div>
<script>
  // Client-side processing only - no server upload
</script>
{{< /rawhtml >}}
```

**Important:** All PDF processing must be client-side using libraries like PDF.js. Files must NOT be uploaded to any server.

---

## Custom Shortcodes

| Shortcode | Purpose | Usage |
|-----------|---------|-------|
| `rawhtml` | Embed raw HTML/CSS/JS in Markdown | `{{< rawhtml >}}...{{< /rawhtml >}}` |
| `homepage_hero` | Homepage hero section | `{{< homepage_hero >}}` |

---

## Styling Guidelines

Custom styles go in `assets/css/extended/custom.css`:

- Uses CSS variables from PaperMod theme (`var(--theme)`, `var(--code-bg)`, etc.)
- Supports dark mode with `.dark` class
- Primary color: `#3b82f6` (blue)
- Category tags use pill-style buttons with rounded corners

---

## SEO & Analytics

### Configured Services
- **Google Analytics**: G-LWML4535XW
- **Baidu Tongji**: hm.js?960956ff1f7af03d8a2321f4cff42e51
- **Baidu Site Verification**: Two codes in `extend_head.html`

### Baidu URL Submission
Use `scripts/baidu_push.py` to submit new pages to Baidu:

```bash
python scripts/baidu_push.py
```

Edit the `urls_to_push` list in the script before running.

---

## Deployment

The site deploys to **Cloudflare Pages**:

1. Build output directory: `./public`
2. Deployment command: `wrangler deploy`
3. Config file: `wrangler.jsonc`

**CI/CD considerations:**
- `public/` is in `.gitignore` - only source files are version controlled
- The `.hugo_build.lock` file is committed

---

## Important Conventions

### Font Content
- Always verify and clearly state the license
- Include both official and mirror download links when possible
- Use preview images in `/static/images/fonts/`
- Tag commercial-friendly fonts with `"可商用"`

### PDF Tools
- **Privacy First**: All processing must be client-side
- Use PDF.js from CDN: `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/`
- Provide clear UI states: loading, success, error
- Include related tools navigation at bottom

### Images
- Font previews: PNG format, stored in `static/images/fonts/`
- Naming convention: `{font-slug}-preview.png`
- Favicon: `static/favicon.png` (used for all sizes)

---

## Security & Privacy

1. **No user data collection** - PDF tools process files locally
2. **No external fonts/tracking** except Google Analytics and Baidu
3. **CDN dependencies**: PDF.js loaded from cdnjs.cloudflare.com
4. Contact email for DMCA: legal@freepd.cn

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Hugo version compatibility (requires 0.146.0+) |
| Theme not found | Ensure `themes/PaperMod/` is present (git submodule or copied) |
| Search not working | Fuse.js requires `outputs.home = ["HTML", "RSS", "JSON"]` in hugo.toml |
| CSS not applied | Custom CSS must be in `assets/css/extended/` (not `static/`) |

---

## External Resources

- **Hugo Docs**: https://gohugo.io/documentation/
- **PaperMod Wiki**: https://github.com/adityatelange/hugo-PaperMod/wiki
- **PDF.js Docs**: https://mozilla.github.io/pdf.js/
- **Cloudflare Wrangler**: https://developers.cloudflare.com/workers/wrangler/
