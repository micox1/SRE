# DevOps Python Capstone Projects

---

## Project 1: Infrastructure Inventory & Health Dashboard

DevOps engineers live and die by their ability to see what's running, where, and whether it's healthy. You're building the inventory system that makes that possible.

At its core you need two classes — one that represents a single server and knows how to evaluate its own health, and one that manages a collection of servers and can answer questions about them. The health evaluation needs to be opinionated: a server is either healthy, degraded, or critical, and the logic should check for missing data before it checks anything else. The inventory class needs to support bulk registration, role-based filtering, and flexible querying that can accept any combination of filter criteria at call time.

On top of the class system, you'll process the inventory using the full toolkit — sorting, filtering, transforming, pairing servers with metadata from a separate list, collecting unique values, and building lookup structures. Simulate multiple health check cycles using a loop.

Use at least 8 servers with varied roles and metrics. Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 2: CI/CD Pipeline Execution Engine

Every CI/CD platform — Jenkins, GitHub Actions, GitLab — models a build as an ordered sequence of stages. You're building the engine that runs them.

You need two classes. One represents a single stage, accepts any number of commands and configuration options at construction time, and knows how to run itself — iterating through commands, detecting failures by inspecting the command string, retrying based on config, and returning a result. The other represents a full pipeline: it holds stages, accepts metadata about the run, can receive additional stages after construction, and runs everything in order — stopping on failure unless the stage is marked as fault-tolerant.

Once the pipeline runs, process the results. Identify which stages passed, rank them by duration, produce a status badge for each, and build lookup structures from the output. Use a while loop inside stage execution for retry logic.

Simulate commands using string inspection — no need for subprocess. Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 3: Cloud Cost Optimization Analyzer

Cloud bills are full of waste. Your job is to build the tool that finds it.

You're working with billing records — each one captures a service, a resource, a region, usage hours, rate, and how heavily the resource was actually used. Your system needs to compute total costs across any number of records, flag underutilized resources based on configurable thresholds, break costs down by service, and produce a concrete recommendation for each resource: terminate it, downsize it, review it, or mark it as rightsized. The recommendation logic should check for edge cases before drawing conclusions.

Use at least 12 records stored as tuples. Process the full dataset using the complete toolkit — computing costs with map, filtering waste, ranking by cost, pairing IDs with recommendations, collecting unique resource types with set comprehension. Simulate three months of historical data using range.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 4: Kubernetes Cluster State Manager

Kubernetes works by constantly comparing what you want to what you have, and reconciling the difference. You're building that reconciliation engine.

You need a class that models a single deployment — it knows its image, namespace, and resource spec, can be scaled with validation, can compare itself to another deployment and report what differs, and can serialize itself into a manifest-style dict. On top of that, you need a cluster class that maintains separate desired and actual state registries, can apply new desired deployments in bulk, and can produce a reconciliation plan — a list of actions (create, update, delete) needed to bring actual state in line with desired state.

Use a while loop to simulate the reconciliation loop running until the states converge or a max iteration count is hit. Process the deployment inventory using the full toolkit — filtering single points of failure, sorting by replica count, building snapshot lookups, collecting namespaces.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 5: Log Aggregation and Alerting System

Logs are raw text until something parses them. You're building that parser and everything that sits on top of it.

You need a class that takes a raw log line and turns it into structured data — timestamp, level, service, message. It should handle malformed input gracefully before it tries to parse anything. On top of that, you need an aggregator that ingests any number of raw lines at once, supports filtering by level or service, computes per-level statistics, and can evaluate a set of configurable alert rules against the ingested data.

Build a realistic dataset of at least 15 raw log strings covering multiple services and severity levels. Process the full log set — extracting errors, sorting by timestamp, identifying unique services, building per-service error counts, labeling each entry. Simulate batch reprocessing using range.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 6: Multi-Environment Deployment Configuration Manager

Teams run dev, staging, and prod — and keeping those configs consistent, safe, and auditable is a real engineering problem. You're building the tool that manages it.

