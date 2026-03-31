# 10 DevOps Python Capstone Projects

> **Topics Covered:** Numbers & Floats, Strings & f-strings, Lists, Tuples, Sets, Dictionaries, Conditionals, Guard Clauses, For/While Loops, List/Set/Dict Comprehensions, Functions, Range/Enumerate/Zip, Classes & Inheritance, `*args`/`**kwargs`, Lambda, `sorted()`/`map()`/`filter()`
>
> **Difficulty:** Moderate to Hard | **Style:** Every project uses as many topics as possible in a way that makes real DevOps sense.

---

## Project 1: Infrastructure Inventory & Health Dashboard

**Real-World Context:** DevOps engineers maintain live inventories of servers and services. This project simulates building that inventory system from scratch with health checks and reporting.

**What You'll Build:**
A multi-class system that tracks servers, checks their health, and generates a formatted dashboard report.

**Requirements:**

**Data Setup**
- Create a list of at least 8 server dictionaries, each containing: `hostname` (str), `ip` (str), `role` (str — `"web"`, `"db"`, `"cache"`, `"worker"`), `cpu_percent` (float), `mem_percent` (float), `disk_percent` (float), `uptime_days` (int), `open_ports` (list of ints), `tags` (set of strings like `{"prod", "us-east-1"}`)

**Class Design**
- Build a `Server` class whose `__init__` accepts `hostname`, `ip`, `role`, and `**metrics` for the flexible numeric fields
- Add a `health_status(self)` method that returns `"CRITICAL"`, `"WARNING"`, or `"HEALTHY"` based on thresholds you define using conditionals and guard clauses — check for missing data first
- Add a `summary(self)` method that returns a formatted f-string one-liner about the server
- Build a `ServerInventory` class that holds a list of `Server` objects
  - Add `register(*servers)` to add servers in bulk
  - Add `get_by_role(role)` that returns a filtered list
  - Add `report(**filters)` that accepts optional keyword filters like `min_cpu=80`, `status="CRITICAL"`, `tag="prod"` and returns matching servers

**Processing & Output**
- Use `enumerate()` to print a numbered list of all servers in the inventory
- Use `zip()` to pair each server with a mock "last check timestamp" from a separate list you create
- Use `filter()` with a lambda to pull all CRITICAL servers
- Use `sorted()` with a lambda to rank servers by `cpu_percent` descending
- Use `map()` with a lambda to extract a list of all unique hostnames
- Use a set comprehension to collect all unique roles present in the inventory
- Use a dict comprehension to build a `{hostname: health_status}` lookup table
- Use `range()` to simulate running 3 health check cycles, printing a summary after each

**Concepts Practiced:** Classes, inheritance-ready design, `__init__`, `*args`, `**kwargs`, lists, dicts, sets, tuples, f-strings, conditionals, guard clauses, `enumerate`, `zip`, `range`, `filter`, `sorted`, `map`, list/set/dict comprehension

---

## Project 2: CI/CD Pipeline Execution Engine

**Real-World Context:** Every CI/CD system (Jenkins, GitHub Actions, GitLab CI) runs jobs as a series of stages. This project builds a pipeline engine that models that behavior.

**What You'll Build:**
A pipeline runner that defines stages, executes them in order, tracks results, and produces a final run report.

**Requirements:**

**Class Design**
- Build a `PipelineStage` class with `__init__(self, name, *commands, **config)` where:
  - `commands` are strings representing shell commands to simulate
  - `config` accepts options like `timeout=30`, `allow_failure=False`, `env="production"`, `retries=1`
- Add a `run(self)` method that iterates through commands using `enumerate()`, simulates success/failure using a condition on the command string (e.g., any command containing `"fail"` fails), and returns a result dict with `stage`, `passed`, `commands_run`, `duration_seconds` (use a float you compute from a formula, not `time`)
- Add a `__str__` method that returns a formatted f-string representation of the stage

