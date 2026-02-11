def group_by_category(monthly_data):
    service_map = {}

    for month, transactions in monthly_data.items():
        for tx in transactions:
            if tx["category"] == "withdrawal":
                service = tx["service"]
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(tx)

    return service_map
