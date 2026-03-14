Must Follow: Python Project Engineering Standards

1. Environment & Dependency Management
Rule: Total Isolation and Determinism
Tooling: Use uv for all project management (faster, unified interface).
Virtual Environments: Every project must have a dedicated .venv managed strictly by uv.
Locking: All dependencies and transitive versions must be locked in a pyproject.toml and uv.lock to ensure environment parity.
2. Code Quality & Style
Rule: Automated Enforcement (The "No-Debate" Policy)
Formatting: Use Black for uncompromising, uniform code layout.
Linting: Use Ruff for high-performance PEP 8 compliance and logical error detection.
Documentation: All public-facing modules, classes, and functions must use Google Style Docstrings.
3. Type Safety & Static Analysis
Rule: Explicit over Implicit
Type Hinting: Every function signature must include type hints for all arguments and the return value.
Static Analysis: Use Mypy in strict mode to verify type consistency. Code failing Mypy is considered "broken."
4. Data Modelling & Validation
Rule: Source-Based Tool Selection
Internal Data (Performance): Use dataclasses with slots=True. This eliminates __dict__ overhead, reducing memory usage and increasing access speed for internal state and math entities.
External Data (Safety): Use Pydantic V2+ for data entering from APIs, JSON, or Databases. It provides mandatory runtime validation and type coercion.
5. Testing & Quality Assurance
Rule: 100% Testability
Framework: Use Pytest with fixtures to maintain DRY (Don't Repeat Yourself) test code.
Logic Separation: Decouple business logic from framework code (e.g., FastAPI/Django) to ensure easy unit testing.
CI Pipeline: Every push must trigger an automated pipeline running Ruff, Mypy, and Pytest.
6. Error Handling & Logging
Rule: Fail Fast and Record Everything
Specific Exceptions: Catch only expected errors (e.g., ValueError); never use a bare except:.
Structured Logging: Use the built-in logging module or Loguru for leveled output (INFO, WARNING, ERROR).
No Silent Failures: Log all unresolved exceptions with full stack traces using logging.exception().
Environment Awareness: Set logs to DEBUG in dev and INFO/WARNING in production via environment variables.
7. Performance & Memory Optimization
Rule: Explicit Resource Management
Memory Footprint: Use slots=True in dataclasses for high-frequency internal objects.
Context Managers: Use with statements for all I/O (files, network, DB) to ensure deterministic cleanup.
Lazy Evaluation: Use generators (yield) for large datasets to maintain $O(1)$ memory complexity.
