COLORS = {
    # Fondos (Deep Space / Midnight Blue for a soothing Dark/Soft Mode)
    "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
    "surface": "rgba(30, 41, 59, 0.7)", # Dark surface with blur
    "surface_hover": "rgba(30, 41, 59, 0.9)",

    # Acento principal — Teal (Serenidad, stands out on dark)
    "primary": "#2dd4bf", # Brighter teal for contrast
    "primary_soft": "rgba(45, 212, 191, 0.15)",

    # Acento secundario — Indigo
    "secondary": "#818cf8",
    "secondary_soft": "rgba(129, 140, 248, 0.12)",

    # Acento terciario — Slate Blue
    "accent": "#38bdf8",
    "accent_soft": "rgba(56, 189, 248, 0.15)",

    # Semáforo analítico
    "positive": "#34d399", # Emerald light
    "neutral": "#fbbf24",  # Amber light
    "negative": "#f87171", # Red light

    # Texto
    "text_primary": "#f8fafc", # Very light slate for readability
    "text_muted": "#cbd5e1",
    "text_accent": "#2dd4bf",

    # Bordes
    "border": "rgba(255, 255, 255, 0.1)",
    "border_strong": "rgba(255, 255, 255, 0.2)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#f8fafc",
            "size": 12
        },
        "colorway": [
            "#2dd4bf", "#818cf8", "#38bdf8",
            "#34d399", "#fbbf24", "#f87171", "#c084fc"
        ],
        "xaxis": {
            "gridcolor": "rgba(255, 255, 255, 0.05)",
            "linecolor": "rgba(255, 255, 255, 0.1)"
        },
        "yaxis": {
            "gridcolor": "rgba(255, 255, 255, 0.05)",
            "linecolor": "rgba(255, 255, 255, 0.1)"
        }
    }
}
