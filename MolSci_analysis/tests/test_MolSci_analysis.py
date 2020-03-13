"""
Unit and regression test for the MolSci_analysis package.
"""

# Import package, test suite, and other packages as needed
import MolSci_analysis
import pytest
import sys

def test_MolSci_analysis_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "MolSci_analysis" in sys.modules
