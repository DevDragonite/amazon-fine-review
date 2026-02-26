COLORS = {
    # Fondos (Warm Pastel Gradient from the Almond to Mimi Pink)
    "bg_gradient": "linear-gradient(135deg, #dbd3c9 0%, #fad4d8 100%)",
    "surface": "rgba(255, 255, 255, 0.55)", # Translúcido mate
    "surface_hover": "rgba(255, 255, 255, 0.85)",

    # Acento principal (Slate Gray)
    "primary": "#546a76",
    "primary_soft": "rgba(84, 106, 118, 0.15)",

    # Acento secundario (Cadet Gray)
    "secondary": "#88a0a8",
    "secondary_soft": "rgba(136, 160, 168, 0.15)",

    # Acento terciario (Mimi Pink)
    "accent": "#fad4d8",
    "accent_soft": "rgba(250, 212, 216, 0.3)",

    # Semáforo analítico
    "positive": "#b4ceb3", # Spring Green
    "neutral": "#dbd3c9",  # Almond
    "negative": "#c05761", # Darker derivate of #fad4d8 para legibilidad en alertas rojas

    # Texto
    "text_primary": "#2d3a40", # Very dark Slate Gray for legibility
    "text_muted": "#546a76",
    "text_accent": "#546a76",

    # Bordes
    "border": "rgba(84, 106, 118, 0.2)",
    "border_strong": "rgba(84, 106, 118, 0.4)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#2d3a40",
            "size": 12
        },
        "colorway": [
            "#546a76", "#88a0a8", "#fad4d8",
            "#b4ceb3", "#dbd3c9", "#c05761"
        ],
        "xaxis": {
            "gridcolor": "rgba(84, 106, 118, 0.05)",
            "linecolor": "rgba(84, 106, 118, 0.1)"
        },
        "yaxis": {
            "gridcolor": "rgba(84, 106, 118, 0.05)",
            "linecolor": "rgba(84, 106, 118, 0.1)"
        }
    }
}
