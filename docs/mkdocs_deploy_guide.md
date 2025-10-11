# Getting Started with MkDocs for a Repo

This guide shows how to set up, preview, and deploy the documentation site for a repository using **MkDocs**, **Material for MkDocs**, and **GitHub Pages** — with support for **math equations**, **feedback widgets**, **copyable code**, **task lists**, and more.

> ✅ Good for documenting your RL learning journey with rich, interactive content.

---

## 📁 Repository Structure

Your mkdocs related docs live in the `docs/` folder:

```
docs/
├── index.md
├── contents.md
├── m00.md
├── m01.md
├── javascripts/
│   ├── feedback.js
│   └── mathjax.js
└── stylesheets/
    └── extra.css  # (optional)
```

MkDocs uses this folder by default.

---

## 🛠 Local Setup

### 1. Install Dependencies via `uv`

We use `uv` for fast, reproducible environments:

```bash
uv add mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin
```

This updates your `pyproject.toml` with all required plugins.

> 💡 Your `pyproject.toml` should now include:
> ```toml
> dependencies = [
>   "mkdocs-material>=9.6.21",
>   "mkdocs-git-revision-date-localized-plugin>=1.4.7",
>   "mkdocs-git-authors-plugin>=0.10.0",
>   # ... other deps
> ]
> ```

### 2. Preview the Site Locally

```bash
uv run mkdocs serve
```

Visit [`http://127.0.0.1:8000`](http://127.0.0.1:8000).

---

## 🎨 Customizations (Add One at a Time)

You can enable any of these features independently.

---

### ✅ 1. Copyable Code Blocks

**In `mkdocs.yml`:**
```yaml
theme:
  name: material
  features:
    - content.code.copy
```

✅ Every code block gets a **copy button**.

---

### ✅ 2. Task Lists (Checkboxes)

**In `mkdocs.yml`:**
```yaml
markdown_extensions:
  - pymdownx.tasklist:
      custom_checkbox: true
```

**In Markdown:**
```md
- [x] Installed libraries
- [ ] Ran agent
```

Renders as interactive checkboxes.

---

### ✅ 3. Math Equations (LaTeX)

#### Step 1: Enable in `mkdocs.yml`
```yaml
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
```

#### Step 2: Create `docs/javascripts/mathjax.js`
```js
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  if (typeof MathJax !== "undefined") {
    MathJax.typesetPromise();
  }
});
```

#### Step 3: Write Math in Markdown
```latex
$$
\mathcal{M} = \langle S, A, P, R, \gamma \rangle
$$
```

✅ Renders beautifully with MathJax.

---

### ✅ 4. Page Metadata (Last Updated + Contributors)

**In `mkdocs.yml`:**
```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
  - git-authors
```

> 🔌 Requires the plugins installed via `uv add` (see above).

✅ Shows **"Last updated: 2 months ago"** and **"Contributors: @you"** at page bottom.

---

### ✅ 5. Feedback Widget (😊 / 😞)

#### Step 1: Add to `mkdocs.yml`
```yaml
extra:
  analytics:
    feedback:
      title: Was this page helpful?
      ratings:
        - icon: material/emoticon-happy-outline
          name: This page was helpful
           1
          note: >-
            Thanks for your feedback!
        - icon: material/emoticon-sad-outline
          name: This page could be improved
           0
          note: >-
            Thanks for your feedback! Help us improve this page by
            using our <a href="https://github.com/deepsaia/rll/issues/new?title=[Feedback]+{title}+–+{url}&body=Page:+{url}%0A%0AWhat+was+missing+or+confusing?" target="_blank" rel="noopener">feedback form</a>.
```

#### Step 2: Create `docs/javascripts/feedback.js`
```js
document$.subscribe(function () {
  const form = document.forms.feedback;
  if (!form) return;

  form.hidden = false;

  // Prevent form submission scroll/jump
  const buttons = form.querySelectorAll(".md-feedback__icon");
  buttons.forEach(btn => btn.setAttribute("type", "button"));

  form.addEventListener("click", function (ev) {
    if (ev.target.matches(".md-feedback__icon")) {
      ev.preventDefault();
      const data = ev.target.getAttribute("data-md-value");
      const note = form.querySelector(`.md-feedback__note[data-md-value="${data}"]`);
      if (note) note.hidden = false;
      console.log("Feedback:", { page: location.pathname, rating: data });
    }
  });
});
```

#### Step 3: Load JS in `mkdocs.yml`
```yaml
extra_javascript:
  - javascripts/feedback.js
  # ... (keep mathjax.js too if used)
```

✅ Shows feedback buttons at **bottom of page** with GitHub issue link.

---

### ✅ 6. Theme Toggle (Light/Dark/Auto)

**In `mkdocs.yml`:**
```yaml
theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to system preference
    - media: "(prefers-color-scheme)"
      scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-auto
        name: Switch to light mode
```

✅ Adds a **theme toggle button** in the top-right header.

---

## 🚀 Deployment to GitHub Pages

### `.github/workflows/deploy.yml`
```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Install project dependencies
        run: uv sync --frozen

      - name: Build MkDocs site
        run: uv run mkdocs build --strict

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

> ✅ This installs **all dependencies from `pyproject.toml`**, including plugins.

---

[Optional] If you're using pyenv
```yml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'  # Optional: enables pip dependency caching

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Build MkDocs site
        run: mkdocs build --strict

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 📝 Adding New Content

1. Add `m02.md` to `docs/`
2. Update `mkdocs.yml` nav:
   ```yaml
   nav:
     - Home: index.md
     - Contents: contents.md
     - "Module 00": m00.md
     - "Module 01": m01.md
     - "Module 02": m02.md
   ```
3. Push → auto-deployed!

---

## 🔧 Troubleshooting

### ❌ "Plugin not installed" error
→ Ensure **all plugins are in `pyproject.toml`** and the workflow uses `uv sync`.

### ❌ Math not rendering
→ Verify `arithmatex` + `generic: true` and `mathjax.js` are present.

### ❌ Feedback causes page jump
→ Ensure `feedback.js` sets `type="button"` on icons.

### ❌ Duplicate GitHub Pages artifacts
→ Delete old workflow runs before re-running.

---

## 🌐 Live Site

Your docs will be live at:

```
https://<your-username>.github.io/<repo-name>/
```

Example: `https://deepsaia.github.io/rll/`

---
