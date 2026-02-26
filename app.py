import streamlit as st # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore
from config import COLORS, PLOTLY_TEMPLATE # type: ignore
from translations import TEXTS # type: ignore
import statsmodels.api as sm # type: ignore
import base64

st.set_page_config(
    page_title="Sentiment Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- SESSION STATE & TRANSLATIONS -----------------
if 'lang' not in st.session_state:
    st.session_state.lang = 'ES'

def t(key):
    return TEXTS[st.session_state.lang].get(key, key)

# ----------------- CSS INJECTION -----------------
def inject_custom_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* App Background - elegant soft gradient */
    .stApp, [data-testid="stAppViewContainer"] {{
        background: {COLORS['bg_gradient']};
        font-family: 'Inter', sans-serif;
        background-attachment: fixed;
    }}
    
    /* Typography */
    html, body, [class*="css"] {{
        color: {COLORS['text_primary']} !important; 
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    /* Liquid Glass Containers for Metrics and general containers */
    [data-testid="stMetric"], .aurora-card, .css-1r6slb0, .css-12oz5g7 {{
        background: {COLORS['surface']} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07) !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
        box-sizing: border-box !important;
    }}
    
    [data-testid="stPlotlyChart"] {{
        background: {COLORS['surface']} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07) !important;
        padding: 0 !important; /* NO PADDING to avoid internal scrollbars */
        box-sizing: border-box !important;
        overflow: hidden !important;
    }}
    
    [data-testid="stPlotlyChart"] iframe {{
        max-width: 100% !important;
        max-height: 100% !important;
    }}
    
    [data-testid="stMetric"]:hover, .aurora-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 1) !important;
    }}
    
    /* Metric Typography */
    [data-testid="stMetricValue"] {{
        font-size: 2.0rem !important; 
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, {COLORS['primary']}, {COLORS['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.95rem !important;
        color: {COLORS['text_muted']} !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Tabs styling - Pill shape full width */
    .stTabs [data-baseweb="tab-list"] {{
        display: flex;
        gap: 10px;
        background: rgba(255, 255, 255, 0.4);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        width: 100%;
        justify-content: space-between;
    }}
    .stTabs [data-baseweb="tab"] {{
        flex: 1; 
        justify-content: center;
        height: 42px;
        background: rgba(226, 232, 240, 0.6); 
        border-radius: 12px;
        padding: 8px 12px;
        font-weight: 800 !important; 
        color: {COLORS['text_primary']} !important; 
        border: 1px solid rgba(203, 213, 225, 0.5) !important;
        transition: all 0.2s ease;
        white-space: nowrap;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(255, 255, 255, 1) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06) !important;
        color: {COLORS['primary']} !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}
    
    /* Welcome Storytelling elements */
    .welcome-card {{
        background: {COLORS['surface']};
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3.5rem;
        border: 1px solid rgba(255, 255, 255, 1);
        box-shadow: 0 15px 50px rgba(15, 23, 42, 0.06);
        margin-bottom: 2rem;
    }}
    .welcome-pillar {{
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 25px rgba(0,0,0,0.03);
        border-left: 5px solid {COLORS['primary']};
        transition: all 0.3s ease;
    }}
    .welcome-pillar * {{
        color: {COLORS['text_primary']} !important;
    }}
    .welcome-pillar:hover {{
        transform: translateX(8px);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 12px 30px rgba(0,0,0,0.05);
    }}
    .welcome-text {{
        font-size: 1.15rem;
        line-height: 1.8;
        color: {COLORS['text_muted']};
    }}
    
    .stButton>button {{
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid rgba(0,0,0,0.1);
        background: white;
        color: {COLORS['text_primary']};
    }}
    
    hr {{
        border-top: 1px solid rgba(15, 23, 42, 0.08);
        margin: 2.5rem 0;
    }}
    
    /* Hero Section */
    .hero-title {{
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, {COLORS['primary']}, {COLORS['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------- HEADER & LANGUAGE SELECTOR -----------------
def render_language_selector():
    col_logo, col_space, col_lang = st.columns([1, 6, 1])
    with col_lang:
        flag_urls = {
            "ES": "https://flagcdn.com/w20/ve.png",
            "EN": "https://flagcdn.com/w20/us.png",
            "BR": "https://flagcdn.com/w20/br.png"
        }
        
        active_lang = st.session_state.lang
        other_langs = [l for l in flag_urls.keys() if l != active_lang]
        
        # Iterate over the non-active languages and inject dynamic CSS for each specific position
        inner_css = ""
        for idx, lang_opt in enumerate(other_langs, start=1):
            inner_css += f"""
            div[data-testid="stPopoverBody"] div[data-testid="stElementContainer"]:nth-child({idx}) button p::before {{
                content: ""; display: inline-block; width: 18px; height: 13px;
                background-image: url('{flag_urls[lang_opt]}'); background-size: cover; 
                margin-right: 8px; vertical-align: middle; border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            """
            
        # CSS injection for natively unsupported images in Streamlit buttons
        css_flags = f"""
        <style>
        /* Main popover button flag */
        div[data-testid="stPopover"] > div > button p::before {{
            content: ""; display: inline-block; width: 18px; height: 13px;
            background-image: url('{flag_urls[active_lang]}'); background-size: cover; 
            margin-right: 8px; vertical-align: middle; border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        {inner_css}
        </style>
        """
        st.markdown(css_flags, unsafe_allow_html=True)
        
        with st.popover("🌐"):
            for lang_option in other_langs:
                if st.button(lang_option, use_container_width=True, key=f"btn_{lang_option}"):
                    st.session_state.lang = lang_option
                    st.rerun()

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_datasets():
    try:
        df_sent = pd.read_csv("output/sentiment_clean.csv")
        df_mkt = pd.read_csv("output/marketing_metrics.csv")
        df_topics = pd.read_csv("output/topic_keywords.csv")
        df_neg_topics = pd.read_csv("output/negative_topics_distribution.csv")
        
        # Parse dates
        df_sent['Date'] = pd.to_datetime(df_sent['Date'])
        df_mkt['Month'] = pd.to_datetime(df_mkt['Month'])
        
        return df_sent, df_mkt, df_topics, df_neg_topics
    except Exception as e:
        st.error(f"Error loading data: {e}. Make sure to run Steps 1 and 2.")
        return None, None, None, None

def main():
    inject_custom_css()
    
    render_language_selector()
    
    st.sidebar.title("🧠 " + t("app_title"))
    
    nav_selection = st.sidebar.radio("", [t("nav_intro"), t("nav_dashboard")])
    
    st.sidebar.markdown("---")
    
    df_sent, df_mkt, df_topics, df_neg_topics = load_datasets()
    
    if df_sent is None:
        return
        
    min_year = int(df_sent['Date'].dt.year.min()) # type: ignore
    max_year = int(df_sent['Date'].dt.year.max()) # type: ignore
    year_range = st.sidebar.slider(t("filter_year"), min_value=min_year, max_value=max_year, value=(min_year, max_year))
    
    sentiment_range = st.sidebar.slider(t("filter_sentiment"), -1.0, 1.0, (-1.0, 1.0))
    
    st.sidebar.markdown(f"<div style='margin-top: 50px; text-align: center; color: {COLORS['text_muted']}; font-weight: bold;'>{t('developed_by')}</div>", unsafe_allow_html=True)
    
    if nav_selection == t("nav_intro"):
        st.markdown(f"""
<div class="welcome-card" style="margin: 0; padding: 2.5rem;">
<h1 style="font-size: 3.2rem; margin-bottom: 0.8rem; text-align: center; color: {COLORS['text_primary']}; font-family: 'Inter', sans-serif;">{t("app_title")}</h1>
<p style="text-align: center; font-size: 1.3rem; color: {COLORS['text_muted']}; margin-bottom: 2.5rem; font-weight: 500; font-family: 'Inter', sans-serif;">
<em>{t("intro_p1")}</em>
</p>

<div class="welcome-pillar" style="font-family: 'Inter', sans-serif;">
<h4 style="margin-bottom: 0.5rem; color: {COLORS['text_primary']};">{t("intro_card1_title")}</h4>
<p style="margin:0; color: {COLORS['text_muted']};">{t("intro_card1_desc")}</p>
</div>
<div class="welcome-pillar" style="font-family: 'Inter', sans-serif;">
<h4 style="margin-bottom: 0.5rem; color: {COLORS['text_primary']};">{t("intro_card2_title")}</h4>
<p style="margin:0; color: {COLORS['text_muted']};">{t("intro_card2_desc")}</p>
</div>
<div class="welcome-pillar" style="font-family: 'Inter', sans-serif;">
<h4 style="margin-bottom: 0.5rem; color: {COLORS['text_primary']};">{t("intro_card3_title")}</h4>
<p style="margin:0; color: {COLORS['text_muted']};">{t("intro_card3_desc")}</p>
</div>

<div style="text-align: center; margin-top: 2rem; font-family: 'Inter', sans-serif;">
<p style="font-weight: 600; font-size: 1.2rem; color: {COLORS['primary']};">
{t("intro_p2")}
</p>
</div>
</div>
""", unsafe_allow_html=True)
        
    elif nav_selection == t("nav_dashboard"):
        
        st.title("📊 Dashboard")
        st.write("")
        
        # MAIN UI FILTERS
        st.markdown(f"<h4 style='color: {COLORS['text_primary']}; margin-bottom: 1rem;'>🎛️ Filtros Globales</h4>", unsafe_allow_html=True)
        filt_c1, filt_c2 = st.columns(2)
        
        channels = df_mkt['Canal'].unique().tolist() # type: ignore
        categories = df_sent['Category'].unique().tolist() # type: ignore
        
        with filt_c1:
            selected_categories = st.multiselect(t("filter_category"), categories, default=categories)
        with filt_c2:
            selected_channels = st.multiselect(t("filter_channel"), channels, default=channels)
        
        # APPLY FILTERS (Moved to Dashboard execution scope since variables live here now)
        f_sent = df_sent[ # type: ignore
            (df_sent['Date'].dt.year >= year_range[0]) &
            (df_sent['Date'].dt.year <= year_range[1]) &
            (df_sent['Category'].isin(selected_categories)) &
            (df_sent['Sentiment_Score'] >= sentiment_range[0]) &
            (df_sent['Sentiment_Score'] <= sentiment_range[1])
        ]
        
        f_mkt = df_mkt[ # type: ignore
            (df_mkt['Month'].dt.year >= year_range[0]) &
            (df_mkt['Month'].dt.year <= year_range[1]) &
            (df_mkt['Canal'].isin(selected_channels))
        ]
        
        # Sidebar download update
        csv = f_sent.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(label=t("download_btn"), data=csv, file_name='filtered_sentiment.csv', mime='text/csv')
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        avg_sent = float(f_sent['Sentiment_Score'].mean()) # type: ignore
        avg_roas = float(f_mkt['ROAS'].mean()) # type: ignore
        neg_pct = float((f_sent['Sentiment_Class'] == 'Negative').astype(float).mean() * 100) # type: ignore
        avg_cac = float(f_mkt['CAC'].mean()) # type: ignore
        
        with col1:
            st.metric(t("kpi_sentiment"), f"{avg_sent:.2f}")
        with col2:
            st.metric(t("kpi_roas"), f"{avg_roas:.2f}x")
        with col3:
            alert = "🚨" if neg_pct > 30 else ""
            st.metric(t("kpi_negative"), f"{neg_pct:.1f}% {alert}")
        with col4:
            st.metric(t("kpi_cac"), f"${avg_cac:.2f}")
            
        # TABS
        tab1, tab2, tab3, tab4 = st.tabs([t("tab_sentiment"), t("tab_marketing"), t("tab_correlation"), t("tab_conclusions")])
        
        # ---------- TAB 1: SENTIMENT ----------
        with tab1:
            t1c1, t1c2 = st.columns(2)
            
            with t1c1:
                # Donut Chart
                dist = f_sent['Sentiment_Class'].value_counts().reset_index()
                dist.columns = ['Sentiment', 'Count']
                fig1 = px.pie(dist, values='Count', names='Sentiment', hole=0.7, 
                              color='Sentiment', color_discrete_map={'Positive': COLORS['positive'], 'Neutral': COLORS['neutral'], 'Negative': COLORS['negative']})
                fig1.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart1_title"))
                st.plotly_chart(fig1, use_container_width=True)
                st.info(f"**{t('insight_label')}**: {t('insight1_pos') if avg_sent>0 else t('insight1_neg')}")
                
            with t1c2:
                # Line Chart Área Sombreada
                f_sent['Month'] = f_sent['Date'].dt.to_period('M').astype(str)
                time_sent = f_sent.groupby(['Month', 'Sentiment_Class']).size().unstack(fill_value=0).reset_index()
                fig2 = go.Figure()
                for col, color in zip(['Positive', 'Neutral', 'Negative'], [COLORS['positive'], COLORS['neutral'], COLORS['negative']]):
                    if col in time_sent.columns:
                        fig2.add_trace(go.Scatter(x=time_sent['Month'], y=time_sent[col], name=col,
                                                  fill='tozeroy', fillcolor=color.replace(')', ', 0.15)').replace('rgb', 'rgba'),
                                                  line=dict(color=color)))
                fig2.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart2_title"))
                st.plotly_chart(fig2, use_container_width=True)
            
            # Heatmap / Top Keywords
            t1c3, t1c4 = st.columns(2)
            with t1c3:
                # Bar Chart Horizontal Keywords - Usando DF preprocesado para evitar KeyError's de memoria
                if df_neg_topics is not None and len(df_neg_topics) > 0: # type: ignore
                    df_freq = df_neg_topics.sort_values(by='Count', ascending=True) # Sort for Plotly horizontal bar
                    fig3 = px.bar(df_freq, x='Count', y='Topic', orientation='h', 
                                  color_discrete_sequence=[COLORS['negative']])
                    fig3.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart3_title"))
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info(t("no_data_keywords"))
                
            with t1c4:
                # Heatmap Categoría vs Mes
                heat_data = f_sent.groupby(['Category', 'Month'])['Sentiment_Score'].mean().reset_index()
                fig4 = go.Figure(data=go.Heatmap(
                    z=heat_data['Sentiment_Score'],
                    x=heat_data['Month'],
                    y=heat_data['Category'],
                    colorscale=[[0, COLORS['negative']], [0.5, COLORS['neutral']], [1, COLORS['positive']]]
                ))
                fig4.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart4_title"))
                st.plotly_chart(fig4, use_container_width=True)
                
        # ---------- TAB 2: MARKETING ----------
        with tab2:
            t2c1, t2c2 = st.columns(2)
            
            with t2c1:
                roas_canal = f_mkt.groupby('Canal')['ROAS'].mean().reset_index()
                fig5 = px.bar(roas_canal, x='Canal', y='ROAS', color='Canal')
                fig5.add_hline(y=3.0, line_dash="solid", line_color=COLORS['secondary'], annotation_text=t('benchmark_label'))
                fig5.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart5_title"))
                st.plotly_chart(fig5, use_container_width=True)
                st.info(f"**{t('insight_label')}**: {t('insight2')}")

            with t2c2:
                fig6 = px.scatter(f_mkt, x='CAC', y='Conversiones', size='Inversion', color='Canal', hover_name='Month')
                fig6.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart6_title"))
                st.plotly_chart(fig6, use_container_width=True)
                
            fig7 = px.area(f_mkt, x='Month', y='Inversion', color='Canal', title=t("chart7_title"))
            rev_total = f_mkt.groupby('Month')['Revenue'].sum().reset_index()
            fig7.add_trace(go.Scatter(x=rev_total['Month'], y=rev_total['Revenue'], name=t('total_revenue'), line=dict(color=COLORS['primary'], width=3)))
            fig7.update_layout(PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig7, use_container_width=True)
            
            # Tabla de rendimiento
            perf_df = f_mkt.groupby('Canal').agg({'Inversion': 'sum', 'Revenue': 'sum', 'ROAS': 'mean', 'CAC': 'mean', 'CTR': 'mean'}).reset_index()
            st.dataframe(perf_df.style.background_gradient(cmap='Blues'), use_container_width=True)
            
            st.info(f"**{t('insight_label')}**: {t('tab2_insight')}")
            
        # ---------- TAB 3: CORRELATION ----------
        with tab3:
            
            # Scatter Plot Principal
            sent_monthly = f_sent.groupby('Month')['Sentiment_Score'].mean().reset_index()
            sent_monthly['Month'] = pd.to_datetime(sent_monthly['Month'])
            mkt_monthly = f_mkt.groupby('Month')['ROAS'].mean().reset_index()
            
            # Lag 1 month for S->ROI correlation
            sent_monthly['Lag_Month'] = sent_monthly['Month'] + pd.DateOffset(months=1)
            merged = pd.merge(sent_monthly, mkt_monthly, left_on='Lag_Month', right_on='Month', suffixes=('_sent', '_mkt'))
            
            if len(merged) > 2:
                fig8 = px.scatter(merged, x='Sentiment_Score', y='ROAS', trendline="ols")
                fig8.update_traces(marker=dict(size=12, color=COLORS['secondary']))
                fig8.update_layout(PLOTLY_TEMPLATE['layout'], title=t("chart8_title"))
                # Get R2
                results = px.get_trendline_results(fig8)
                r2 = results.iloc[0]["px_fit_results"].rsquared
                fig8.add_annotation(x=merged['Sentiment_Score'].mean(), y=merged['ROAS'].max(), text=f"R² = {r2:.2f} — {t('correlation_note')}", showarrow=False, font=dict(color=COLORS['primary']))
                st.plotly_chart(fig8, use_container_width=True)
                
                st.markdown(f"<div class='aurora-card' style='text-align: center; border-color: {COLORS['primary']}'><h3 style='color: {COLORS['primary']}'>{t('insight3')}</h3></div>", unsafe_allow_html=True)
                st.info(f"**{t('insight_label')}**: {t('tab3_insight')}")
            else:
                st.warning(t("no_data_correlation"))

        # ---------- TAB 4: CONCLUSIONS ----------
        with tab4:
            
            def create_insight(hallazgo, impacto, accion, prediccion):
                st.markdown(f"""
                <div style="margin-bottom: 2rem; padding: 1.5rem; border-left: 5px solid {COLORS['primary']}; background: {COLORS['surface_hover']}; border-radius: 0 8px 8px 0;">
                    <h4 style="margin-top: 0; color: {COLORS['text_primary']}; font-size: 1.1rem;">🔍 {t('finding')}: {hallazgo}</h4>
                    <p style="margin: 0.8rem 0; font-size: 1rem;"><strong>💥 {t('impact')}:</strong> {impacto}</p>
                    <p style="margin: 0.8rem 0; font-size: 1rem;"><strong>✅ {t('action')}:</strong> {accion}</p>
                    <div style="margin-top: 1rem; padding: 0.8rem; background: {COLORS['primary_soft']}; border-radius: 6px;">
                        <span style="color: {COLORS['primary']}; font-weight: bold;">📈 {t('prediction')}:</span> 
                        <span style="color: {COLORS['text_primary']};">{prediccion}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            create_insight(
                t("c1_finding"),
                t("c1_impact"),
                t("c1_action"),
                t("c1_prediction")
            )
            create_insight(
                t("c2_finding"),
                t("c2_impact"),
                t("c2_action"),
                t("c2_prediction")
            )
            create_insight(
                t("c3_finding"),
                t("c3_impact"),
                t("c3_action"),
                t("c3_prediction")
            )
            create_insight(
                t("c4_finding"),
                t("c4_impact"),
                t("c4_action"),
                t("c4_prediction")
            )
            
            st.markdown(f"<p style='margin-top: 2rem; font-style: italic; color: {COLORS['text_muted']}; font-size: 0.85rem;'>{t('methodology_note')}: {t('conclusions_intro')}</p>", unsafe_allow_html=True)
            
            footer_labels = {
                "ES": "Desarrollado por Hely Camargo utilizando:",
                "EN": "Developed by Hely Camargo using:",
                "BR": "Desenvolvido por Hely Camargo utilizando:"
            }
            f_text = footer_labels.get(st.session_state.lang, footer_labels["ES"])
            techs = "Python, Streamlit, Plotly, Pandas, Scikit-Learn, NLTK, SpaCy"
            
            st.markdown(f"""
            <div style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid {COLORS['border']}; text-align: right;">
                <p style="color: {COLORS['text_primary']}; font-size: 0.9rem; font-weight: bold;">
                    {f_text} 
                    <span style="color: {COLORS['primary']};">{techs}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
