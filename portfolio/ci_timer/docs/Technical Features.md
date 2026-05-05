# ci_timer — Technical Features

**Version:** 0.1.0
**Author:** Brittney Estes
**Language:** Python 3.11+

---

## Overview

`ci_timer` is a command-line tool that measures and visualizes execution times of jobs in a GitHub Actions CI/CD pipeline. Given a repository and an optional run ID, the tool fetches workflow data from the GitHub REST API, computes timing metrics, identifies bottlenecks, and presents the results in multiple output formats.

The primary use case is helping engineers quickly identify which jobs in a long-running workflow are slowing down their pipeline.

---

## Architecture

The tool is organized into four distinct layers, each with a single responsibility:

```
┌─────────────────────────────────────┐
│            CLI Layer                │  Parses arguments, orchestrates flow
├─────────────────────────────────────┤
│          API Client Layer           │  Communicates with GitHub REST API
├─────────────────────────────────────┤
│       Data & Analysis Layer         │  Models, duration math, bottleneck detection
├─────────────────────────────────────┤
│         Output Layer                │  Table, chart, JSON, CSV rendering
└─────────────────────────────────────┘
```

### Project Structure

```
ci_timer/
├── __main__.py                 # Entry point: python -m ci_timer
├── cli.py                      # Typer command definitions
├── config.py                   # Token resolution and default configuration
├── analysis.py                 # Duration computation and bottleneck detection
├── utils.py                    # Shared utility functions
├── enums.py                    # OutputType enum
├── api/
│   ├── client.py               # GitHub REST API client
│   └── models.py               # Dataclasses: WorkflowRun, Job, Step, WorkflowMetrics
└── docs/
│   ├── Technical Features.md   # Documentation about current and planned tool features
└── output/
    ├── table.py                # Rich terminal table renderer
    ├── chart.py                # Terminal horizontal bar chart renderer
    └── export.py               # Output router + JSON/CSV file exporters
```

---

## Current Features (v0.1.0)

### 1. GitHub Actions API Integration

The tool communicates with the GitHub REST API to fetch workflow run and job data in real time. Authentication is handled via a GitHub personal access token.

**Endpoints used:**
- `GET /repos/{owner}/{repo}/actions/runs` — fetch recent workflow runs
- `GET /repos/{owner}/{repo}/actions/runs/{run_id}` — fetch a specific run by ID
- `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs` — fetch all jobs for a run

**Key behaviors:**
- Automatic pagination — handles workflows with more than 30 jobs transparently
- Robust error handling — distinguishes between HTTP status errors (4xx/5xx) and network-level errors (timeouts, connection failures)
- Context manager pattern — HTTP connections are always properly closed after use

---

### 2. Data Modeling

All API responses are parsed into typed Python dataclasses for safe, structured access throughout the application.

**Models:**

| Model | Key Fields |
|-------|-----------|
| `WorkflowRun` | `id`, `name`, `run_number`, `status`, `conclusion`, `created_at`, `updated_at`, `jobs` |
| `Job` | `id`, `name`, `status`, `conclusion`, `started_at`, `completed_at`, `duration`, `steps` |
| `Step` | `name`, `status`, `conclusion`, `started_at`, `completed_at`, `duration` |
| `WorkflowMetrics` | `bottlenecks`, `stats` |

**Timezone handling:** All datetime values are parsed as timezone-aware objects (UTC) to prevent arithmetic errors when computing durations.

**Partial run handling:** Jobs and steps with `None` timestamps (cancelled or in-progress runs) are gracefully handled. Durations are set to `None` and excluded from metric calculations.

---

### 3. Bottleneck Detection

The tool automatically identifies the slowest jobs in a workflow run.

- Jobs are sorted by duration in descending order
- The top N slowest jobs are flagged as bottlenecks (default: top 3)
- Jobs with `None` durations are excluded from bottleneck analysis
- The `--top` flag allows the user to control how many bottlenecks are highlighted

---

### 4. Summary Statistics

For each workflow run the tool computes:

| Stat | Description |
|------|-------------|
| `total_job_duration` | Sum of all valid job durations |
| `average_job_duration` | Mean duration across all valid jobs |
| `longest_job` | The `Job` object with the highest duration |
| `shortest_job` | The `Job` object with the lowest duration |

