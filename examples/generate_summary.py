"""Generate a 2x4 summary image of key BOJ data categories.

Usage:
    uv run python examples/generate_summary.py

Saves to docs/assets/summary.png for use in README.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pyboj import (
    BOJ,
    BopAccount,
    Currency,
    Database,
    Frequency,
    IndexType,
    Lang,
    MonetaryComponent,
    RateCategory,
)
from pyboj._domains.tankan import Tankan

# ── Fetch data ────────────────────────────────────────────────────────


def _try(label, fn):
    """Run *fn* and return its result, or None on error."""
    try:
        return fn()
    except Exception as e:
        print(f"  Warning: {label} failed: {e}")
        return None


def fetch_all():
    """Fetch one representative series per category."""
    boj = BOJ(lang=Lang.EN)
    data = {}

    # 1. Exchange rates — USD/JPY daily
    rates = _try("exchange_rates", lambda: boj.exchange_rates(
        currency=Currency.USD_JPY, frequency=Frequency.D, start_date="202301"
    ))
    if rates:
        data["USD/JPY"] = rates[0].to_dataframe()

    # 2. Interest rates — call rate daily
    ir = _try("interest_rates", lambda: boj.interest_rates(
        category=RateCategory.CALL_RATE, frequency=Frequency.D, start_date="202301"
    ))
    if ir:
        data["Call Rate"] = ir[0].to_dataframe()

    # 3. Tankan — manufacturing large DI (use specific known code)
    tankan_di = _try("tankan", lambda: [
        Tankan(sr)
        for sr in boj._client.iter_data_code(
            db="CO", code="TK99F1000601GCQ01000", start_date="201001"
        )
    ])
    if tankan_di:
        data["Tankan DI"] = tankan_di[0].to_dataframe()

    # 4. Price index — producer
    indices = _try("price_indices", lambda: boj.price_indices(
        index_type=IndexType.PRODUCER, start_date="201501"
    ))
    if indices:
        data["Producer Price Index"] = indices[0].to_dataframe()

    # 5. Balance of payments — current account
    bop = _try("balance_of_payments", lambda: boj.balance_of_payments(
        account=BopAccount.CURRENT, frequency=Frequency.M, start_date="201501"
    ))
    if bop:
        data["Current Account"] = bop[0].to_dataframe()

    # 6. Monetary base
    money = _try("money_deposits", lambda: boj.money_deposits(
        component=MonetaryComponent.TOTAL,
        db=Database.MONETARY_BASE,
        start_date="200001",
    ))
    if money:
        data["Monetary Base"] = money[0].to_dataframe()

    # 7. Loans — manufacturing (use specific known code)
    from pyboj._domains.loan import Loan

    loan_series = _try("loans", lambda: [
        Loan(sr)
        for sr in boj._client.iter_data_code(
            db="LA01", code="DLLILKG21_DLLI5DO1TMK", start_date="201501"
        )
    ])
    if loan_series:
        data["Loans (Manufacturing)"] = loan_series[0].to_dataframe()

    # 8. Flow of funds — households (use specific known code)
    from pyboj._domains.flow_of_funds import FlowOfFunds

    fof_series = _try("flow_of_funds", lambda: [
        FlowOfFunds(sr)
        for sr in boj._client.iter_data_code(
            db="FF", code="FOF_FFAR430A100", start_date="200001"
        )
    ])
    if fof_series:
        data["Household Assets"] = fof_series[0].to_dataframe()

    boj.close()
    return data


# ── Plot ──────────────────────────────────────────────────────────────

ZERO_LINE = {"Tankan DI", "Current Account"}


def make_summary(data: dict, output: str = "docs/assets/summary.png"):
    """Create a 2x4 subplot grid and save."""
    fig, axes = plt.subplots(2, 4, figsize=(16, 6))
    fig.suptitle("pyboj — Bank of Japan Time-Series Data", fontsize=14, fontweight="bold", y=0.98)

    for ax, (title, df) in zip(axes.flat, data.items(), strict=False):
        ax.plot(df.index, df["value"], linewidth=1.2, color="#1f77b4")
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.tick_params(axis="both", labelsize=7)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        if title in ZERO_LINE:
            ax.axhline(y=0, color="black", linewidth=0.6, linestyle="--")
        # Rotate x labels
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_ha("right")

    # Hide unused axes
    for ax in axes.flat[len(data):]:
        ax.set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {output}")


if __name__ == "__main__":
    print("Fetching data from BOJ API...")
    data = fetch_all()
    print(f"Got {len(data)} series. Generating summary image...")
    make_summary(data)
