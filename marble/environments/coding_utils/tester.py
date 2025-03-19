# coding_utils/tester.py
import os
import resource
import subprocess
import sys
import tempfile
from typing import Any, Dict, Optional

import pytest


def run_tests_handler(
    env, test_file: str, subdir: Optional[str] = None, verbosity: int = 2
) -> Dict[str, Any]:
    try:
        test_path = env._get_file_path(test_file, subdir)

        # Add workspace to Python path
        sys.path.insert(0, env.workspace_dir)

        # Run pytest programmatically
        pytest_args = [
            test_path,
            f"--verbosity={verbosity}",
            "-p",
            "no:warnings",  # Disable warning capture
            "--tb=short",  # Short traceback
        ]

        test_output = pytest.main(pytest_args)

        # Remove workspace from Python path
        sys.path.pop(0)

        return {
            "success": test_output == pytest.ExitCode.OK,
            "exit_code": test_output,
            "test_file": test_path,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def register_tester_actions(env):
    env.register_action(
        "run_tests",
        handler=lambda **kwargs: run_tests_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Runs tests for the specified file or directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_file": {
                            "type": "string",
                            "description": "Test file to run",
                        },
                        "subdir": {
                            "type": "string",
                            "description": "Optional subdirectory within workspace",
                        },
                        "verbosity": {
                            "type": "integer",
                            "description": "Test output verbosity level",
                        },
                    },
                    "required": ["test_file"],
                },
            },
        },
    )


def create_sandbox_handler(
    env, code: str, test_input: str = "", timeout: int = 5, memory_limit: int = 512
) -> Dict[str, Any]:
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
            temp_file.write(code.encode())
            temp_file_path = temp_file.name

        def limit_resources():
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit * 1024 * 1024, -1))
            resource.setrlimit(resource.RLIMIT_CPU, (timeout, -1))

        process = subprocess.Popen(
            [sys.executable, temp_file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=limit_resources,
        )

        try:
            stdout, stderr = process.communicate(
                input=test_input.encode(), timeout=timeout
            )
            stdout = stdout.decode()
            stderr = stderr.decode()
            return_code = process.returncode

        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "error": "Execution timed out",
                "stdout": "",
                "stderr": "",
                "return_code": -1,
            }

        finally:
            os.unlink(temp_file_path)

        return {
            "success": return_code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def run_test_case_handler(
    env, code: str, test_case: Dict[str, Any], timeout: int = 5
) -> Dict[str, Any]:
    try:
        input_data = test_case.get("input", "")
        expected_output = test_case.get("expected_output", "")

        result = create_sandbox_handler(env, code, input_data, timeout)

        if not result["success"]:
            return result

        actual_output = result["stdout"].strip()
        expected_output = expected_output.strip()

        return {
            "success": actual_output == expected_output,
            "actual_output": actual_output,
            "expected_output": expected_output,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def run_test_suite_handler(
    env, code: str, test_cases: list, timeout: int = 5
) -> Dict[str, Any]:
    results = []
    passed = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases):
        result = run_test_case_handler(env, code, test_case, timeout)
        result["test_case_id"] = i + 1
        results.append(result)
        if result["success"]:
            passed += 1

    return {
        "success": passed == total,
        "passed": passed,
        "total": total,
        "results": results,
    }


def register_sandbox_tester_actions(env):
    env.register_action(
        "create_sandbox",
        handler=lambda **kwargs: create_sandbox_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "create_sandbox",
                "description": "Creates a sandbox environment and executes code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Code to execute"},
                        "test_input": {
                            "type": "string",
                            "description": "Input for the code",
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Execution timeout in seconds",
                        },
                        "memory_limit": {
                            "type": "integer",
                            "description": "Memory limit in MB",
                        },
                    },
                    "required": ["code"],
                },
            },
        },
    )

    env.register_action(
        "run_test_case",
        handler=lambda **kwargs: run_test_case_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "run_test_case",
                "description": "Runs a single test case against the code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Code to test"},
                        "test_case": {
                            "type": "object",
                            "description": "Test case with input and expected output",
                            "properties": {
                                "input": {"type": "string"},
                                "expected_output": {"type": "string"},
                            },
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Execution timeout in seconds",
                        },
                    },
                    "required": ["code", "test_case"],
                },
            },
        },
    )

    env.register_action(
        "run_test_suite",
        handler=lambda **kwargs: run_test_suite_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "run_test_suite",
                "description": "Runs multiple test cases against the code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Code to test"},
                        "test_cases": {
                            "type": "array",
                            "description": "List of test cases",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "input": {"type": "string"},
                                    "expected_output": {"type": "string"},
                                },
                            },
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Execution timeout in seconds",
                        },
                    },
                    "required": ["code", "test_cases"],
                },
            },
        },
    )
