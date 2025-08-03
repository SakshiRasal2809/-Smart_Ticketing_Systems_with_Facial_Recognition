from datetime import datetime

def calculate_fare(entry_time=None, exit_time=None, distance_km=5):
    """
    Calculate fare based on distance, peak hours, and minimum fare rule.

    Parameters:
        entry_time (str) : Entry timestamp in "%Y-%m-%d %H:%M:%S" format (optional)
        exit_time  (str) : Exit timestamp in "%Y-%m-%d %H:%M:%S" format (optional)
        distance_km (float) : Distance traveled in kilometers (default 5)

    Returns:
        float: Calculated fare
    """
    base_rate_per_km = 5  # Rs per km
    fare = distance_km * base_rate_per_km

    # If entry/exit time provided → check for peak hours
    if entry_time:
        try:
            entry_hour = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S").hour
        except:
            entry_hour = None
    else:
        entry_hour = datetime.now().hour

    # Peak hour surcharge: 7–10 AM and 5–8 PM → +20%
    if entry_hour and ((7 <= entry_hour <= 10) or (17 <= entry_hour <= 20)):
        fare *= 1.2

    # Minimum fare rule
    if fare < 10:
        fare = 10

    return round(fare, 2)
