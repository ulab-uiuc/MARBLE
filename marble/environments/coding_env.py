import os
import ast
import sys
import time
import pytest
import typing
import logging
import subprocess
from typing import Any, Dict, List, Optional, Tuple
from marble.environments.base_env import BaseEnvironment

class CodingEnvironment(BaseEnvironment):
    """Enhanced coding environment with comprehensive development tools."""

    def __init__(self, config: Dict[str, Any], name: str = "CodingEnv"):
        """
        Initialize the CodingEnvironment.

        Args:
            config (Dict[str, Any]): Configuration dictionary
            name (str): Name of the environment
        """
        super().__init__(name, config)
        
        self.workspace_dir = config.get("workspace_dir", "workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        
        self.register_standard_actions()
        
    def register_standard_actions(self) -> None:
        """Register all standard actions available in the coding environment."""
        # File Operations
        self._register_file_actions()
        # Code Analysis 
        self._register_analysis_actions()
        # Testing
        self._register_testing_actions()
        # Documentation
        self._register_documentation_actions()

    def _register_file_actions(self) -> None:
        """Register all file-related actions."""
        self.register_action(
            "create_file",
            handler=self._create_file_handler,
            description={
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Creates a new file in the workspace with specified content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the file to create"},
                            "content": {"type": "string", "description": "Content to write to the file"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"}
                        },
                        "required": ["filename", "content"]
                    }
                }
            }
        )

        self.register_action(
            "read_file",
            handler=self._read_file_handler,
            description={
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Reads content from an existing file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the file to read"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"}
                        },
                        "required": ["filename"]
                    }
                }
            }
        )

        self.register_action(
            "update_file",
            handler=self._update_file_handler,
            description={
                "type": "function",
                "function": {
                    "name": "update_file",
                    "description": "Updates content in an existing file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the file to update"},
                            "content": {"type": "string", "description": "New content"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"},
                            "mode": {"type": "string", "enum": ["w", "a"], "description": "Write mode"}
                        },
                        "required": ["filename", "content"]
                    }
                }
            }
        )

    def _register_analysis_actions(self) -> None:
        """Register all code analysis actions."""
        self.register_action(
            "analyze_code",
            handler=self._analyze_code_handler,
            description={
                "type": "function",
                "function": {
                    "name": "analyze_code",
                    "description": "Performs comprehensive code analysis",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the file to analyze"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"},
                            "analysis_type": {
                                "type": "string", 
                                "enum": ["syntax", "style", "complexity", "typing", "security", "all"],
                                "description": "Type of analysis to perform"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            }
        )

    def _register_testing_actions(self) -> None:
        """Register all testing-related actions."""
        self.register_action(
            "run_tests",
            handler=self._run_tests_handler,
            description={
                "type": "function",
                "function": {
                    "name": "run_tests",
                    "description": "Runs tests for the specified file or directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "test_file": {"type": "string", "description": "Test file to run"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"},
                            "verbosity": {"type": "integer", "description": "Test output verbosity level"}
                        },
                        "required": ["test_file"]
                    }
                }
            }
        )

    def _register_documentation_actions(self) -> None:
        """Register all documentation-related actions."""
        self.register_action(
            "check_documentation",
            handler=self._check_documentation_handler,
            description={
                "type": "function",
                "function": {
                    "name": "check_documentation",
                    "description": "Checks documentation completeness and quality",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "File to check documentation"},
                            "subdir": {"type": "string", "description": "Optional subdirectory within workspace"},
                            "doc_type": {
                                "type": "string",
                                "enum": ["docstrings", "comments", "readme", "all"],
                                "description": "Type of documentation to check"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            }
        )

    def _get_file_path(self, filename: str, subdir: Optional[str] = None) -> str:
        """
        Constructs the full file path within the workspace.
        
        Args:
            filename (str): Name of the file
            subdir (Optional[str]): Optional subdirectory within workspace
            
        Returns:
            str: Full file path
        """
        if subdir:
            full_path = os.path.join(self.workspace_dir, subdir)
            os.makedirs(full_path, exist_ok=True)
            return os.path.join(full_path, filename)
        return os.path.join(self.workspace_dir, filename)

    def _create_file_handler(self, filename: str, content: str, subdir: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new file with the specified content."""
        try:
            file_path = self._get_file_path(filename, subdir)
            with open(file_path, 'w') as f:
                f.write(content)
            return {
                "success": True,
                "message": f"File created successfully: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_file_handler(self, filename: str, subdir: Optional[str] = None) -> Dict[str, Any]:
        """Reads content from an existing file."""
        try:
            file_path = self._get_file_path(filename, subdir)
            with open(file_path, 'r') as f:
                content = f.read()
            return {
                "success": True,
                "content": content,
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _update_file_handler(self, filename: str, content: str, 
                           subdir: Optional[str] = None, mode: str = 'w') -> Dict[str, Any]:
        """Updates content in an existing file."""
        try:
            file_path = self._get_file_path(filename, subdir)
            with open(file_path, mode) as f:
                f.write(content)
            return {
                "success": True,
                "message": f"File updated successfully: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _analyze_code_handler(self, filename: str, subdir: Optional[str] = None,
                            analysis_type: str = "all") -> Dict[str, Any]:
        """Performs comprehensive code analysis."""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            analysis_results = {
                "syntax": None,
                "style": None,
                "complexity": None,
                "typing": None,
                "security": None
            }
            
            with open(file_path, 'r') as f:
                code = f.read()
                
            # Syntax check
            if analysis_type in ["syntax", "all"]:
                try:
                    ast.parse(code)
                    analysis_results["syntax"] = "No syntax errors found"
                except SyntaxError as e:
                    analysis_results["syntax"] = f"Syntax error: {str(e)}"
            
            # Style check (basic)
            if analysis_type in ["style", "all"]:
                style_issues = []
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not ast.get_docstring(node):
                            style_issues.append(f"Missing docstring in function {node.name}")
                analysis_results["style"] = style_issues if style_issues else "No style issues found"
            
            # Complexity analysis (basic)
            if analysis_type in ["complexity", "all"]:
                complexity_info = {"functions": {}}
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = 1  # Base complexity
                        for child in ast.walk(node):
                            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                                complexity += 1
                        complexity_info["functions"][node.name] = complexity
                analysis_results["complexity"] = complexity_info
            
            # Type hint check
            if analysis_type in ["typing", "all"]:
                type_issues = []
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not node.returns and not any(
                            isinstance(ann, ast.AnnAssign) for ann in node.body):
                            type_issues.append(f"Missing type hints in function {node.name}")
                analysis_results["typing"] = type_issues if type_issues else "No typing issues found"
            
            return {
                "success": True,
                "analysis": analysis_results,
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _run_tests_handler(self, test_file: str, subdir: Optional[str] = None, 
                          verbosity: int = 2) -> Dict[str, Any]:
        """Runs tests using pytest."""
        try:
            test_path = self._get_file_path(test_file, subdir)
            
            # Add workspace to Python path
            sys.path.insert(0, self.workspace_dir)
            
            # Run pytest programmatically
            pytest_args = [
                test_path,
                f"--verbosity={verbosity}",
                "-p", "no:warnings",  # Disable warning capture
                "--tb=short"  # Short traceback
            ]
            
            test_output = pytest.main(pytest_args)
            
            # Remove workspace from Python path
            sys.path.pop(0)
            
            return {
                "success": test_output == pytest.ExitCode.OK,
                "exit_code": test_output,
                "test_file": test_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _check_documentation_handler(self, filename: str, subdir: Optional[str] = None,
                                   doc_type: str = "all") -> Dict[str, Any]:
        """Checks documentation completeness and quality."""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            doc_results = {
                "docstrings": None,
                "comments": None,
                "readme": None
            }
            
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Check docstrings
            if doc_type in ["docstrings", "all"]:
                doc_issues = []
                tree = ast.parse(code)
                
                # Check module docstring
                if not ast.get_docstring(tree):
                    doc_issues.append("Missing module docstring")
                
                # Check function and class docstrings
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if not ast.get_docstring(node):
                            doc_issues.append(f"Missing docstring in {node.__class__.__name__} {node.name}")
                
                doc_results["docstrings"] = doc_issues if doc_issues else "All required docstrings present"
            
            # Check comments
            if doc_type in ["comments", "all"]:
                comment_lines = [line.strip() for line in code.split('\n') 
                               if line.strip().startswith('#')]
                doc_results["comments"] = {
                    "total_comments": len(comment_lines),
                    "comment_lines": comment_lines
                }
            
            # Check README if applicable
            if doc_type in ["readme", "all"] and filename.lower() == "readme.md":
                readme_issues = []
                required_sections = ["Installation", "Usage", "Examples"]
                content_lower = code.lower()
                
                for section in required_sections:
                    if section.lower() not in content_lower:
                        readme_issues.append(f"Missing {section} section")
                
                doc_results["readme"] = readme_issues if readme_issues else "All required sections present"
            
            return {
                "success": True,
                "documentation": doc_results,
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}