You need a class that holds environment-specific configuration, can validate it against a set of rules (checking for bad ports, invalid log levels, missing fields), can merge in any number of override configs, can diff itself against another config, and can produce a redacted copy that masks any secrets. On top of the class, write a standalone function that handles environment promotion — copying a config to a new environment, protecting locked keys, applying overrides — and another that produces a human-readable change report.

Define base config dicts for dev, staging, and prod. Process them using the full toolkit — filtering changed keys, sorting validation errors, formatting non-sensitive values, pairing environments with their validation results. Track which environments have been validated.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 7: Network Port Scanner and Security Auditor

Security engineers don't just scan ports — they audit them against a policy and report on what's wrong. You're building that audit system.

You need a class that models a single host's scan result, stores its open ports in a way that supports both ordered reporting and fast lookups, audits those ports against a passed-in policy, and computes a numeric risk score based on what it finds. On top of that, a security auditor class accepts raw scan tuples, constructs host objects from them, and produces a full ranked report.

Define a baseline policy with allowed, forbidden, and review-required port sets. Build a dataset of at least 10 host tuples. Process the full inventory — ranking by risk, filtering high-risk hosts, building risk score lookups, flattening all open ports, identifying ports that appear across multiple hosts. Simulate rescanning flagged hosts with a while loop.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 8: Incident Management and On-Call Routing System

When something breaks at 3am, the right engineer needs to be paged immediately. You're building the routing logic that makes that happen.

You need a class that models a single incident — it can be acknowledged, resolved (but not before it's acknowledged), and can report how long it took to resolve. On top of that, an incident router that maintains an on-call roster, routes incoming incidents to the right engineer based on service ownership and escalation level, supports bulk escalation with configurable options, and can compute mean time to resolve across all closed incidents.

Build a dataset of at least 10 alert tuples with varied severities and services. Process the incident queue — filtering by severity, ranking by age, extracting key fields, building per-engineer workload maps, identifying long-running incidents. Use a while loop to simulate escalation until all P1s are acknowledged.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 9: GitOps Change Tracking and Rollback System

GitOps tools track every infrastructure change as a versioned snapshot. You're building that version control system.

You need a class that represents a single change — it carries an author, a set of affected resources, and metadata about what changed and why. It should validate itself before being applied. On top of that, a state manager that stores the full history as versioned tuples, can apply changes by snapshotting current state and appending a new version, can diff any two versions, can roll back to a previous version with guard clauses protecting against invalid targets, and supports filtered audit queries.

Define an initial infrastructure state as a nested dict with services, databases, and networking. Process the history using the full toolkit — extracting version numbers, filtering high-risk deletions, sorting by version, generating changelog strings, building author lookups, collecting unique contributors. Use a while loop to drain a queue of pending changes.

Deliver clean, working code. Be prepared to walk through every decision you made.

---

## Project 10: Full DevOps Platform Simulator

This is the capstone. Everything you've built across the previous nine projects comes together here.

You're building a mini DevOps platform with four interconnected subsystems — a service registry, a secrets vault, a metrics collector, and a unified command dispatcher — composed inside a single platform class.

The service registry manages `Service` objects that inherit from a shared base class. Services can be deployed, scaled, and health-checked. The base class handles tagging and filter matching. The secrets vault stores secrets with metadata, supports redaction, and can surface secrets that are expiring soon. The metrics collector stores time-series readings per service and can compute averages and detect anomalies. The platform class ties all of this together through an `execute` method that dispatches string commands to the right subsystem using a dict of lambdas as a dispatch table.

Process the full platform state in the report — filtering unhealthy services, ranking by CPU, generating deployment summaries, building health lookup dicts, collecting unique regions, finding under-replicated services. Use range and a while loop to simulate a monitoring cycle.

At the bottom of the file, write a `run_demo` function that exercises every subsystem exclusively through the `execute` dispatcher — no direct class calls. If `run_demo` can drive the entire platform, you've built it right.

Deliver clean, working code. Be prepared to walk through every decision you made.