"""
# Finance Plugin Tests

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/test_finance.py #domain/finance #domain/testing/unit #layer/test

## Purpose
Unit tests for the finance plugin operations including compound interest,
present/future value, loan payments, NPV, and IRR calculations.

## Related Documentation
- Pattern: [[obsidian/testing-strategy.md|Testing Strategy]]
- Implementation: [[code/plugins/finance.py|Finance Plugin]]

## Test Coverage
Tests all financial functions: compound_interest, present_value, future_value,
loan_payment, npv, irr
"""
import unittest
import math
from plugins import finance


class TestCompoundInterest(unittest.TestCase):  # ^TestCompoundInterest
    """
    Tests for the compound interest function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_compound_interest_annual(self):  # ^TestCompoundInterest-test_compound_interest_annual
        """Test compound interest with annual compounding."""
        # $1000 at 5% for 10 years, compounded annually
        result = finance.compound_interest(1000, 0.05, 10, 1)
        self.assertAlmostEqual(result, 1628.89, places=2)

    def test_compound_interest_monthly(self):  # ^TestCompoundInterest-test_compound_interest_monthly
        """Test compound interest with monthly compounding."""
        # $1000 at 5% for 10 years, compounded monthly
        result = finance.compound_interest(1000, 0.05, 10, 12)
        self.assertAlmostEqual(result, 1647.01, places=2)

    def test_compound_interest_continuous(self):  # ^TestCompoundInterest-test_compound_interest_continuous
        """Test compound interest with very high compounding frequency."""
        # $1000 at 5% for 10 years, compounded daily (approximates continuous)
        result = finance.compound_interest(1000, 0.05, 10, 365)
        self.assertAlmostEqual(result, 1648.66, places=2)

    def test_compound_interest_zero_rate(self):  # ^TestCompoundInterest-test_compound_interest_zero_rate
        """Test compound interest with zero interest rate."""
        result = finance.compound_interest(1000, 0, 10, 1)
        self.assertEqual(result, 1000)

    def test_compound_interest_negative_principal(self):  # ^TestCompoundInterest-test_compound_interest_negative_principal
        """Test compound interest raises error on negative principal."""
        with self.assertRaises(ValueError):
            finance.compound_interest(-1000, 0.05, 10, 1)

    def test_compound_interest_negative_rate(self):  # ^TestCompoundInterest-test_compound_interest_negative_rate
        """Test compound interest raises error on negative rate."""
        with self.assertRaises(ValueError):
            finance.compound_interest(1000, -0.05, 10, 1)

    def test_compound_interest_negative_time(self):  # ^TestCompoundInterest-test_compound_interest_negative_time
        """Test compound interest raises error on negative time."""
        with self.assertRaises(ValueError):
            finance.compound_interest(1000, 0.05, -10, 1)

    def test_compound_interest_zero_frequency(self):  # ^TestCompoundInterest-test_compound_interest_zero_frequency
        """Test compound interest raises error on zero compounding frequency."""
        with self.assertRaises(ValueError):
            finance.compound_interest(1000, 0.05, 10, 0)


class TestPresentValue(unittest.TestCase):  # ^TestPresentValue
    """
    Tests for the present value function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_present_value_basic(self):  # ^TestPresentValue-test_present_value_basic
        """Test basic present value calculation."""
        # $1000 in 5 years at 5% discount rate
        result = finance.present_value(1000, 0.05, 5)
        self.assertAlmostEqual(result, 783.53, places=2)

    def test_present_value_zero_rate(self):  # ^TestPresentValue-test_present_value_zero_rate
        """Test present value with zero discount rate."""
        result = finance.present_value(1000, 0, 5)
        self.assertEqual(result, 1000)

    def test_present_value_high_rate(self):  # ^TestPresentValue-test_present_value_high_rate
        """Test present value with high discount rate."""
        # $1000 in 10 years at 20% discount rate
        result = finance.present_value(1000, 0.20, 10)
        self.assertAlmostEqual(result, 161.51, places=2)

    def test_present_value_negative_rate(self):  # ^TestPresentValue-test_present_value_negative_rate
        """Test present value raises error on negative rate."""
        with self.assertRaises(ValueError):
            finance.present_value(1000, -0.05, 5)

    def test_present_value_negative_periods(self):  # ^TestPresentValue-test_present_value_negative_periods
        """Test present value raises error on negative periods."""
        with self.assertRaises(ValueError):
            finance.present_value(1000, 0.05, -5)


