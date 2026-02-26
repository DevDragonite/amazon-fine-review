COLORS = {
    # Fondos (Luz muy suave, "Pearl/Cloud" no escandila)
    "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
    "surface": "rgba(255, 255, 255, 0.65)", # Translúcido mate
    "surface_hover": "rgba(255, 255, 255, 0.9)",

    # Acento principal — Teal calmo (bosque/eucalipto suave)
    "primary": "#0f766e",
    "primary_soft": "rgba(15, 118, 110, 0.1)",

    # Acento secundario — Slate (Pizarra)
    "secondary": "#475569",
    "secondary_soft": "rgba(71, 85, 105, 0.1)",

    # Acento terciario — Indigo apagado
    "accent": "#4f46e5",
    "accent_soft": "rgba(79, 70, 229, 0.1)",

    # Semáforo analítico (Tonos pastel mate legibles)
    "positive": "#059669", # Emerald suave
    "neutral": "#d97706",  # Amber oscuro
    "negative": "#dc2626", # Red oscuro

    # Texto
    "text_primary": "#1e293b", # Gris oscuro (nunca negro puro)
    "text_muted": "#64748b",
    "text_accent": "#0f766e",

    # Bordes
    "border": "rgba(148, 163, 184, 0.2)",
    "border_strong": "rgba(148, 163, 184, 0.4)",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#1e293b",
            "size": 12
        },
        "colorway": [
            "#0f766e", "#475569", "#4f46e5",
            "#059669", "#d97706", "#dc2626", "#8b5cf6"
        ],
        "xaxis": {
            "gridcolor": "rgba(30, 41, 59, 0.05)",
            "linecolor": "rgba(30, 41, 59, 0.1)"
        },
        "yaxis": {
            "gridcolor": "rgba(30, 41, 59, 0.05)",
            "linecolor": "rgba(30, 41, 59, 0.1)"
        }
    }
}
