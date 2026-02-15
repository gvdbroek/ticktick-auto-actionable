# TickTick Auto-Actionable

Ensures every task list in your TickTick account stays actionable. If a project has no task tagged `#next`, a high-priority reminder task is automatically created.

## Why?

Projects without a clear next step become stale and forgotten. This tool enforces that every list always has a chosen next action, so nothing falls through the cracks.

## How it works

1. Fetches all projects from the TickTick API
2. Checks each project's tasks for a `#next` tag
3. If no task is tagged `#next`, creates a reminder task: `"Set #next action for: <project>"`

Empty projects are skipped.

## Actionability tags

- **`#next`** - The chosen next step to work on
- **`#waiting`** - Blocked or waiting on something external
- **`#choose`** - An important decision must be made before proceeding

These can be combined (e.g. `#next` + `#waiting` = literally blocked, no action possible until the wait lifts).

## Setup

### 1. Get a TickTick API key

Load `archive/gcp/TickTick.postman_collection.json` into Postman and set up three environment variables: `base_url`, `client_id`, `client_secret`. Request a new token through the OAuth flow - the access token is valid for ~1 year.

### 2. Configure

Create a `.env` file in the project root:

```
API_KEY=your_ticktick_access_token
```

### 3. Run

#### Docker (recommended)

```sh
docker run --env API_KEY=your_token mcbuffington/ticktick-actionable
```

#### From source

```sh
cargo run --release
```

Set up a cron job or scheduler to run it periodically.

## Project structure

```
src/         - Rust source code
archive/     - Deprecated Python implementations (gcp/, py/)
.github/     - CI/CD workflow
```

## CI/CD

Pushes to `main` that touch `src/`, `Cargo.*`, or `Dockerfile` trigger a GitHub Actions workflow that builds the Docker image and pushes it to Docker Hub as `mcbuffington/ticktick-actionable`.
