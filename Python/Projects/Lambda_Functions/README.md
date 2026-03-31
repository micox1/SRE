# 15 DevOps Python Projects: *args, **kwargs & Lambda Functions

> **Topics Covered:** `*args`, `**kwargs`, `*` unpacking in calls, `**` unpacking in calls, lambda functions, `sorted()` with lambda, `map()`, `filter()`
>
> **Difficulty:** Moderate to Hard | **Focus:** DevOps Engineering

---

## Project 1: Multi-Target Log Shipper

**Concept:** Build a log shipping utility that accepts a variable number of destination targets (files, endpoints, stdout) and optional configuration settings per target.

**Your Task:**
Write a function `ship_log(message, *targets, **options)` that:
- Accepts a log `message` as the first positional argument
- Accepts any number of `targets` (strings representing destinations like `"stdout"`, `"file"`, `"http"`)
- Accepts keyword arguments for options such as `log_level="INFO"`, `timestamp=True`, `format="json"`
- Iterates through each target and prints what *would* be sent there, including the options applied

**Extension Challenge:**
- Write a second function `bulk_ship(*messages, **shared_options)` that ships multiple messages at once, applying the same options to all of them
- Use `**shared_options` unpacking when calling `ship_log` internally so you don't repeat yourself

**Concepts Practiced:** `*args`, `**kwargs`, `**` unpacking in calls

---

## Project 2: Dynamic Ansible-Style Inventory Builder

**Concept:** Simulate an Ansible-style inventory system where hosts are grouped with flexible metadata tags.

**Your Task:**
- Write a function `register_host(hostname, *groups, **metadata)` that stores a host entry. Groups might be `"webservers"`, `"prod"`, `"us-east-1"`. Metadata might be `ip="10.0.0.1"`, `os="ubuntu"`, `ssh_port=22`
- Store all registered hosts in a dictionary structure
- Write a function `get_hosts_in_group(group)` that returns all hosts belonging to that group
- Write a function `print_inventory()` that prints a formatted inventory report

**Extension Challenge:**
- Write a `bulk_register(*host_definitions)` where each item in `host_definitions` is a dictionary. Use `**` unpacking to call `register_host` for each one
- Use `filter()` with a lambda to return only hosts where `ssh_port` is not the default `22`

**Concepts Practiced:** `*args`, `**kwargs`, `**` unpacking in calls, `filter()` with lambda

---

## Project 3: CI/CD Pipeline Stage Runner

**Concept:** Build a pipeline executor that runs named stages, supports optional configuration per stage, and collects results.

**Your Task:**
- Write a function `run_stage(stage_name, *commands, **config)` where `commands` are shell command strings (just print them as if executing), and `config` accepts options like `timeout=30`, `retry=3`, `env="production"`
- Write a `run_pipeline(pipeline_name, *stages)` function where each item in `stages` is a tuple of `(stage_name, [commands], {config})`
- Inside `run_pipeline`, unpack each tuple and use `*` and `**` unpacking to call `run_stage`

**Extension Challenge:**
- Use `map()` with a lambda to transform a list of raw stage names (strings) into a formatted status report list, e.g. `"build" → "[ PENDING ] build"`
- Use `filter()` with a lambda to pull out only stages where `retry > 1` from a list of stage config dicts

**Concepts Practiced:** `*args`, `**kwargs`, `*` and `**` unpacking in calls, `map()`, `filter()`

---

## Project 4: Kubernetes Resource Manifest Generator

**Concept:** Build a function that dynamically generates Kubernetes-style resource manifest dictionaries.

**Your Task:**
- Write a function `create_manifest(kind, name, **spec_fields)` that builds a dict representing a K8s manifest. `spec_fields` might include `replicas=3`, `image="nginx:latest"`, `port=80`, `namespace="default"`
- Write a `batch_create(*manifest_configs)` where each config is a dict. Use `**` unpacking to call `create_manifest` for each
- Print each generated manifest in a readable format

**Extension Challenge:**
- Given a list of manifest dicts, use `sorted()` with a lambda to sort them by `kind` alphabetically, then by `name`
- Use `filter()` with a lambda to find all manifests where `namespace == "production"`
- Use `map()` with a lambda to extract just the `name` field from each manifest into a flat list

**Concepts Practiced:** `**kwargs`, `**` unpacking in calls, `sorted()`, `map()`, `filter()`

---

## Project 5: Metrics Aggregation Engine

**Concept:** Build a metrics collector that accepts an arbitrary number of numeric samples and computes statistics based on requested operations.

**Your Task:**
- Write a function `aggregate(*samples, **operations)` where `samples` are float values and `operations` are booleans like `mean=True`, `minimum=True`, `maximum=True`, `stddev=False`
- The function should compute and return only the requested operations as a results dictionary
- Do not use any external libraries — compute statistics manually

**Extension Challenge:**
- Write a `compare_services(**service_samples)` function where each keyword is a service name and the value is a list of samples, e.g. `api=[120, 135, 98]`, `db=[45, 52, 60]`
- Use `sorted()` with a lambda to rank services by their average response time
- Use `map()` with a lambda to normalize all sample values in a list to a 0–1 range

