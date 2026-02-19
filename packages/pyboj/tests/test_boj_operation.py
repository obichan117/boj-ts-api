"""Tests for the BOJ operation domain wrapper."""

from pyboj._domains.boj_operation import (
    OperationType,
    _detect_operation,
)


class TestDetectOperation:
    def test_govt_receipts(self):
        assert _detect_operation("Treasury Receipts") == OperationType.GOVT_RECEIPTS

    def test_govt_payments(self):
        assert _detect_operation("Treasury Payments") == OperationType.GOVT_PAYMENTS

    def test_jgb(self):
        assert _detect_operation("JGB Outright Purchase") == OperationType.JGB_OPERATIONS

    def test_govt_bond(self):
        assert _detect_operation("Government Bond Operations") == OperationType.JGB_OPERATIONS

    def test_lending(self):
        assert _detect_operation("Lending Facility") == OperationType.LENDING

    def test_repo(self):
        assert _detect_operation("Repo Operations") == OperationType.REPO_OPERATIONS

    def test_outright_purchase(self):
        assert _detect_operation("Outright Purchase of CP") == OperationType.OUTRIGHT_PURCHASE

    def test_collateral(self):
        assert _detect_operation("Collateral Value") == OperationType.COLLATERAL

    def test_total(self):
        assert _detect_operation("Total") == OperationType.TOTAL

    def test_other(self):
        assert _detect_operation("Unknown") == OperationType.OTHER
