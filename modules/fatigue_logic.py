def evaluate_fatigue(eye_closed, yawning, head_droop):
    score = 0

    # Assign weights
    if eye_closed:
        score += 2

    if yawning:
        score += 1

    if head_droop:
        score += 2

    # Decide fatigue level
    if score >= 4:
        return "CRITICAL", score
    elif score >= 2:
        return "WARNING", score
    else:
        return "NORMAL", score