def is_title_safe(title: str) -> bool:
    """Evaluate whether a window title is safe for display (No high-risk privacy data)."""
    cleaned_title = (title or "").lower().strip()
    
    # Strictly high-risk security/privacy items only
    sensitive_keywords = [
        "login", "signin", "sign-in", "signup", "sign-up",
        "register", "password", "auth", "credentials",
        "bank", "checkout", "pay", "stripe", "paypal", "wallet", "crypto",
        "gmail", "accounts.google", "facebook", "instagram"
    ]
    return not any(keyword in cleaned_title for keyword in sensitive_keywords)