**Concepts Practiced:** `*args`, `**kwargs`, `sorted()` with lambda, `map()`

---

## Project 6: Docker Container Health Monitor

**Concept:** Simulate a container health monitoring system that filters and sorts container status reports.

**Your Task:**
- You are given a list of container dictionaries, each with keys: `id`, `name`, `status` (`"running"`, `"stopped"`, `"exited"`), `cpu_percent`, `mem_mb`, `restarts`
- Create this list yourself with at least 8 containers (make up realistic values)
- Use `filter()` with a lambda to get only containers where `status != "running"`
- Use `filter()` with a lambda to get containers with more than 3 restarts
- Use `sorted()` with a lambda to rank all containers by `cpu_percent` descending
- Use `map()` with a lambda to generate an alert string for each unhealthy container

**Extension Challenge:**
- Write a function `health_report(*container_ids, **thresholds)` where `container_ids` limits which containers to check, and `thresholds` sets limits like `max_cpu=80`, `max_mem=512`, `max_restarts=5`
- The function should return containers violating any threshold

**Concepts Practiced:** `filter()`, `sorted()`, `map()` all with lambdas, `*args`, `**kwargs`

---

## Project 7: Terraform Variable File Generator

**Concept:** Build a utility that generates `.tfvars`-style configuration output from Python function calls.

**Your Task:**
- Write a function `define_vars(**variables)` that accepts keyword arguments representing Terraform variable names and values (strings, ints, bools, lists)
- It should output each variable in `key = value` format, correctly quoting strings but not numbers or booleans
- Write a `merge_var_files(*var_dicts)` function that accepts multiple dictionaries and merges them, with later dicts overriding earlier ones on key conflicts
- Use `**` unpacking when merging

**Extension Challenge:**
- Use `sorted()` with a lambda to output variables alphabetically by key name
- Use `filter()` with a lambda to separate sensitive variables (those whose key contains `"secret"`, `"key"`, or `"password"`) from non-sensitive ones
- Use `map()` with a lambda to redact the values of sensitive variables in printed output

**Concepts Practiced:** `**kwargs`, `**` unpacking, `sorted()`, `filter()`, `map()`

---

## Project 8: Custom Logging Middleware

**Concept:** Build a structured logging decorator-like utility that wraps any function call with before/after log output and timing.

**Your Task:**
- Write a function `logged_call(func, *args, **kwargs)` that:
  - Logs the function name, the positional args, and keyword args before calling
  - Calls `func(*args, **kwargs)` using unpacking
  - Logs the return value and a mock elapsed time after the call
  - Returns the result
- Test it by passing in several different functions (e.g. a deployment function, a restart function) with varying signatures

**Extension Challenge:**
- Write a `batch_logged_calls(*call_specs)` where each spec is a tuple of `(func, args_list, kwargs_dict)`. Unpack and pass each to `logged_call`
- Use `map()` with a lambda to extract just the function names from a list of call specs for a pre-run summary print

**Concepts Practiced:** `*args`, `**kwargs`, `*` and `**` unpacking in calls, `map()`

---

## Project 9: Service Dependency Resolver

**Concept:** Build a dependency-aware service startup system that determines the correct boot order.

**Your Task:**
- Write a function `register_service(name, *dependencies, **config)` where `dependencies` are service names this service requires to start first, and `config` includes options like `critical=True`, `timeout=10`, `port=8080`
- Store all registered services
- Write a `resolve_start_order()` function that performs a basic topological sort — services with no dependencies start first, then those whose dependencies are all already started

**Extension Challenge:**
- Use `sorted()` with a lambda to order services with the same dependency depth by their `timeout` value (ascending)
- Use `filter()` with a lambda to return only `critical=True` services from the registry
- Use `map()` with a lambda to produce a startup command string for each service in order

**Concepts Practiced:** `*args`, `**kwargs`, `sorted()`, `filter()`, `map()`

---

## Project 10: Cloud Cost Analyzer

**Concept:** Build a cost analysis tool that processes cloud resource billing data.

**Your Task:**
- You are given a list of billing records, each a dict with: `service`, `region`, `resource_type`, `hours`, `cost_per_hour`
- Create at least 10 records covering services like `"ec2"`, `"rds"`, `"s3"` across regions like `"us-east-1"`, `"eu-west-1"`
- Use `map()` with a lambda to compute `total_cost = hours * cost_per_hour` for each record
- Use `filter()` with a lambda to get records with `total_cost > 100`
- Use `sorted()` with a lambda to rank records from most to least expensive
- Write a `cost_summary(*services, **filters)` function that accepts optional service names to focus on, and keyword filter options like `region="us-east-1"`, `min_cost=50`

**Concepts Practiced:** `map()`, `filter()`, `sorted()`, `*args`, `**kwargs`

---

## Project 11: Alert Rule Engine

**Concept:** Build a configurable alerting system where rules are defined with flexible conditions.

