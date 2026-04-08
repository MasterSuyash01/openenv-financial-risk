TASKS = {
    "easy": {
        "transaction": {
            "id": "tx100",
            "amount": 20,
            "country": "India",
            "history_flagged": 0,
            "pattern": "normal purchase"
        },
        "risk": "low",
        "correct_decision": "approve"
    },

    "medium": {
        "transaction": {
            "id": "tx200",
            "amount": 7000,
            "country": "Russia",
            "history_flagged": 1,
            "pattern": "unusual location"
        },
        "risk": "medium",
        "correct_decision": "flag"
    },

    "hard": {
        "transaction": {
            "id": "tx300",
            "amount": 25000,
            "country": "Unknown",
            "history_flagged": 3,
            "pattern": "rapid repeated transfers"
        },
        "risk": "high",
        "correct_decision": "escalate"
    }
}