- Build a `Pipeline` class with `__init__(self, name, environment, *stages, **metadata)`
  - `stages` are `PipelineStage` objects
  - `metadata` might include `triggered_by="push"`, `branch="main"`, `commit="abc123"`
- Add `add_stage(*new_stages)` to append more stages after construction
- Add `run_pipeline(self)` that runs each stage in order using a for loop, stops on failure unless `allow_failure=True`, and returns a full report dict
- Add `summary(self)` that prints a formatted pipeline run summary using f-strings

**Processing & Output**
- Use a list comprehension to extract only the names of passed stages from the report
- Use `filter()` with a lambda to identify stages where `allow_failure=True`
- Use `sorted()` with a lambda to rank stages by `duration_seconds`
- Use `map()` with a lambda to produce a status badge string per stage: `"✓ build"` or `"✗ test"`
- Use a dict comprehension to build a `{stage_name: passed}` result lookup
- Use `zip()` to pair stage names with their durations for a timing report
- Use a while loop to implement the retry logic inside `PipelineStage.run()` — retry up to `retries` times before marking as failed

**Concepts Practiced:** Classes, `*args`, `**kwargs`, `__str__`, for/while loops, conditionals, guard clauses, `enumerate`, `zip`, `map`, `filter`, `sorted`, list/dict comprehension, f-strings, floats

---

## Project 3: Cloud Cost Optimization Analyzer

**Real-World Context:** Cloud engineers review billing data to find waste, rightsizing opportunities, and budget overruns. This project builds that analysis tool.

**What You'll Build:**
A cost analysis system that ingests billing records, computes totals, flags waste, and produces recommendations.

**Requirements:**

**Data Setup**
- Create a list of at least 12 billing record tuples in the format: `(service, resource_id, region, resource_type, hours_used, cost_per_hour, max_capacity, actual_usage_percent)`
- Example: `("ec2", "i-0abc123", "us-east-1", "t3.large", 720, 0.0832, 100, 12.5)`
- Store all unique regions in a set
- Store all unique resource types in a set

**Functions**
- Write `compute_totals(*records)` that accepts any number of billing tuples and returns a dict with `total_cost`, `total_hours`, `avg_cost_per_hour` — compute `total_cost = hours * rate` for each using `map()` with a lambda first, then sum the result
- Write `flag_underutilized(records, **thresholds)` where thresholds like `max_usage=20.0`, `min_hours=100` flag records that are wasteful
- Write `cost_by_service(**service_filters)` that accepts keyword arguments where each key is a service name and value is a list of records for that service, then returns total cost per service
- Write `recommend_action(record)` that uses conditionals and guard clauses to return a string recommendation: `"TERMINATE"`, `"DOWNSIZE"`, `"RIGHTSIZED"`, or `"REVIEW"`

**Processing & Output**
- Use a dict comprehension to build `{resource_id: total_cost}` for all records
- Use `filter()` with a lambda to find records where `actual_usage_percent < 15`
- Use `sorted()` with a lambda to rank records by total cost descending
- Use `map()` with a lambda to apply `recommend_action` to every record
- Use `enumerate()` to print a ranked waste report with position numbers
- Use `zip()` to pair each resource ID with its recommendation
- Use a set comprehension to collect all resource types that have at least one `"TERMINATE"` recommendation
- Use `range()` to simulate 3 months of historical data by multiplying costs

**Concepts Practiced:** Tuples, lists, sets, dicts, comprehensions (all three types), `*args`, `**kwargs`, `map`, `filter`, `sorted`, `enumerate`, `zip`, `range`, guard clauses, f-strings, floats/integers

---

## Project 4: Kubernetes Cluster State Manager

**Real-World Context:** Kubernetes constantly reconciles desired state vs. actual state. This project simulates that reconciliation loop using Python data structures and OOP.

**What You'll Build:**
A cluster state simulator that tracks deployments, detects drift between desired and actual state, and generates remediation plans.

