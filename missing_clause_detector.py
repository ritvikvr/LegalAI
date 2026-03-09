REQUIRED = {
    "Termination",
    "Confidentiality",
    "Indemnity",
    "Governing Law",
    "Limitation of Liability",
    "Dispute Resolution",
    "Force Majeure"
}

def detect_missing(classified):
    present = {c["type"] for c in classified}
    return list(REQUIRED - present)
