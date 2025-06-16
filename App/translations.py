translations = {
    'welcome': {
        'en': "Welcome to Real Estate Bot, {name}!",
        'ta': "ரியல் எஸ்டேட் போட்டுக்கு வரவேற்கிறோம், {name}!",
        'te': "రియల్ ఎస్టేట్ బాట్కు స్వాగతం, {name}!",
        'kn': "ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಬಾಟ್ಗೆ ಸ್ವಾಗತ, {name}!",
        'ml': "റിയൽ എസ്റ്റേറ്റ് ബോട്ടിലേക്ക് സ്വാഗതം, {name}!",
    },
    'role_registered': {
        'en': "✅ You've been registered as a {role}!",
        'ta': "✅ நீங்கள் {role} ஆக பதிவு செய்யப்பட்டுள்ளீர்கள்!",
        'te': "✅ మీరు {role} గా నమోదు చేయబడ్డారు!",
        'kn': "✅ ನೀವು {role} ಆಗಿ ನೋಂದಾಯಿಸಲ್ಪಟ್ಟಿದ್ದೀರಿ!",
        'ml': "✅ നിങ്ങൾ {role} ആയി രജിസ്റ്റർ ചെയ്തു!",
    }
}

def get_translation(key, lang='en'):
    return translations.get(key, {}).get(lang, translations[key]['en'])
