import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    exit_code: int
    stdout: str
    stderr: str


class CommandCollector:
    def run(self, command: tuple[str, ...], timeout_seconds: int = 10) -> CommandResult:
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                check=False,
                text=True,
                timeout=timeout_seconds,
            )
            return CommandResult(command, completed.returncode, completed.stdout, completed.stderr)
        except FileNotFoundError as error:
            return CommandResult(command, 127, "", str(error))
        except subprocess.TimeoutExpired as error:
            stdout = error.stdout if isinstance(error.stdout, str) else ""
            stderr = error.stderr if isinstance(error.stderr, str) else ""
            return CommandResult(command, 124, stdout, stderr or "command timed out")

