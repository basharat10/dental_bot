FAQ_DATA = {
    "location": "We are located at 123 Smile Avenue, Dental City. You can find us right next to the Central Park.",
    "hours": "Our clinic is open Monday to Friday from 9:00 AM to 6:00 PM, and Saturday from 10:00 AM to 2:00 PM.",
    "emergency": "For dental emergencies after hours, please call our emergency hotline at (555) 000-9999.",
    "services": "We offer a wide range of services including Cleanings, Fillings, Whitening, Root Canals, and Orthodontics.",
    "parking": "Yes, we have free parking available for all our patients directly in front of the clinic."
}

def get_faq_answer(user_text):
    """
    Checks if the user's text matches any FAQ keywords.
    Returns the answer if found, otherwise None.
    """
    text = user_text.lower()
    
    if any(word in text for word in ["location", "address", "where are you", "find you"]):
        return FAQ_DATA["location"]
    
    if any(word in text for word in ["hours", "open", "time", "closing"]):
        return FAQ_DATA["hours"]
    
    if any(word in text for word in ["emergency", "urgent", "pain", "after hours"]):
        return FAQ_DATA["emergency"]
    
    if any(word in text for word in ["services", "treatment", "cleaning", "whitening"]):
        return FAQ_DATA["services"]
    
    if any(word in text for word in ["parking", "park my car", "garage"]):
        return FAQ_DATA["parking"]
    
    return None