**Your Task:**
- Write a function `create_rule(rule_name, *conditions, **actions)` where:
  - `conditions` are lambda functions that each accept a metrics dict and return True/False
  - `actions` are keyword arguments like `notify="ops-team"`, `severity="critical"`, `runbook="http://..."`
- Write an `evaluate_rules(metrics_snapshot, *rules)` function that runs each rule's conditions against the snapshot and triggers the actions for rules that fire
- Create at least 4 rules with real-world conditions (e.g., CPU > 90%, error rate > 5%, disk < 10%)

**Extension Challenge:**
- Use `filter()` with a lambda to find all rules where `severity == "critical"` for a priority alert list
- Use `sorted()` with a lambda to sort fired alerts by severity level (define your own severity ordering)

**Concepts Practiced:** `*args`, `**kwargs`, lambdas as values, `filter()`, `sorted()`

---

## Project 12: SSH Config File Parser and Manager

**Concept:** Build a utility to parse, query, and output SSH config-style host blocks.

**Your Task:**
- Write a function `add_host(hostname, **settings)` to register an SSH host entry. Settings might include `User`, `HostName`, `Port`, `IdentityFile`, `ForwardAgent`
- Write a `find_hosts(*tags, **filters)` function where `tags` are partial name matches (e.g., `"prod"`, `"bastion"`) and `filters` are exact field matches like `Port=22`, `User="deploy"`
- Write a `render_config(*hostnames)` function that outputs SSH config block format for the specified hosts (or all if none specified)

**Extension Challenge:**
- Use `sorted()` with a lambda to output hosts alphabetically by hostname
- Use `filter()` with a lambda to find hosts that use a non-standard port (not 22)
- Use `map()` with a lambda to produce a quick-reference list of `user@hostname:port` strings

**Concepts Practiced:** `**kwargs`, `*args`, `*` unpacking, `sorted()`, `filter()`, `map()`

---

## Project 13: Deployment Rollback System

**Concept:** Build a deployment history tracker with rollback capabilities and filtering.

**Your Task:**
- Write a function `record_deployment(service, version, *changed_files, **metadata)` where `changed_files` are filenames deployed and `metadata` includes `deployed_by`, `environment`, `timestamp`, `success=True`
- Maintain a global deployment history list
- Write a `rollback(service, **criteria)` function that finds the most recent successful deployment of a service matching optional criteria like `environment="prod"`, `deployed_by="ci-bot"`

**Extension Challenge:**
- Use `filter()` with a lambda to find all failed deployments (`success=False`)
- Use `sorted()` with a lambda to sort history by timestamp descending
- Use `map()` with a lambda to summarize each deployment as a single-line string: `"[v2.1.0] api | prod | 2024-01-15"`
- Use `filter()` on the mapped summaries to find lines containing a specific service name

**Concepts Practiced:** `*args`, `**kwargs`, `filter()`, `sorted()`, `map()`

---

## Project 14: Infrastructure Diff Tool

**Concept:** Build a tool that compares two infrastructure state snapshots and reports changes.

**Your Task:**
- Write a function `snapshot(**resources)` where each keyword is a resource name and the value is a dict of its properties, e.g. `web_server={"type": "t3.medium", "count": 2}`, `db={"type": "db.t3.small", "storage": 100}`
- Write a `diff(snapshot_a, snapshot_b)` function that returns three categories: `added`, `removed`, `modified`
- For `modified` resources, show which specific fields changed and from what value to what value

**Extension Challenge:**
- Write a `apply_change(*resource_names, **change_fields)` function that simulates applying specific field changes to named resources
- Use `filter()` with a lambda to find only resources where `count` changed (scale events vs config changes)
- Use `sorted()` with a lambda to rank modified resources by number of changed fields (most changed first)
- Use `map()` with a lambda to produce an output line per diff item in a consistent format

**Concepts Practiced:** `**kwargs`, `*args`, `**` unpacking, `filter()`, `sorted()`, `map()`

---

## Project 15: Self-Service DevOps CLI Command Builder

**Concept:** Build a dynamic CLI command construction system that assembles shell commands from structured inputs.

**Your Task:**
- Write a function `build_command(base_cmd, *positional_args, **flags)` that constructs a shell command string. Positional args are appended directly. Flags become `--key value` pairs (booleans become `--key` with no value)
- Write a `run_batch(*command_specs)` function where each spec is a dict with keys `base`, `args` (list), and `flags` (dict). Use `*` and `**` unpacking to call `build_command` for each
- Print the resulting commands (do not actually execute them)

**Extension Challenge:**
- Use `sorted()` with a lambda to sort a list of built commands by length (shortest first — often simpler commands)
- Use `filter()` with a lambda to identify commands that include `--force` or `--delete` flags as potentially dangerous
- Use `map()` with a lambda to prepend `"dry-run: "` to all dangerous commands before printing
- Write a `template_command(base_cmd, *required_args)` that returns a lambda which, when called with `**kwargs`, fills in the flags dynamically — this is a lambda returning a lambda

**Concepts Practiced:** `*args`, `**kwargs`, `*` and `**` unpacking in calls, `sorted()`, `filter()`, `map()`, lambda returning lambda

---