**Requirements:**

**Class Design**
- Build a `Deployment` class with `__init__(self, name, image, namespace, **spec)` where `spec` accepts fields like `replicas=3`, `cpu_limit="500m"`, `mem_limit="256Mi"`, `env_vars={}`, `labels={}`
- Add `scale(self, replicas)` method that validates the input (guard clause: replicas must be int > 0 and <= 50) and updates the replica count
- Add `diff(self, other_deployment)` that compares two `Deployment` objects and returns a dict of fields that differ
- Add `to_manifest(self)` that returns a dict representing the deployment as a K8s-style manifest

- Build a `Cluster` class that holds a dict of `{name: Deployment}` for both `desired_state` and `actual_state`
- Add `apply(*deployments)` to add to desired state
- Add `sync()` that compares desired vs actual, returns a list of actions needed: `{"action": "CREATE"/"UPDATE"/"DELETE", "deployment": name, "changes": {...}}`
- Add `status_report(self, **filters)` accepting filters like `namespace="production"`, `min_replicas=2`

**Processing & Output**
- Use a list comprehension to extract all deployment names in a namespace
- Use a dict comprehension to build a `{name: replica_count}` snapshot
- Use `filter()` with a lambda to find deployments with `replicas < 2` (potential single points of failure)
- Use `sorted()` with a lambda to order deployments by replica count descending
- Use `map()` with a lambda to produce a `"namespace/name:image"` string for each deployment
- Use `zip()` to pair desired state deployments with their actual state counterparts for comparison
- Use `enumerate()` to print a numbered reconciliation plan
- Use a set comprehension to collect all namespaces in use
- Use a while loop to simulate a reconciliation loop that runs until desired == actual state (max 5 iterations)

**Concepts Practiced:** Classes, `__init__`, `*args`, `**kwargs`, inheritance-ready, guard clauses, conditionals, while loop, for loop, `enumerate`, `zip`, `sorted`, `filter`, `map`, all comprehension types, dicts, sets, f-strings

---

## Project 5: Log Aggregation and Alerting System

**Real-World Context:** Log aggregation tools like ELK Stack and Splunk parse logs, extract patterns, and fire alerts. This project builds that pipeline in Python.

**What You'll Build:**
A log processor that parses raw log strings, classifies entries, aggregates statistics, and fires alerts based on configurable rules.

**Requirements:**

**Data Setup**
- Create a list of at least 15 raw log strings in a realistic format:
  `"2024-01-15 14:32:01 ERROR api-service Connection timeout after 30s"`
  `"2024-01-15 14:32:05 INFO web-server GET /health 200 12ms"`
- Each log entry should have: timestamp, level (`DEBUG`, `INFO`, `WARN`, `ERROR`, `CRITICAL`), service name, and message

