# Getting Started with MkDocs for This Repo

This guide shows how to set up, preview, and deploy the documentation site for this repository using **MkDocs** and **GitHub Pages**.

> ✅ Perfect for documenting your RL learning journey with Markdown files and code examples.

---

## 📁 Repository Structure

Your docs live in the `docs/` folder:

```
docs/
├── index.md        # Home page
├── contents.md     # Course outline
├── m00.md          # Module 00 notes
└── m01.md          # Module 01 notes
```

MkDocs automatically uses this folder as the source.

---

## 🛠 Local Setup

### 1. Install MkDocs + Material Theme

```bash
pip install mkdocs mkdocs-material
```

> 💡 You can also use `uv` if you prefer:  
> `uv pip install mkdocs mkdocs-material`

### 2. Preview the Site Locally

```bash
mkdocs serve
```

Visit [`http://127.0.0.1:8000`](http://127.0.0.1:8000) to see your live docs with hot-reload.

---

## 🚀 Deployment to GitHub Pages

The site is automatically deployed via **GitHub Actions** on every push to the `main` branch.

### How It Works

- The workflow builds your site using MkDocs.
- It uploads the static files to GitHub Pages.
- Your site goes live at:  
  `https://<your-username>.github.io/<repo-name>/`

> 🔒 This does **not** affect your personal `username.github.io` site.

### Configuration

The deployment is controlled by:

- **`.github/workflows/deploy.yml`** – GitHub Actions workflow
- **`mkdocs.yml`** – Site configuration (title, nav, theme, etc.)

No manual steps needed after setup!

---

## 📝 Adding New Content

1. Create a new Markdown file in `docs/` (e.g., `m02.md`)
2. Update the navigation in `mkdocs.yml`:

   ```yaml
   nav:
     - Home: index.md
     - Contents: contents.md
     - "Module 00": m00.md
     - "Module 01": m01.md
     - "Module 02": m02.md  # ← add this line
   ```

3. Commit and push — the site updates automatically!

---

## 🔧 Troubleshooting

### "Multiple artifacts named 'github-pages'" error

This happens if you re-run a failed workflow. To fix:

1. Go to **Actions** tab on GitHub
2. **Delete** any failed or duplicate workflow runs
3. Push a new commit (or use **"Run workflow"** manually)

> The included workflow uses `concurrency` to prevent this in the future.

### Site not updating?

- Wait 1–2 minutes after push — GitHub Pages can be slow.
- Check the **Actions** tab for deployment status.
- Ensure your branch is `main` (or update `deploy.yml` if using `master`).

---

## 🌐 Live Site

Once deployed, your documentation is available at:

```
https://<your-github-username>.github.io/<this-repo-name>/
```

Example: `https://alice.github.io/rl-learning/`

---

> 🎉 Happy documenting! Use this space to explain concepts, link to code, and track your RL progress.