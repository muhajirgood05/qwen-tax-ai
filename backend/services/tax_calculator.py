"""
Indonesian Income Tax (PPh 21) Calculator.
Based on UU HPP (UU No. 7/2021) and PP 58/2023.
"""


class TaxCalculator:
    """Calculator for Indonesian PPh 21 (Employee Income Tax)."""

    # PTKP values (Penghasilan Tidak Kena Pajak) - Annual
    PTKP = {
        "TK/0": 54_000_000,
        "TK/1": 58_500_000,
        "TK/2": 63_000_000,
        "TK/3": 67_500_000,
        "K/0": 58_500_000,
        "K/1": 63_000_000,
        "K/2": 67_500_000,
        "K/3": 72_000_000,
    }

    # Progressive tax brackets (UU HPP - Pasal 17)
    TAX_BRACKETS = [
        (60_000_000, 0.05),
        (250_000_000, 0.15),
        (500_000_000, 0.25),
        (5_000_000_000, 0.30),
        (float("inf"), 0.35),
    ]

    # Maximum biaya jabatan (5% of gross, max Rp 6 juta/tahun)
    MAX_BIAYA_JABATAN_ANNUAL = 6_000_000
    BIAYA_JABATAN_RATE = 0.05

    def calculate_pph21(
        self,
        gross_monthly_salary: float,
        status: str = "TK/0",
        bpjs_percentage: float = 0.01,
        other_deductions: float = 0.0,
    ) -> dict:
        """
        Calculate annual and monthly PPh 21.

        Args:
            gross_monthly_salary: Monthly gross salary in IDR
            status: PTKP status (TK/0, K/0, K/1, K/2, K/3, etc.)
            bpjs_percentage: BPJS employee contribution rate (default 1%)
            other_deductions: Other monthly deductions in IDR

        Returns:
            Dictionary with complete tax calculation breakdown
        """
        if status not in self.PTKP:
            raise ValueError(
                f"Invalid status '{status}'. "
                f"Valid options: {', '.join(self.PTKP.keys())}"
            )

        if gross_monthly_salary <= 0:
            raise ValueError("Gross monthly salary must be positive")

        # Annual calculations
        gross_annual = gross_monthly_salary * 12

        # Biaya Jabatan (5% of gross, max Rp 500.000/month or Rp 6.000.000/year)
        biaya_jabatan = min(
            gross_annual * self.BIAYA_JABATAN_RATE,
            self.MAX_BIAYA_JABATAN_ANNUAL,
        )

        # BPJS contribution (employee portion)
        bpjs_annual = gross_annual * bpjs_percentage

        # Other deductions
        other_deductions_annual = other_deductions * 12

        # Net annual income
        net_annual = gross_annual - biaya_jabatan - bpjs_annual - other_deductions_annual

        # PTKP
        ptkp = self.PTKP[status]

        # PKP (Penghasilan Kena Pajak)
        pkp = max(0, net_annual - ptkp)

        # Calculate progressive tax
        pph21_annual, breakdown = self._calculate_progressive_tax(pkp)

        # Monthly PPh 21
        pph21_monthly = pph21_annual / 12

        # Effective tax rate
        effective_rate = (pph21_annual / gross_annual * 100) if gross_annual > 0 else 0

        return {
            "gross_annual": gross_annual,
            "biaya_jabatan": biaya_jabatan,
            "bpjs_annual": bpjs_annual,
            "other_deductions_annual": other_deductions_annual,
            "net_annual": net_annual,
            "ptkp": ptkp,
            "pkp": pkp,
            "pph21_annual": pph21_annual,
            "pph21_monthly": round(pph21_monthly, 0),
            "effective_rate": round(effective_rate, 2),
            "breakdown": breakdown,
        }

    def _calculate_progressive_tax(self, pkp: float) -> tuple[float, list[dict]]:
        """
        Calculate tax using progressive brackets.

        Returns:
            Tuple of (total_tax, breakdown_list)
        """
        if pkp <= 0:
            return 0, []

        total_tax = 0
        remaining = pkp
        breakdown = []
        prev_limit = 0

        for limit, rate in self.TAX_BRACKETS:
            if remaining <= 0:
                break

            bracket_size = limit - prev_limit
            taxable_in_bracket = min(remaining, bracket_size)
            tax_in_bracket = taxable_in_bracket * rate

            breakdown.append({
                "bracket": f"Rp {prev_limit:,.0f} - Rp {limit:,.0f}",
                "rate": f"{rate * 100:.0f}%",
                "taxable_amount": taxable_in_bracket,
                "tax": tax_in_bracket,
            })

            total_tax += tax_in_bracket
            remaining -= taxable_in_bracket
            prev_limit = limit

        return total_tax, breakdown