---

### 5. Output Formats

The tool supports four output formats, selectable via the `--output` flag.

#### Table (default)
A Rich terminal table with the following columns:

| Column | Description |
|--------|-------------|
| Job Name | Name of the CI job |
| Conclusion | Color-coded result (green=success, red=failure, yellow=skipped, dim=cancelled) |
| Duration | Formatted as `mm:ss` |
| % of Total Duration | Each job's share of the total pipeline time |
| Flag | ⚠ warning icon for bottleneck jobs (highlighted in red) |

A summary panel below the table displays total duration, average duration, longest job, and shortest job.

#### Chart
A horizontal bar chart rendered in the terminal. Each job is represented as a bar scaled proportionally to the longest job's duration. Bottleneck jobs are highlighted in red. Jobs with no duration display an empty bar with `--` as the label.

#### JSON
Exports the full `WorkflowRun` and `WorkflowMetrics` data to a JSON file in the current working directory. Filename format: `workflow_{run_id}.json`. All `datetime` values are serialized to ISO 8601 strings. All `timedelta` values are serialized to total seconds as integers.

#### CSV
Exports a flat CSV file with one row per job to the current working directory. Filename format: `workflow_{run_id}.csv`.

Columns: `run_id`, `job_name`, `status`, `conclusion`, `started_at`, `completed_at`, `duration_seconds`

---

### 6. Token Resolution

The tool resolves the GitHub API token using the following priority order (most specific wins):

```
--token CLI flag  →  GITHUB_TOKEN env variable  →  .env file
```

If no token is found, the tool raises a clear error message directing the user to set the environment variable or pass the flag.

---

### 7. Configuration Defaults

All default values are centralized in `config.py` for easy modification:

| Setting | Default | Description |
|---------|---------|-------------|
| `DEFAULT_LIMIT` | 10 | Number of recent runs to fetch when no `--run-id` is provided |
| `DEFAULT_TOP_N` | 3 | Number of bottleneck jobs to highlight |
| `DEFAULT_OUTPUT` | `table` | Default output format |

---

## Planned Features (v0.2.0+)

### Retries and Timeouts
All API calls will include configurable timeouts and automatic retry logic with exponential backoff for transient failures (5xx responses, connection resets). Rate limit awareness via GitHub's `X-RateLimit-*` headers will be added to prevent unexpected failures on busy repositories.

### Step-Level Drill Down
A `--steps` flag will allow users to inspect the individual steps within a specific job, enabling pinpoint identification of slow steps within an already-identified bottleneck job.

### Multiple Run Comparison
A `--compare` flag combined with `--limit N` will display duration trends across multiple recent runs side by side, making it easy to spot regressions introduced by recent commits.

### HTML Export
A self-contained HTML report with interactive charts will be added as a fifth output type, making results easier to share with teammates who don't have terminal access.

### `--output-path` Flag
Users will be able to specify a custom destination directory for JSON and CSV exports rather than always writing to the current working directory.

### Sub-Second Duration Formatting
Jobs that complete in under one second currently display as `00:00`. This will be improved to display `<1s` for clarity.

### Multi-Platform Support
The layered architecture is designed for extension. A `BaseClient` abstract class will be introduced to formalize the client interface, enabling `GitLabClient` and `CircleCIClient` implementations to be added without changes to the analysis or output layers.

### Type Checking and Linting
`mypy` and `ruff` will be integrated into the development workflow to enforce type safety and consistent code style across the entire codebase.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `typer` | CLI argument parsing and command definition |
| `httpx` | HTTP client for GitHub API calls |
| `rich` | Terminal table, chart, and panel rendering |
| `python-dotenv` | `.env` file loading for local development |

---

## Limitations (v0.1.0)

- **GitHub Actions only** — other CI/CD platforms are not yet supported
- **No retries** — transient network failures will not be automatically retried
- **No rate limit handling** — heavy usage may exhaust the GitHub API rate limit without warning
- **Steps excluded from CSV** — step-level data is available in JSON export only
- **Current working directory only** — exported files are always written to the directory where the tool is invoked