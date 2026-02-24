COLORS = {
    # Fondos
    "bg_gradient": "linear-gradient(135deg, #0f1729 0%, #1a2744 50%, #0d2137 100%)",
    "surface": "rgba(255, 255, 255, 0.06)",
    "surface_hover": "rgba(255, 255, 255, 0.10)",

    # Acento principal — Cian Aurora
    "primary": "#00d4ff",
    "primary_soft": "rgba(0, 212, 255, 0.15)",

    # Acento secundario — Verde esmeralda
    "secondary": "#00ffa3",
    "secondary_soft": "rgba(0, 255, 163, 0.12)",

    # Acento terciario — Violeta
    "accent": "#a855f7",
    "accent_soft": "rgba(168, 85, 247, 0.15)",

    # Semáforo analítico
    "positive": "#00ffa3",
    "neutral": "#f0b94a",
    "negative": "#ff6b6b",

    # Texto
    "text_primary": "#e8f4fd",
    "text_muted": "#8aa4c8",
    "text_accent": "#00d4ff",

    # Bordes
    "border": "rgba(0, 212, 255, 0.15)",
    "border_strong": "rgba(0, 212, 255, 0.35)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#e8f4fd",
            "size": 12
        },
        "colorway": [
            "#00d4ff", "#00ffa3", "#a855f7",
            "#f0b94a", "#ff6b6b", "#38bdf8", "#fb923c"
        ],
        "xaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": "rgba(255,255,255,0.1)"
        },
        "yaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": "rgba(255,255,255,0.1)"
        }
    }
}