class TestFutureValue(unittest.TestCase):  # ^TestFutureValue
    """
    Tests for the future value function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_future_value_basic(self):  # ^TestFutureValue-test_future_value_basic
        """Test basic future value calculation."""
        # $1000 invested for 5 years at 5%
        result = finance.future_value(1000, 0.05, 5)
        self.assertAlmostEqual(result, 1276.28, places=2)

    def test_future_value_zero_rate(self):  # ^TestFutureValue-test_future_value_zero_rate
        """Test future value with zero interest rate."""
        result = finance.future_value(1000, 0, 5)
        self.assertEqual(result, 1000)

    def test_future_value_inverse_of_present_value(self):  # ^TestFutureValue-test_future_value_inverse_of_present_value
        """Test that future value and present value are inverses."""
        pv = 1000
        rate = 0.05
        periods = 5
        fv = finance.future_value(pv, rate, periods)
        pv_back = finance.present_value(fv, rate, periods)
        self.assertAlmostEqual(pv, pv_back, places=2)

    def test_future_value_negative_rate(self):  # ^TestFutureValue-test_future_value_negative_rate
        """Test future value raises error on negative rate."""
        with self.assertRaises(ValueError):
            finance.future_value(1000, -0.05, 5)

    def test_future_value_negative_periods(self):  # ^TestFutureValue-test_future_value_negative_periods
        """Test future value raises error on negative periods."""
        with self.assertRaises(ValueError):
            finance.future_value(1000, 0.05, -5)


class TestLoanPayment(unittest.TestCase):  # ^TestLoanPayment
    """
    Tests for the loan payment function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_loan_payment_basic(self):  # ^TestLoanPayment-test_loan_payment_basic
        """Test basic loan payment calculation."""
        # $10,000 loan at 5% annual for 5 years (60 monthly payments at 5%/12)
        result = finance.loan_payment(10000, 0.05/12, 60)
        self.assertAlmostEqual(result, 188.71, places=2)

    def test_loan_payment_zero_interest(self):  # ^TestLoanPayment-test_loan_payment_zero_interest
        """Test loan payment with zero interest (simple division)."""
        result = finance.loan_payment(10000, 0, 60)
        self.assertAlmostEqual(result, 166.67, places=2)

    def test_loan_payment_high_interest(self):  # ^TestLoanPayment-test_loan_payment_high_interest
        """Test loan payment with high interest rate."""
        # $10,000 at 20% annual for 5 years (60 monthly payments at 20%/12)
        result = finance.loan_payment(10000, 0.20/12, 60)
        self.assertAlmostEqual(result, 264.94, places=2)

    def test_loan_payment_short_term(self):  # ^TestLoanPayment-test_loan_payment_short_term
        """Test loan payment for short-term loan."""
        # $1,000 loan at 12% annual for 12 months
        result = finance.loan_payment(1000, 0.12/12, 12)
        self.assertAlmostEqual(result, 88.85, places=2)

    def test_loan_payment_negative_principal(self):  # ^TestLoanPayment-test_loan_payment_negative_principal
        """Test loan payment raises error on negative principal."""
        with self.assertRaises(ValueError):
            finance.loan_payment(-10000, 0.05, 60)

    def test_loan_payment_negative_rate(self):  # ^TestLoanPayment-test_loan_payment_negative_rate
        """Test loan payment raises error on negative rate."""
        with self.assertRaises(ValueError):
            finance.loan_payment(10000, -0.05, 60)

    def test_loan_payment_zero_periods(self):  # ^TestLoanPayment-test_loan_payment_zero_periods
        """Test loan payment raises error on zero periods."""
        with self.assertRaises(ValueError):
            finance.loan_payment(10000, 0.05, 0)


