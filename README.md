
# Smart Task Management Engine

A high-performance, object-oriented Command Line Interface (CLI) task management system built with Python. This application features dynamic priority scheduling, automated deadline tracking using the native `datetime` module, persistent state serialization via JSON data storage, and live productivity performance analytics.

## Core Features

- **Object-Oriented Architecture:** Clean separation of concerns using `Task` and `TaskManager` paradigms.
- **Dynamic Priority Allocation:** Automated logic that computes and assigns urgency metrics (High, Medium, Low) based on real-time deadline parameters.
- **Data Persistence & Hydration:** Production-grade JSON serialization and deserialization routines to maintain runtime state across application restarts without data loss.
- **Productivity Analytics:** On-demand performance report compilation that parses data matrix arrays to compute precision completion scores.
- **Robust Exception Handling:** Built-in validation blocks to handle faulty data type parsing (e.g., non-integer casting for operational intervals) and missing storage records smoothly.

## Architectural Overview

The engine encapsulates state properties in dedicated runtime data arrays, utilizing automated I/O handlers to serialize execution structures into flat storage files (`tasks.json`).

```text
[ User Menu Interface ] <---> [ TaskManager Control Block ] <---> [ File Handling / JSON DB ]
                                          |
                                          v
                              [ Individual Task Instance ]
