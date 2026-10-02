from dataclasses import dataclass


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
