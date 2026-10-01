# netpreflight

netprefligth is a Python toolkit for validating network state before and after infrastructure changes.

It allows network engineers to define expected conditions in YAML, collect operational data from network devices, evaluate that data, and produce a clear pass/fail report. It is designed to work as both a command-line tool and an importable Python library.

> [!IMPORTANT]
> This project is in early development, The interfaces and examples below describe the intended first release and may change before version `0.1.0`.

## The problem

Network changes are often validated manually by connecting to devices, running show commands, and visually comparing their output. This process is repetitive, difficult to reproduce, and easy to perform inconsistently.

Automation tools can push configurations, but a successful configuration task does not necessarily mean the network reached the intended operational state, for example:

- An interface configuration may be accepted while the interface remains down.
- An OSPF or BGP neighbor may fail to establish after the change.
- A route may disappear even though the deployment completed successfully.
- A change may produce an unexpected difference elsewhere in the network.

`netpreflight` separates **deployment success** from **network validation**. It answers the question:

> Did the network reach the state we expected?

## WHat the project will provide

The initial version of `netpreflight` will provide:

- A YAML inventory describing network devices.
- YAML-based validation checks that do not require users to write Python.
- Device command execution through a pluggable connection adapter.
- Structured parsing through pyATS/Genie.
- Reusable assertions such as `equals`, `contains`, `exists`, `greater_than`, and `less_than`.
- Human-readable console output.
- Machine-readable JSON output.
- Predictable exit codes for CI/CD pipelines.
- A Python API for applications and custom automation.

Future versions may add:

- Ansible modules, action plugins, or callback plugins.
- Pre-change and post-change snapshots.
- State comparison and configuration-drift detection.
- JUnit XML and HTML reports.
- Additional network platforms and parsing backends.
- Parallel device validation.

## Intended workflow

A typical network change workflow looks like this:

1. Run pre-change checks and optionally capture a snapshot.
2. Apply the network change with ANsible, Terraform, or other tool.
3. Run post-change checks.
4. Return a nonzero exit code if validation fails.
5. Store the report as a CI/CD artifact or use it to trigger remediation.

`netpreflight` does not replace Ansible, Terraform, or pyATS. It provides a small validation layer that can be used alongside them.

## Installation

The package is not yet published. Once the first release is available, the intended installation command will be:

```bash
python -m pip install netpreflight
```

During local development, it will be installed in editable mode:

```bash
python -m pip install --editable ".[dev]"
```

## Quick Start

### 1. Create an inventory

Create `inventory.yaml`:

```yaml
devices:
  router-01:
    os: iosxe
    connections:
      cli:
        protocol: ssh
        host: 192.0.2.10
        port: 22
    credentials:
      username_env: NETPREFLIGHT_USERNAME
      password_env: NETPREFLIGHT_PASSWORD
```


Credentials should be supplied through environment variables or an external secret provider. They should not be committed to the inventory file.

```bash
export NETPREFLIGHT_USERNAME="automation"
export NETPREFLIGHT_PASSWORD="replace-with-a-secret"
```

### 2. Define validation checks

Create `checks.yml`

```yaml
checks:
  - name: Uplink is operational
    devices:
      - router-01
    command: show interfaces GigabitEthernet1
    parser: pyats
    assert:
      path: GigabitEthernet1.oper_status
      operator: equals
      expected: up

  - name: Default route exists
    devices:
      - router-01
    command: show ip route
    parser: pyats
    assert:
      path: vrf.default.address_family.ipv4.routes.0.0.0.0/0
      operator: exists
```

The exact check schema is part of the version `0.1.0` design work and may change during implementation.

### 3. Run validation

```bash
netpreflight check \
  --inventory inventory.yml \
  --checks checks.yml
```

Example output:

```text
router-01
  PASS  Uplink is operational
  FAIL  Default route exists

Summary: 1 passed, 1 failed
```

To generate JSON output:

