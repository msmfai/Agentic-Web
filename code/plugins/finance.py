"""
# Finance Plugin

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/plugins/finance.py #domain/finance #domain/mathematics #layer/plugin-implementation #pattern/plugin-architecture #pattern/strategy/function-registry

## Purpose
Provides financial mathematics operations including compound interest,
present/future value calculations, and loan amortization.

## Related Documentation
- Pattern: [[obsidian/plugin-architecture.md|Plugin Architecture]]
- Concept: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]

## Plugin Interface
Exports PLUGIN_OPERATIONS dictionary for dynamic loading by the plugin system.

## Used By
- [[../plugin_system.py|Plugin System]]
"""
import math
from typing import List, Tuple


def compound_interest(principal: float, rate: float, time: float, n: float = 1) -> float:  # ^compound_interest
    """
    Calculate compound interest.

    Formula: A = P(1 + r/n)^(nt)

    Args:
        principal: Initial principal amount
        rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
        n: Number of times interest is compounded per year (default: 1)

    Returns:
        Final amount after compound interest

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if principal < 0:
        raise ValueError("Principal must be non-negative")
    if rate < 0:
        raise ValueError("Interest rate must be non-negative")
    if time < 0:
        raise ValueError("Time must be non-negative")
    if n <= 0:
        raise ValueError("Compounding frequency must be positive")

    return principal * math.pow((1 + rate / n), n * time)


def present_value(future_value: float, rate: float, periods: float) -> float:  # ^present_value
    """
    Calculate present value of a future amount.

    Formula: PV = FV / (1 + r)^n

    Args:
        future_value: Future value amount
        rate: Discount rate per period (as decimal)
        periods: Number of periods

    Returns:
        Present value

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if rate < 0:
        raise ValueError("Discount rate must be non-negative")
    if periods < 0:
        raise ValueError("Number of periods must be non-negative")

    return future_value / math.pow((1 + rate), periods)


def future_value(present_value_amt: float, rate: float, periods: float) -> float:  # ^future_value
    """
    Calculate future value of a present amount.

    Formula: FV = PV * (1 + r)^n

    Args:
        present_value_amt: Present value amount
        rate: Interest rate per period (as decimal)
        periods: Number of periods

    Returns:
        Future value

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if rate < 0:
        raise ValueError("Interest rate must be non-negative")
    if periods < 0:
        raise ValueError("Number of periods must be non-negative")

    return present_value_amt * math.pow((1 + rate), periods)


def loan_payment(principal: float, rate: float, periods: float) -> float:  # ^loan_payment
    """
    Calculate periodic payment for a loan (annuity).

    Formula: PMT = P * [r(1 + r)^n] / [(1 + r)^n - 1]

    Args:
        principal: Loan amount
        rate: Interest rate per period (as decimal)
        periods: Number of payment periods

    Returns:
        Payment amount per period

    Raises:
        ValueError: If rate is zero (use principal/periods instead)

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if principal < 0:
        raise ValueError("Principal must be non-negative")
    if rate < 0:
        raise ValueError("Interest rate must be non-negative")
    if periods <= 0:
        raise ValueError("Number of periods must be positive")

    if rate == 0:
        # No interest case
        return principal / periods

    numerator = rate * math.pow((1 + rate), periods)
    denominator = math.pow((1 + rate), periods) - 1

    return principal * (numerator / denominator)


def npv(rate: float, cash_flows: List[float]) -> float:  # ^npv
    """
    Calculate Net Present Value of a series of cash flows.

    Args:
        rate: Discount rate per period (as decimal)
        cash_flows: List of cash flows (first is at time 0)

    Returns:
        Net present value

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")

    npv_value = 0
    for i, cash_flow in enumerate(cash_flows):
        npv_value += cash_flow / math.pow((1 + rate), i)

    return npv_value


def irr(cash_flows: List[float], guess: float = 0.1, max_iter: int = 100, tolerance: float = 1e-6) -> float:  # ^irr
    """
    Calculate Internal Rate of Return using Newton-Raphson method.

    Args:
        cash_flows: List of cash flows (first is typically negative investment)
        guess: Initial guess for IRR (default: 0.1 or 10%)
        max_iter: Maximum iterations (default: 100)
        tolerance: Convergence tolerance (default: 1e-6)

    Returns:
        Internal rate of return

    Raises:
        ValueError: If IRR cannot be found

    Related: [[obsidian/arithmetic-operations.md|Arithmetic Operations]]
    """
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")
    if len(cash_flows) < 2:
        raise ValueError("IRR requires at least 2 cash flows")

    rate = guess

    for iteration in range(max_iter):
        # Calculate NPV and its derivative
        npv_val = 0
        npv_derivative = 0

        for i, cash_flow in enumerate(cash_flows):
            npv_val += cash_flow / math.pow((1 + rate), i)
            if i > 0:
                npv_derivative -= i * cash_flow / math.pow((1 + rate), i + 1)

        # Newton-Raphson step
        if abs(npv_derivative) < 1e-10:
            raise ValueError("IRR calculation failed: derivative too small")

        new_rate = rate - npv_val / npv_derivative

        # Check convergence
        if abs(new_rate - rate) < tolerance:
            return new_rate

        rate = new_rate

    raise ValueError(f"IRR did not converge after {max_iter} iterations")


# Plugin Operations Registry
# Exported for dynamic loading by the plugin system
PLUGIN_OPERATIONS = {  # ^PLUGIN_OPERATIONS
    'compound_interest': compound_interest,
    'present_value': present_value,
    'future_value': future_value,
    'loan_payment': loan_payment,
    'npv': npv,
    'irr': irr,
}
