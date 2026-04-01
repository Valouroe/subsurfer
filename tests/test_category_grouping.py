import io
from src.category_grouping import sort_by_month, group_by_category

def test_category_case_insensitive():
    csv_data = """Date,Amount,Merchant Name,Service,Category
2025-01-01,-10,Netflix,Streaming,withdrawal
"""

    file = io.StringIO(csv_data)

    monthly = sort_by_month(file)
    result = group_by_category(monthly)

    assert "Streaming" in result


def test_missing_merchant_name():
    csv_data = """Date,Amount,Merchant Name,Service,Category
2025-01-01,-10,,Streaming,Withdrawal
"""

    file = io.StringIO(csv_data)

    monthly = sort_by_month(file)

    assert len(monthly) > 0


def test_missing_amount():
    monthly_data = {
        "January 2025": [
            {"Category": "Withdrawal", "Service": "Streaming"}
        ]
    }

    result = group_by_category(monthly_data)

    assert result == {}


def test_different_date_format():
    csv_data = """Date,Amount,Merchant Name,Service,Category
01/02/2025,-10,Netflix,Streaming,Withdrawal
"""

    file = io.StringIO(csv_data)

    monthly = sort_by_month(file)

    assert len(monthly) > 0

def test_group_by_category_returns_grouped_transactions():
    monthly_data = {
        "January 2025": [
            {"date": "2025-01-01", "Amount": 3200.00, "Category": "Deposit", "Service": "Income"},
            {"date": "2025-01-01", "Amount": -1200.00, "Category": "Withdrawal", "Service": "Bills"},
            {"date": "2025-01-02", "Amount": -15.99, "Category": "Withdrawal", "Service": "Services"},
            {"date": "2025-01-08", "Amount": -12.50, "Category": "Withdrawal", "Service": "Food"},
        ]
    }

    result = group_by_category(monthly_data)

    # Deposit should be ignored
    assert "Income" not in result

    # Expected withdrawal services
    assert "Bills" in result
    assert "Services" in result
    assert "Food" in result

    # Ensure full transaction data is preserved
    bills_tx = result["Bills"][0]
    assert bills_tx["Amount"] == 1200.00
    assert bills_tx["Category"] == "Withdrawal"


def test_group_by_category_counts_are_correct():
    monthly_data = {
        "January 2025": [
            {"Category": "Deposit", "Service": "Income", "Amount": 1000},
            {"Category": "Withdrawal", "Service": "Bills", "Amount": -50},
            {"Category": "Withdrawal", "Service": "Services", "Amount": -20},
            {"Category": "Withdrawal", "Service": "Bills", "Amount": -30},
            {"Category": "Withdrawal", "Service": "Food", "Amount": -10},
            {"Category": "Withdrawal", "Service": "Memberships", "Amount": -15},
            {"Category": "Withdrawal", "Service": "Services", "Amount": -25},
            {"Category": "Withdrawal", "Service": "Food", "Amount": -12},
            {"Category": "Withdrawal", "Service": "Bills", "Amount": -40},
            {"Category": "Withdrawal", "Service": "Food", "Amount": -8},
            {"Category": "Withdrawal", "Service": "Miscellaneous", "Amount": -60},
            {"Category": "Withdrawal", "Service": "Food", "Amount": -9},
        ]
    }

    result = group_by_category(monthly_data)

    assert len(result["Food"]) == 4
    assert len(result["Bills"]) == 3
    assert len(result["Services"]) == 2
    assert len(result["Memberships"]) == 1
    assert len(result["Miscellaneous"]) == 1
