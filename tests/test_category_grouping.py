from src.category_grouping import group_by_category

def test_group_by_category_returns_grouped_transactions():
    monthly_data = {
        "January 2025": [
            {"date": "2025-01-01", "amount": 3200.00, "category": "deposit", "service": "Income"},
            {"date": "2025-01-01", "amount": -1200.00, "category": "withdrawal", "service": "Bills"},
            {"date": "2025-01-02", "amount": -15.99, "category": "withdrawal", "service": "Services"},
            {"date": "2025-01-08", "amount": -12.50, "category": "withdrawal", "service": "Food"},
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
    assert bills_tx["amount"] == -1200.00
    assert bills_tx["category"] == "withdrawal"


def test_group_by_category_counts_are_correct():
    monthly_data = {
        "January 2025": [
            {"category": "deposit", "service": "Income"},
            {"category": "withdrawal", "service": "Bills"},
            {"category": "withdrawal", "service": "Services"},
            {"category": "withdrawal", "service": "Bills"},
            {"category": "withdrawal", "service": "Food"},
            {"category": "withdrawal", "service": "Memberships"},
            {"category": "withdrawal", "service": "Services"},
            {"category": "withdrawal", "service": "Food"},
            {"category": "withdrawal", "service": "Bills"},
            {"category": "withdrawal", "service": "Food"},
            {"category": "withdrawal", "service": "Miscellaneous"},
            {"category": "withdrawal", "service": "Food"},
        ]
    }

    result = group_by_category(monthly_data)

    assert len(result["Food"]) == 4
    assert len(result["Bills"]) == 3
    assert len(result["Services"]) == 2
    assert len(result["Memberships"]) == 1
    assert len(result["Miscellaneous"]) == 1