**Class Design**
- Build a `LogEntry` class with `__init__(self, raw_line)` that parses the raw string in `__init__` using `.split()` and string methods, storing `timestamp`, `level`, `service`, `message` as instance attributes
- Add guard clauses to handle malformed lines (lines that don't have enough parts)
- Add a `is_error(self)` method returning a bool
- Add `__str__` returning a clean formatted f-string

- Build a `LogAggregator` class
  - Add `ingest(*log_lines)` to parse and store `LogEntry` objects
  - Add `get_by_level(level)` that returns filtered entries
  - Add `get_by_service(*service_names)` that returns entries matching any of the given services
  - Add `stats(self)` returning a dict with counts per level — use a dict comprehension
  - Add `alert_on(**rules)` where rules are like `ERROR_threshold=5`, `CRITICAL_threshold=1`, `service="api-service"` — fires if any rule is breached

**Processing & Output**
- Use `filter()` with a lambda to extract all ERROR and CRITICAL entries
- Use `sorted()` with a lambda to sort entries by timestamp string (lexicographic works here)
- Use `map()` with a lambda to extract just the service names from all entries
- Use a set comprehension on the mapped service names to get unique services
- Use a dict comprehension to build `{service: error_count}` for all services
- Use `enumerate()` and `zip()` together to produce a numbered report pairing each service with its error count
- Use a list comprehension with a conditional expression to label each entry as `"ACTION NEEDED"` or `"OK"`
- Use `range()` to simulate re-processing the log 3 times (batch processing simulation) and track totals across runs

**Concepts Practiced:** Classes, `__init__` parsing, `*args`, `**kwargs`, guard clauses, string methods (`.split()`, `.strip()`, `.startswith()`), f-strings, conditionals, for/while loops, `range`, `enumerate`, `zip`, `filter`, `sorted`, `map`, all comprehension types, sets, dicts

---

## Project 6: Multi-Environment Deployment Configuration Manager

**Real-World Context:** Teams maintain separate configs for dev, staging, and production. This project builds a system to manage, validate, merge, and diff those configs.

**What You'll Build:**
A configuration management library that handles environment-specific settings, validates them, and detects dangerous production changes.

**Requirements:**

**Data Setup**
- Define base config dictionaries for three environments: `dev`, `staging`, `prod`
- Each dict should have keys like: `db_host`, `db_port`, `replicas`, `log_level`, `feature_flags` (a dict), `allowed_ips` (a list), `secrets` (a dict with keys containing `"key"` or `"password"`)

**Class Design**
- Build a `Config` class with `__init__(self, environment, **settings)`
- Add `validate(self)` that uses guard clauses to check: environment is a known string, `db_port` is an int between 1 and 65535, `replicas` is a positive int, `log_level` is in an allowed set — return a list of validation errors
- Add `merge(self, *override_configs)` that applies each override dict in order (later ones win), returning a new `Config`
- Add `diff(self, other_config)` returning a dict of changed keys with `{"from": old_val, "to": new_val}`
- Add `redact(self)` that returns a copy of settings where any key containing `"secret"`, `"key"`, or `"password"` has its value replaced with `"***REDACTED***"`

**Functions**
- Write `promote(source_config, target_env, *locked_keys, **overrides)` that creates a new config for `target_env` by copying `source_config`, blocking changes to `locked_keys`, and applying `overrides`
- Write `audit_diff(config_a, config_b)` that produces a human-readable change report using f-strings

**Processing & Output**
- Use `filter()` with a lambda to find all config keys whose values changed between staging and prod
- Use `sorted()` with a lambda to sort validation errors alphabetically
- Use `map()` with a lambda to produce `"KEY=VALUE"` formatted strings for non-sensitive config values
- Use a dict comprehension to build a redacted version of the config
- Use a set to track which environments have been validated
- Use `zip()` to pair environment names with their validation results in a summary
- Use `enumerate()` to number each validation error in the output

**Concepts Practiced:** Classes, `*args`, `**kwargs`, dicts, sets, lists, guard clauses, conditionals, string methods, f-strings, `filter`, `sorted`, `map`, `zip`, `enumerate`, dict comprehension, lambda

---

## Project 7: Network Port Scanner and Security Auditor

**Real-World Context:** Security engineers scan for open ports and check them against policy baselines. This project builds that auditing tool.

**What You'll Build:**
A network audit tool that scans port data, classifies ports by risk, compares against baselines, and generates a security report.

**Requirements:**

**Data Setup**
- Create a list of at least 10 host scan result tuples: `(hostname, ip, [open_ports], scan_timestamp, os_guess)`
- Example: `("web-prod-01", "10.0.1.5", [22, 80, 443, 8080, 3306], "2024-01-15T14:30:00", "Ubuntu 22.04")`
- Define a baseline policy dict: `{"allowed_ports": {22, 80, 443}, "forbidden_ports": {23, 21, 3389}, "review_required": {8080, 8443, 3306}}`

**Class Design**
- Build a `HostAudit` class with `__init__(self, hostname, ip, open_ports, **metadata)`
  - `open_ports` stored as both a list (ordered, for reporting) and a set (for fast lookups)
  - `metadata` includes `scan_timestamp`, `os_guess`, etc.
- Add `audit(self, policy)` that compares open ports against the policy, returning a dict with `violations` (list), `warnings` (list), `compliant_ports` (list)
- Add `risk_score(self)` that computes a numeric score: each forbidden port = 10 points, each review port = 3 points, each unknown port = 1 point — return as a float
- Add `__str__` with a formatted f-string summary

- Build a `SecurityAuditor` class
  - Add `scan(*host_tuples, **policy_overrides)` using `*` unpacking internally to construct `HostAudit` objects from each tuple
  - Add `full_report(self)` that generates the complete audit
  - Add `hosts_by_risk(self)` that returns hosts sorted by risk score

**Processing & Output**
- Use `sorted()` with a lambda to rank hosts by risk score descending
- Use `filter()` with a lambda to find all hosts with at least one forbidden port open
- Use `map()` with a lambda to produce a `"hostname (score: X)"` string per host
- Use a set comprehension to find all ports that appear on more than one host (requires a loop + set logic)
- Use a dict comprehension to build `{hostname: risk_score}` for the full inventory
- Use `enumerate()` in the ranked report output
- Use `zip()` to pair each host with its audit result
- Use a list comprehension to flatten all open ports across all hosts into one list
- Use `range()` and a while loop to simulate rescanning flagged hosts up to 3 times

**Concepts Practiced:** Classes, tuples, sets, lists, dicts, `*args`, `**kwargs`, `*` unpacking, guard clauses, conditionals, `sorted`, `filter`, `map`, comprehensions (list/set/dict), `enumerate`, `zip`, `range`, while loop, f-strings, floats, integers

---

## Project 8: Incident Management and On-Call Routing System

**Real-World Context:** Tools like PagerDuty route alerts to the right on-call engineer based on severity, service ownership, and schedules. This project builds that routing logic.

**What You'll Build:**
An incident management system that creates incidents, routes them to on-call engineers, escalates unacknowledged incidents, and tracks MTTR (mean time to resolve).

**Requirements:**

**Data Setup**
- Create a list of on-call engineer dicts: `{"name", "team", "services": [...], "escalation_level": int, "contact": str}`
- Create a list of at least 10 raw alert tuples: `(alert_id, service, severity, message, timestamp_minutes)`
  - `severity` is one of `"P1"`, `"P2"`, `"P3"`, `"P4"`
  - `timestamp_minutes` is a number representing minutes since epoch (just use integers like `1440`, `1445`, etc.)

**Class Design**
- Build an `Incident` class with `__init__(self, alert_id, service, severity, message, created_at, **context)`
  - `context` might include `region`, `affected_users`, `runbook_url`
- Add `acknowledge(self, engineer_name)` that sets acknowledged state and records who acknowledged
- Add `resolve(self, resolution_note)` with a guard clause requiring acknowledgment first
- Add `time_to_resolve(self)` — return `None` if not resolved, otherwise return a float representing minutes elapsed (compute from `created_at` and a `resolved_at` you set)
- Add `__str__` with severity, service, and status in a formatted f-string

- Build an `IncidentRouter` class
  - Add `register_oncall(*engineers)` 
  - Add `route(incident)` that finds the right engineer based on service ownership and escalation level using conditionals and guard clauses
  - Add `escalate(*incident_ids, **escalation_options)` where options include `reason`, `notify_manager=False`
  - Add `mttr_report(self)` returning average time-to-resolve as a float, using only resolved incidents

**Processing & Output**
- Use `filter()` with a lambda to get all P1 and P2 incidents
- Use `sorted()` with a lambda to rank unresolved incidents by age (oldest first)
- Use `map()` with a lambda to extract `(incident_id, severity, service)` tuples from all incidents
- Use a dict comprehension to build `{engineer_name: [incident_ids]}` showing each engineer's workload
- Use a list comprehension to find all incidents that have been open longer than a threshold you define
- Use `enumerate()` to display a prioritized incident queue
- Use `zip()` to pair incident IDs with assigned engineer names for a dispatch log
- Use a while loop to simulate an escalation check that keeps escalating until all P1s are acknowledged (max iterations: 5)
- Use `range()` to simulate running the routing engine over 3 alert batches

**Concepts Practiced:** Classes, `__init__`, `*args`, `**kwargs`, tuples, lists, dicts, sets, guard clauses, conditionals, while loop, `range`, `enumerate`, `zip`, `filter`, `sorted`, `map`, dict/list comprehension, f-strings, floats, string methods

---

## Project 9: GitOps Change Tracking and Rollback System

**Real-World Context:** GitOps tools like ArgoCD track every infrastructure change as a versioned commit. This project simulates that change log with full rollback capability.

**What You'll Build:**
A versioned state manager that records every infrastructure change, diffs versions, and supports targeted rollback with audit trails.

**Requirements:**

**Data Setup**
- Define an initial infrastructure state as a nested dict:
  ```
  {
    "services": {"api": {"image": "...", "replicas": 2}, "worker": {...}},
    "databases": {"primary": {"size": "db.t3.medium", "storage_gb": 100}},
    "networking": {"vpc_cidr": "10.0.0.0/16", "subnets": [...]}
  }
  ```

**Class Design**
- Build a `Change` class with `__init__(self, change_id, author, *affected_resources, **details)`
  - `affected_resources` are strings like `"services.api"`, `"databases.primary"`
  - `details` includes `description`, `environment`, `change_type` (`"update"/"create"/"delete"`), `approved_by`
- Add `validate(self)` with guard clauses: must have author, at least one affected resource, valid change_type
- Add `__str__` f-string summary

- Build a `StateManager` class
  - Store a list of `(version_number, state_snapshot, change_object)` tuples as the history
  - Add `apply_change(change, **field_updates)` that deep-copies the current state, applies `field_updates`, and appends a new version tuple — version number is an integer that increments
  - Add `diff_versions(version_a, version_b)` returning a dict of what changed between two versions
  - Add `rollback(target_version, *reasons, **metadata)` with guard clauses checking the version exists and is not the current version
  - Add `audit_log(self, **filters)` accepting filters like `author="ci-bot"`, `environment="prod"`, `change_type="update"`

**Processing & Output**
- Use a list comprehension to extract all version numbers from history
- Use `filter()` with a lambda to get only changes where `change_type == "delete"` (higher risk)
- Use `sorted()` with a lambda to order history by version number
- Use `map()` with a lambda to produce `"v{n} by {author}: {description}"` strings for each history entry
- Use `enumerate()` in the audit log output
- Use `zip()` to pair version numbers with change descriptions for a changelog display
- Use a dict comprehension to build `{version: author}` for all history entries
- Use a set comprehension to collect all unique authors across the change history
- Use a while loop to simulate applying a series of changes from a queue until the queue is empty
- Use `range()` to generate sequential version numbers

**Concepts Practiced:** Classes, `*args`, `**kwargs`, tuples (as history records), lists, dicts, sets, guard clauses, conditionals, for/while loops, `range`, `enumerate`, `zip`, `filter`, `sorted`, `map`, all comprehension types, f-strings, integers, string methods

---

## Project 10: Full DevOps Platform Simulator

**Real-World Context:** This capstone ties everything together. Real platforms like Heroku or Railway give developers a single interface to deploy apps, scale services, monitor health, manage secrets, and view costs — all in one tool.

**What You'll Build:**
A mini DevOps platform with interconnected subsystems: a service registry, a deployment engine, a secrets vault, a metrics collector, and a unified CLI-style command dispatcher.

**Requirements:**

**Class Hierarchy**
- Build a base `PlatformResource` class with `__init__(self, resource_id, name, **tags)`
  - `tags` is stored as a dict
  - Add `tag(self, **new_tags)` to add tags
  - Add `matches_filter(self, **filters)` that returns True if all filters match the resource's tags or attributes

- Build `Service(PlatformResource)` that inherits from `PlatformResource`
  - Additional `__init__` params: `image`, `port`, and `**config` (replicas, env, region, etc.)
  - Add `deploy(self, version, *changed_files, **deploy_options)` that records a deployment entry
  - Add `scale(self, replicas)` with a guard clause
  - Add `health_check(self)` returning `"HEALTHY"`, `"DEGRADED"`, or `"DOWN"` based on a simulated condition using the service's current state

- Build `SecretsVault` (standalone class, not inheriting)
  - `__init__` stores secrets in a dict internally
  - Add `set_secret(key, value, **metadata)` where metadata includes `created_by`, `environment`, `expires_in_days`
  - Add `get_secret(key, requestor)` with a guard clause checking the key exists
  - Add `list_secrets(redacted=True)` using `map()` with a lambda to redact values when `redacted=True`
  - Add `expiring_soon(days_threshold)` using `filter()` with a lambda on `expires_in_days`

- Build `MetricsCollector` (standalone class)
  - `__init__` stores a dict of `{service_name: [metric_readings]}` where each reading is a tuple `(timestamp_int, cpu, mem, req_per_sec)`
  - Add `record(service_name, *readings)` to add multiple readings at once
  - Add `average(service_name, metric)` where `metric` is `"cpu"`, `"mem"`, or `"rps"` — use `map()` to extract the right column, then compute average manually
  - Add `anomalies(service_name, **thresholds)` returning readings that breach any threshold

- Build a `Platform` class that composes all of the above
  - `__init__` creates a `SecretsVault`, a `MetricsCollector`, and an empty service registry (dict)
  - Add `register_service(*service_objects)`
  - Add `execute(command, *args, **kwargs)` that acts as a command dispatcher — `command` is a string like `"deploy"`, `"scale"`, `"health"`, `"cost"`, `"secrets"` — route to the right method using a dict of lambdas (the dispatch table is a dict where values are lambdas)
  - Add `platform_report(self, **filters)` that produces a full status report across all subsystems

**Processing & Output**
- Use `filter()` with a lambda inside `platform_report` to find unhealthy services
- Use `sorted()` with a lambda to rank services by average CPU usage
- Use `map()` with a lambda to generate a deployment history summary string per service
- Use a dict comprehension to build `{service_name: health_status}` for the whole platform
- Use a set comprehension to collect all unique regions services are deployed in
- Use a list comprehension to find all services with `replicas < 2`
- Use `enumerate()` in the platform report to number each service
- Use `zip()` to pair service names with their latest metric readings
- Use `range()` and a while loop to simulate a monitoring loop that checks health every "tick" for 5 ticks
- Use `**` unpacking when calling internal methods from `execute()`
- Use `*` unpacking when passing stored args to methods from the dispatcher
- Use `zip()` + `dict()` pattern to build service config dicts from parallel key/value lists

**Final Challenge:**
Write a `run_demo()` function at the bottom of your file that exercises every subsystem: register services, deploy them, inject secrets, record metrics, fire the health check loop, and print a full platform report. This function should use no classes directly — only the `Platform.execute()` dispatcher.

**Concepts Practiced:** ALL topics — inheritance, `super()`, `*args`, `**kwargs`, `*` and `**` unpacking in calls, lambdas as dict values (dispatch table), `filter`, `sorted`, `map`, all comprehension types, guard clauses, all conditionals, for/while loops, `range`, `enumerate`, `zip`, tuples, sets, lists, dicts, f-strings, floats, integers, string methods (`.split()`, `.strip()`, `.replace()`, `.lower()`)

