from netpreflight.models import ValidationReport


def format_console_report(report: ValidationReport) -> str:
    output_lines: list[str] = []

    for result in report.results:
        line = (
            f"[{result.status}] "
            f"{result.device} - {result.check_name}"
        )

        if result.message is not None:
            line += f": {result.message}"

        output_lines.append(line)

    if report.results:
        output_lines.append("")

    summary_line = (
        f"Summary: {report.passed_count} passed, "
        f"{report.failed_count} failed"
    )
    output_lines.append(summary_line)

    return "\n".join(output_lines)
