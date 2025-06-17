translations = {
    "welcome": {
        "en": "Welcome to Real Estate Bot!",
        "ta": "ரியல் எஸ்டேட் போட்டுக்கு வரவேற்கிறோம்!",
        "te": "రియల్ ఎస్టేట్ బాట్కు స్వాగతం!",
        "kn": "ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಬಾಟ್ಗೆ ಸ್ವಾಗತ!",
        "ml": "റിയൽ എസ്റ്റേറ്റ് ബോട്ടിലേക്ക് സ്വാഗതം!"
    }
}

def get_translation(key, lang="en"):
    return translations.get(key, {}).get(lang, key)
