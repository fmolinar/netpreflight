from dataclasses import dataclass

PathSegment = str | int
# alias for a path segment, which can be either a string (for dictionary keys) or an integer (for list indices)
Path = tuple[PathSegment, ...]


@dataclass(frozen=True, slots=True)
class ValidationResult:
    device: str
    check_name: str
    passed: bool
    actual: object
    expected: object
    message: str | None = None

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"


@dataclass(frozen=True, slots=True)
class CheckDefinition:
    name: str
    path: Path
    expected: object


@dataclass(frozen=True, slots=True)
class ValidationReport:
    results: tuple[ValidationResult, ...]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.results if result.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for result in self.results if not result.passed)
