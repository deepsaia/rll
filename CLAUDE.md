# CLAUDE.md - Project Guide for RL Learning (rll)

## Project Overview

This is a **hands-on Reinforcement Learning course** - a structured, module-by-module curriculum that takes learners from zero to expertise in RL. It includes a documentation website (deployed to GitHub Pages) and runnable Python code for every concept.

- **Repo**: `deepsaia/rll`
- **Live site**: https://deepsaia.github.io/rll/
- **Author**: Deepak
- **Python**: 3.12+ (managed with `uv`)
- **Docs framework**: Docusaurus (React-based, deployed to GitHub Pages)

---

## Module Structure (Revised Curriculum)

| Module | Topic |
|--------|-------|
| 00 | Introduction |
| 01 | Math Foundations for RL |
| 02 | Multi-Armed Bandits & Exploration |
| 03 | MDPs, Bellman Equations & Dynamic Programming |
| 04 | Monte Carlo & Temporal Difference Methods |
| 05 | Function Approximation & DQN |
| 06 | Policy Gradients & Actor-Critic |
| 07 | Modern Deep RL (PPO, SAC, TD3) |
| 08 | Reward Design, Debugging & Diagnostics |
| 09 | Partial Observability & Generalization |
| 10 | Model-Based RL & Planning |
| 11 | RLHF & LLM Alignment |
| 12 | Multi-Agent RL |
| 13 | Sim-to-Real & Production RL |
| 14 | Paper Reproduction Project |
| 15 | Capstone |

Code for each module lives in a directory named after the module (e.g., `m00/`, `m01/`). Each module's documentation lives in the Docusaurus `docs/` directory.

---

## Content & Writing Guidelines

### Tone
- **Fun to read, not boring.** This is not a dry textbook. Write with personality.
- Use humor where it lands naturally - not forced, not on every page, but enough that a reader smiles.
- Conversational but technically precise. Explain hard things simply without dumbing them down.
- Analogies are encouraged. A good analogy is worth a thousand equations.

### Examples & Industry Coverage
- Every concept must be illustrated with **ample code examples** that actually run.
- Some examples should be funny or memorable (a squirrel hoarding acorns as a bandit problem, etc.).
- Regularly draw examples from **real-world industries**: Automobile, Healthcare, Insurance, Finance, Robotics, Consumer Products, Travel, Hospitality, and others.
- Not every example needs to be from industry - mix in games, toy problems, and absurd scenarios to keep things varied.
- When using industry examples, be specific enough that a domain expert would nod, not so jargon-heavy that a newcomer drowns.

### Depth
- Cover **sufficient detail** for each topic. Do not skim or hand-wave.
- Every algorithm should include: intuition, math (where needed), pseudocode, runnable Python implementation, and discussion of when/why it fails.
- Include diagnostic advice: "If you see X, it probably means Y."
- Exercises should range from guided ("fill in this function") to open-ended ("design a reward function for...").

### Structure per Module
Each module page should follow this structure:
1. **Learning Objectives** - what the reader will be able to do after this module
2. **Concept Explanation** - theory with analogies and visuals
3. **Code Examples** - runnable, well-commented Python
4. **Real-World Connections** - industry examples showing where this applies
5. **Common Pitfalls** - what goes wrong and how to debug it
6. **Exercises** - with starter code and test cases where applicable
7. **Key Takeaways** - concise summary

---

## Tech Stack

- **Language**: Python 3.12+
- **Package manager**: `uv`
- **RL libraries**: Gymnasium, Stable-Baselines3, PyTorch
- **Experiment tracking**: MLflow, Weights & Biases
- **Docs**: Docusaurus (React/Node.js), deployed via GitHub Actions to GitHub Pages
- **Math rendering**: KaTeX (via remark-math + rehype-katex)
- **Logging**: loguru (not print statements)

---

## Coding Guidelines & Best Practices

---

### General Principles

* Write **clear, maintainable, and modular code**.
* Prefer **explicitness over cleverness**.
* Keep functions and modules **small and focused**.
* Do not ever write nested functions or classes.
* Avoid duplication; reuse existing utilities where possible.
* Prioritize **readability and maintainability** over premature optimization.

---

### Code Style

* Follow **PEP8** for formatting, naming conventions, and import conventions.
* Organize imports into standard library, third-party, and local modules.
* Use **explicit type hints** for all functions and methods.
* Avoid untyped interfaces unless absolutely necessary.

---

### Module Design

* Each module should have a **single clear responsibility**. And therefore have only a single class per module.
* Avoid excessively large modules or functions.
* Group related functionality logically within packages.
* Do **not place anything logic** inside `__init__.py`.
* Avoid global variables unless absolutely necessary.
* Favor simple, well-understood design patterns when appropriate.

---

### Error Handling & Logging

* Handle exceptions **explicitly and consistently**.
* Do not silently swallow exceptions.
* Provide meaningful error messages and logging.
* Use a structured logging approach instead of `print` statements.
* Ensure logs provide sufficient context for debugging and monitoring.

---

### Testing

* Write tests for new functionality whenever possible.
* Ensure tests cover normal behavior, edge cases, and failure scenarios.
* Tests should be deterministic and easy to run.

---

## Repository Layout

```
rll/
  CLAUDE.md              # This file
  pyproject.toml         # Python project config (uv)
  website/               # Docusaurus site
    docusaurus.config.ts # Site configuration
    sidebars.ts          # Sidebar navigation
    package.json         # Node.js dependencies (yarn)
    docs/                # Course documentation (Markdown/MDX)
      index.md           # Landing page
      contents.md        # Course roadmap
      modules/           # m00.md through m15.md
    src/
      components/        # Custom React components (FeedbackWidget)
      clientModules/     # Client-side scripts (progress tracking)
      css/               # Custom styles
      theme/             # Swizzled Docusaurus theme components
    static/              # Static assets (favicon, images)
  m00/ - m15/            # Module Python code directories
  gyms/                  # Custom Gymnasium environments
  tracing/               # Experiment tracking examples
  .github/workflows/     # CI/CD (GitHub Actions -> GitHub Pages)
```

---

## Deployment

The docs site is deployed to GitHub Pages via GitHub Actions on every push to `main`. The workflow installs Node.js dependencies with `yarn`, builds the Docusaurus site, and publishes `website/build/` to GitHub Pages.
