# RinseKit (vibe-sweeper)

**RinseKit** is a CLI tool that scans a repository for "vibe-coded" / AI-ish mess
and produces a simple report. It can optionally run formatters like `ruff` (Python)
and `biome` (JS/TS/etc) if they are installed on your PATH.

This is a **v1 MVP** – focused on:
- Scanning files
- Detecting AI-style phrases & long comment blocks
- Producing a Markdown report
- Optional formatting pass via external tools

## Installation

From the project root:

```bash
pip install .
```

Or, in editable mode:

```bash
pip install -e .
```

## Usage

Scan the current directory (no changes applied):

```bash
vibe-sweeper scan .
```

Generate a report and run safe formatters where possible:

```bash
vibe-sweeper run . --apply
```

Check mode for CI (exits with non-zero code if issues are found):

```bash
vibe-sweeper check .
```

## Configuration

You can create a `vibe.yaml` at the project root to override defaults.

See `src/vibe_sweeper/config/default_rules.yaml` for the base configuration.
