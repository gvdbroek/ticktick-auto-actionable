# CLAUDE.md

## Project overview

TickTick Auto-Actionable is a tool that enforces actionability across all TickTick task lists. It checks every project for a `#next`-tagged task and creates a reminder task if none exists.

## Active implementation

**Rust** is the sole active implementation. The Python versions are archived under `archive/`.

## Architecture

- Entry point: `src/main.rs`
- Uses the `ticks` crate for TickTick API interaction
- Single-threaded Tokio runtime (intentional — avoids resource issues in containers)
- Concurrent project checking and task creation via `futures::join_all`
- Config via environment variables (loaded from `.env` in development via `dotenv`)

## Environment variables

- `API_KEY` — TickTick OAuth bearer token (required)

## Build & run

```sh
cargo run --release
```

Or via Docker:
```sh
docker run --env API_KEY=your_token mcbuffington/ticktick-actionable
```

## Deployment

Self-hosted. Docker image is built via GitHub Actions on push to `main` (when `src/`, `Cargo.*`, or `Dockerfile` change) and published to Docker Hub as `mcbuffington/ticktick-actionable`.

## Coding conventions

- Idiomatic Rust: proper error handling with `Result`, clippy clean, well-typed
- Keep it simple: no unnecessary abstractions or over-engineering
- Prefer straightforward, readable code over clever solutions

## Planned features

- **Expand actionability**: Support `#waiting` and `#choose` tags beyond just `#next`
- **Auto token refresh**: Automate OAuth token renewal (currently a manual Postman flow, token valid ~1 year)
- **Project blacklist**: Allow skipping specific projects by name or ID
