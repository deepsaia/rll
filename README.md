# RL Learning

A hands-on Reinforcement Learning course - from zero to expertise, with code at every step.

Live site: https://deepsaia.github.io/rll/

## Local Development

### Prerequisites

- [Node.js](https://nodejs.org/) 20+
- [Yarn](https://yarnpkg.com/) 1.x

### Setup

```bash
cd website
yarn install
```

### Run locally

```bash
cd website
yarn start
```

This starts a local dev server at `http://localhost:3000/rll/` with hot reloading - edits to docs and components are reflected instantly in the browser.

### Edit content

Course content lives in `website/docs/`:

- `docs/index.md` - Landing page
- `docs/contents.md` - Course roadmap
- `docs/modules/m00.md` through `m15.md` - Module pages

Pages are Markdown with optional MDX (React components) and KaTeX math (`$...$` for inline, `$$...$$` for display).

### Build

```bash
cd website
yarn build
```

This generates a static site in `website/build/`. To preview the production build locally:

```bash
cd website
yarn serve
```

## Publishing Changes

Push to `main` - that's it. A GitHub Actions workflow automatically builds the Docusaurus site and deploys it to GitHub Pages. No manual steps needed.

To check deployment status, see the **Actions** tab in the GitHub repo.
