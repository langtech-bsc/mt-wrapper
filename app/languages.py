"""Map ISO / DeepL / Google language codes to the English names SalamandraTA expects.

SalamandraTA is prompted with language *names* ("Translate the following text
from Spanish into Catalan."), whereas Google Translate v2 and DeepL v2 clients
send codes ("es", "CA", "EN-GB"). Values that are not a known code are passed
through unchanged, so clients that already send names keep working.
"""
from typing import Optional

_NAMES = {
    "ar": "Arabic", "an": "Aragonese", "ast": "Asturian", "eu": "Basque",
    "bg": "Bulgarian", "ca": "Catalan", "zh": "Chinese", "hr": "Croatian",
    "cs": "Czech", "da": "Danish", "nl": "Dutch", "en": "English",
    "et": "Estonian", "fi": "Finnish", "fr": "French", "gl": "Galician",
    "de": "German", "el": "Greek", "hi": "Hindi", "hu": "Hungarian",
    "ga": "Irish", "it": "Italian", "ja": "Japanese", "ko": "Korean",
    "lv": "Latvian", "lt": "Lithuanian", "mt": "Maltese",
    "no": "Norwegian", "nb": "Norwegian Bokmål", "nn": "Norwegian Nynorsk",
    "oc": "Occitan", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian",
    "ru": "Russian", "sr": "Serbian", "sk": "Slovak", "sl": "Slovenian",
    "es": "Spanish", "sv": "Swedish", "uk": "Ukrainian", "cy": "Welsh",
}

# Regional / script variants (lower-case). Anything not listed falls back to
# the primary subtag, e.g. "en-gb" -> "English", "pt-br" -> "Portuguese".
_VARIANTS = {
    "ca-valencia": "Valencian", "ca-es-valencia": "Valencian",
    "oc-aranes": "Aranese", "oc-aran": "Aranese",
    "zh-hans": "Chinese", "zh-cn": "Chinese",
}


def language_name(value: Optional[str]) -> Optional[str]:
    """Return the English language name for a code; unknown values pass through."""
    if value is None:
        return None
    key = value.strip().lower().replace("_", "-")
    if key in _VARIANTS:
        return _VARIANTS[key]
    if key in _NAMES:
        return _NAMES[key]
    primary = key.split("-")[0]
    if primary in _NAMES and key != primary:
        return _NAMES[primary]
    return value.strip()
