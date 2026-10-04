# Deep's Personal Wikipedia

A wiki built **only** from the books I've read completely ([books.md](books.md)). The goal is to get an instant "aha" when I'm curious about something random or stuck on a professional problem. I can pull a specific story or idea and use it right away.

## Core Design Idea: Search by Situation
Normal Wikipedia is organized by **topic**. Mine should also be organized by **the moment I'm in**:
> "My team won't push back on me" → Korean Air crashes (Outliers), Netflix candor (No Rules Rules), Toyota's andon cord

## Page Types
| Type | Folder | What it holds | Example |
|------|--------|---------------|---------|
| **Story** | `stories/` | One memorable anecdote with its lesson and when to use it | Korean Air & power distance |
| **Concept** | `concepts/` | One idea, linked to every book that touches it | Incentives, 10,000 hours, Theory of Constraints, Blue Ocean |
| **Book** | `books/` | Summary, big ideas, and a list of its stories and concepts | Outliers |
| **Situation** | `situations/` | A real-life prompt that points to the right stories | "Negotiating a raise", "Launching something new" |
| **Debate** | `debates/` | Places where my books disagree | Outliers (10,000 hours / specialize) vs Range (sample widely) |
| **Person / Company** | `entities/` | People and companies that show up across books | Amazon (Everything Store, The Four), Jeff Bezos |

## How It's Organized
- **Shelves:** similar books grouped together (the `##` headings in [books.md](books.md)). Stories sit under their book.
- **I'm dealing with:** situations from [taxonomy.md](taxonomy.md), grouped into 7 themes.
- **Concepts:** big ideas that cut across books, also listed in [taxonomy.md](taxonomy.md).
- Only use tags from `taxonomy.md`. `build.py` warns about anything else.

## Using the App
1. Add or edit Markdown pages in `stories/`.
2. Run `python build.py` in this folder. It regenerates `wiki-data.js` and checks the tags.
3. Open `index.html` in a browser, or refresh it.

## Story Template
Every story page has: **hook → story → lesson → when to use → try this → related → aha prompt**.
See [stories/korean-air-power-distance.md](stories/korean-air-power-distance.md).

## Accuracy Rule
Drafts written with AI can misremember details. Every page has `verified_by_deep: false` until I've checked it against my memory or highlights. Each page cites its book and chapter.

## Ideas & Roadmap
See [IDEAS.md](IDEAS.md).
