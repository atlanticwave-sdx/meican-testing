#!/usr/bin/env python3
"""
Comprehensive test runner for MEICAN SDX UI tests
Runs all test categories with proper reporting and environment setup
"""

import subprocess
import sys
import os
from datetime import datetime


def run_test_category(test_pattern, category_name):
    """Run a specific category of tests"""
    print(f"\n{'='*60}")
    print(f"RUNNING {category_name.upper()} TESTS")
    print(f"{'='*60}")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        f"tests/{test_pattern}",
        "-v", 
        "--tb=short",
        f"--html=reports/{category_name}_report.html",
        "--self-contained-html"
    ]
    
    env = os.environ.copy()
    env['PYTHONPATH'] = 'tests'
    
    try:
        result = subprocess.run(cmd, cwd=os.getcwd(), env=env, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {category_name} tests: {e}")
        return False


def main():
    """Main test execution function"""
    print("MEICAN SDX UI Test Suite")
    print(f"Test execution started at: {datetime.now()}")
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Define test categories
    test_categories = [
        ("test_*_admin_login.py", "admin_authentication"),
        ("test_8_orcid_login.py", "orcid_authentication"), 
        ("test_9_cilogon_login.py", "cilogon_authentication"),
        ("test_10_topology_visualization.py", "topology_visualization"),
        ("test_11_connection_management.py", "connection_management"),
        ("test_12_form_validation.py", "form_validation"),
        ("test_13_end_to_end_workflows.py", "end_to_end_workflows")
    ]
    
    results = {}
    
    # Run each test category
    for pattern, category in test_categories:
        success = run_test_category(pattern, category)
        results[category] = success
    
    # Generate summary report
    print(f"\n{'='*60}")
    print("TEST EXECUTION SUMMARY")
    print(f"{'='*60}")
    
    total_categories = len(results)
    passed_categories = sum(results.values())
    
    for category, success in results.items():
        status = "PASSED" if success else "FAILED/SKIPPED"
        print(f"{category:<30} {status}")
    
    print(f"\nOverall: {passed_categories}/{total_categories} test categories completed successfully")
    print(f"Test execution completed at: {datetime.now()}")
    
    # Generate combined HTML report
    print(f"\nDetailed reports available in:")
    for category in results.keys():
        print(f"  - reports/{category}_report.html")


if __name__ == "__main__":
    main()