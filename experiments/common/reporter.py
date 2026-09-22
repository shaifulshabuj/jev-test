"""
CLI Table and Report Formatter for Agentic Org Experiments.
"""

from typing import List, Dict, Any

class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def print_header(title: str, subtitle: str = ""):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {title}{Colors.END}")
    if subtitle:
        print(f"{Colors.BLUE}  {subtitle}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 75}{Colors.END}\n")

def print_threshold_verdict(label: str, passed: bool, details: str):
    icon = f"{Colors.GREEN}✓ PASSED [GO]{Colors.END}" if passed else f"{Colors.RED}✗ FAILED [NO-GO]{Colors.END}"
    print(f"  {icon} | {Colors.BOLD}{label:<30}{Colors.END}: {details}")

def print_meter(confidence: float, width: int = 15) -> str:
    filled = int(confidence * width)
    bar = "█" * filled + "░" * (width - filled)
    if confidence >= 0.85:
        return f"{Colors.GREEN}[{bar}] {confidence:.2f}{Colors.END}"
    elif confidence >= 0.50:
        return f"{Colors.YELLOW}[{bar}] {confidence:.2f}{Colors.END}"
    else:
        return f"{Colors.RED}[{bar}] {confidence:.2f}{Colors.END}"