class TestNPV(unittest.TestCase):  # ^TestNPV
    """
    Tests for the Net Present Value function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_npv_basic(self):  # ^TestNPV-test_npv_basic
        """Test basic NPV calculation."""
        # Initial investment of -1000, then 300 per year for 5 years at 10%
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        result = finance.npv(0.10, cash_flows)
        self.assertAlmostEqual(result, 137.24, places=2)

    def test_npv_positive(self):  # ^TestNPV-test_npv_positive
        """Test NPV with profitable investment."""
        cash_flows = [-1000, 500, 500, 500]
        result = finance.npv(0.05, cash_flows)
        self.assertGreater(result, 0)  # Should be profitable

    def test_npv_negative(self):  # ^TestNPV-test_npv_negative
        """Test NPV with unprofitable investment."""
        cash_flows = [-1000, 100, 100, 100]
        result = finance.npv(0.10, cash_flows)
        self.assertLess(result, 0)  # Should be unprofitable

    def test_npv_zero_rate(self):  # ^TestNPV-test_npv_zero_rate
        """Test NPV with zero discount rate (simple sum)."""
        cash_flows = [-1000, 300, 400, 500]
        result = finance.npv(0, cash_flows)
        self.assertEqual(result, 200)  # -1000 + 300 + 400 + 500

    def test_npv_single_cash_flow(self):  # ^TestNPV-test_npv_single_cash_flow
        """Test NPV with single cash flow."""
        result = finance.npv(0.10, [-1000])
        self.assertEqual(result, -1000)

    def test_npv_empty_list(self):  # ^TestNPV-test_npv_empty_list
        """Test NPV raises error on empty cash flows."""
        with self.assertRaises(ValueError):
            finance.npv(0.10, [])


class TestIRR(unittest.TestCase):  # ^TestIRR
    """
    Tests for the Internal Rate of Return function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_irr_basic(self):  # ^TestIRR-test_irr_basic
        """Test basic IRR calculation."""
        # Investment of -1000, then 300 per year for 5 years
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        result = finance.irr(cash_flows)
        # IRR should be around 15.24%
        self.assertAlmostEqual(result, 0.1524, places=3)

    def test_irr_simple_doubling(self):  # ^TestIRR-test_irr_simple_doubling
        """Test IRR for investment that doubles in one period."""
        # Invest 100, get back 200 (100% return)
        cash_flows = [-100, 200]
        result = finance.irr(cash_flows)
        self.assertAlmostEqual(result, 1.0, places=3)

    def test_irr_break_even(self):  # ^TestIRR-test_irr_break_even
        """Test IRR for break-even investment."""
        # Invest 100, get back 100 (0% return)
        cash_flows = [-100, 100]
        result = finance.irr(cash_flows)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_irr_validates_at_npv_zero(self):  # ^TestIRR-test_irr_validates_at_npv_zero
        """Test that IRR produces NPV of zero."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr_rate = finance.irr(cash_flows)
        npv_at_irr = finance.npv(irr_rate, cash_flows)
        self.assertAlmostEqual(npv_at_irr, 0.0, places=4)

    def test_irr_different_guess(self):  # ^TestIRR-test_irr_different_guess
        """Test IRR with different initial guess."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        result1 = finance.irr(cash_flows, guess=0.1)
        result2 = finance.irr(cash_flows, guess=0.5)
        # Should converge to same answer regardless of guess
        self.assertAlmostEqual(result1, result2, places=4)

    def test_irr_empty_list(self):  # ^TestIRR-test_irr_empty_list
        """Test IRR raises error on empty cash flows."""
        with self.assertRaises(ValueError):
            finance.irr([])

    def test_irr_single_cash_flow(self):  # ^TestIRR-test_irr_single_cash_flow
        """Test IRR raises error on single cash flow."""
        with self.assertRaises(ValueError):
            finance.irr([-1000])

    def test_irr_no_convergence(self):  # ^TestIRR-test_irr_no_convergence
        """Test IRR raises error when it cannot converge."""
        # All positive cash flows - no meaningful IRR
        cash_flows = [100, 200, 300]
        with self.assertRaises(ValueError):
            finance.irr(cash_flows, max_iter=10)


if __name__ == '__main__':
    unittest.main()
