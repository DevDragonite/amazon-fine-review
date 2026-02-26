COLORS = {
    # Fondos (Teal a Slate muy claro para Light Mode)
    "bg_gradient": "linear-gradient(135deg, #f0fdfa 0%, #f8fafc 100%)",
    "surface": "rgba(255, 255, 255, 0.8)",
    "surface_hover": "rgba(255, 255, 255, 0.95)",

    # Acento principal — Teal (Serenidad)
    "primary": "#0d9488",
    "primary_soft": "rgba(13, 148, 136, 0.15)",

    # Acento secundario — Slate
    "secondary": "#475569",
    "secondary_soft": "rgba(71, 85, 105, 0.12)",

    # Acento terciario — Indigo pálido (para equilibrio)
    "accent": "#6366f1",
    "accent_soft": "rgba(99, 102, 241, 0.15)",

    # Semáforo analítico
    "positive": "#10b981", # Emerald
    "neutral": "#f59e0b",  # Amber
    "negative": "#ef4444", # Red

    # Texto
    "text_primary": "#0f172a", # Slate oscuro
    "text_muted": "#64748b",
    "text_accent": "#0d9488",

    # Bordes
    "border": "rgba(13, 148, 136, 0.2)",
    "border_strong": "rgba(13, 148, 136, 0.4)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#0f172a",
            "size": 12
        },
        "colorway": [
            "#0d9488", "#475569", "#6366f1",
            "#10b981", "#f59e0b", "#ef4444", "#38bdf8"
        ],
        "xaxis": {
            "gridcolor": "rgba(15, 23, 42, 0.05)",
            "linecolor": "rgba(15, 23, 42, 0.1)"
        },
        "yaxis": {
            "gridcolor": "rgba(15, 23, 42, 0.05)",
            "linecolor": "rgba(15, 23, 42, 0.1)"
        }
    }
}