```bash
netpreflight check \
  --inventory inventory.yml \
  --checks checks.yml \
  --format json
```

## Python API

Applications will also be able to use the validation engine directly:

```python
from netpreflight import NetworkValidator

validator = NetworkValidator.from_files(
    inventory="inventory.yml",
    checks="checks.yml",
)

report = validator.run()

for result in report.results:
    print(result.device, result.check_name, result.passed)

if not report.passed:
    raise SystemExit(1)
```

The CLI and Python API will use the same validation engine so that their behavior remains consistent.

## Exit codes

The planned command-line exit codes are:


| Code | Meaning |
| ---: | --- |
| `0` | All validation checks passed. |
| `1` | One or more validation checks failed. |
| `2` | The command could not run because of invalid input, a connection problem, or another execution error. |

This distinction allows a pipeline to tell the difference between an unhealthy network state and a problem running the validation tool.


## Planned architecture

The project will keep its core domain logic independent from external tools:

```text
CLI / Python API
       |
Validation runner
       |
Inventory + checks + assertions
       |
Connection and parser adapters
       |
pyATS/Genie and future backends
```

The adapter boundary is important because it allows the validation engine and assertion logic to be tested without connecting to real devices

## Development roadmap

### Milestone 1: Package foundation

- Create the `src/` package layout.
- Configure `pyproject.toml`.
- Add a minimal CLI entry point.
- Configure pytest, linting, and type checking.

### Milestone 2: Domain models and input loading

- Define device, check, assertion, result, and report models.
- load YAML safely.
- Validate input and return helpful errors.
- Resolve credentials from environment variables.

### Milestone 3: Validation engine

- Implement path lookup in parsed data.
- Implement the initial assetion operators.
- Distinguish failed checks from execution errors.
- Unit-test the engine with static fixtures.

### Milestone 4: pyATS adapter

- Convert inventory data into a pyATS-compatible testbed.
- Connect to devices.
- execute and parse commands.
- Normalize adapter errors.

### Milestone 5: Reporting and CLI

- Add readable terminal output.
- Add JSON output.
- Implement stable exit codes.
- Add logging and optional verbosity.

### Milestone 6: Release

- Add complete user documentation and examples.
- Build the source distribution and wheel.
- Test the built package in a clean virtual environment
- Publish a release candidate to TestPyPI.
- Publish version `0.1.0` to PyPI.


## Proposed repository layout

```text
netpreflight/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── netpreflight/
│       ├── __init__.py
│       ├── cli.py
│       ├── inventory.py
│       ├── models.py
│       ├── runner.py
│       ├── assertions.py
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── pyats_adapter.py
│       └── reports/
│           ├── __init__.py
│           ├── console.py
│           └── json_report.py
└── tests/
    ├── fixtures/
    ├── test_assertions.py
    ├── test_inventory.py
    └── test_runner.py
```

The layout may evolve as the public interfaces become clearer. New abstractions should be added only when the implementation demonstrates that they are needed.

## Design principles:

- **Simple for users** common checks should require YAML, not Python.
- **Useful as a library** Python users should have access to typed results and explicit exceptions.
- **Safe by default** credentials must not appear in reports or logs.
- **Backend-independent core:** assertions should operate on ordinary Python data structures.
- **Testable without devices** most test should use fixtures and fake adapters.
- **Helpful failures:** errors should explain the device, check, operation , and likely correction.
- **Stable automation behavior** output formats and exit codes should be trated as public interfaces.


## Project status

`netpreflight` is currently in the design and learning phase. The first goal is a smal well-tested vertical slice:

 1. Load one device and one check from YAML.
 2. Obtain structured command data through a fake adapter.
 3. Evaluate an `equals` assertion.
 4. Print a result and return the correct exit code.

Once the path works end to end, pyATS device connectivity and additional operators will be added incrementally.

## Contributing

Contributions guidelines will be added after the first working release. Early feedback on the check schema, reports, supported platforms, and integration workflow is welcome.

## License

MIT