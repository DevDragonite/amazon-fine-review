import pandas as pd
import numpy as np
import datetime

def log_qa(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("output/nlp_qa_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\\n")
    print(message)

def generate_marketing_data():
    log_qa("\\n--- PASO 2 QA: MARKETING DATA START ---")
    
    # Try to load sentiment to correlate with real generated dates
    try:
        sentiment_df = pd.read_csv("output/sentiment_clean.csv")
        sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])
        sentiment_df['Month'] = sentiment_df['Date'].dt.to_period('M')
        # Get monthly average sentiment
        monthly_sentiment = sentiment_df.groupby('Month')['Sentiment_Score'].mean().reset_index()
        monthly_sentiment = monthly_sentiment.sort_values('Month')
        
        # Take the last 24 months available in the dataset
        if len(monthly_sentiment) > 24:
            monthly_sentiment = monthly_sentiment.tail(24).copy()
        elif len(monthly_sentiment) < 24:
            # Pad with average if not enough months
            avg_sent = monthly_sentiment['Sentiment_Score'].mean()
            missing = 24 - len(monthly_sentiment)
            last_month = monthly_sentiment['Month'].max()
            new_months = pd.period_range(start=last_month + 1, periods=missing, freq='M')
            pad_df = pd.DataFrame({'Month': new_months, 'Sentiment_Score': [avg_sent]*missing})
            monthly_sentiment = pd.concat([monthly_sentiment, pad_df])
            
        months = monthly_sentiment['Month'].astype(str).tolist()
        sentiment_scores = monthly_sentiment['Sentiment_Score'].tolist()
        
    except Exception as e:
        log_qa(f"Error loading sentiment data: {e}. Generating 24 arbitrary months.")
        # Fallback if sentiment file doesn't exist
        today = datetime.datetime.today()
        months = [(today - pd.DateOffset(months=x)).strftime('%Y-%m') for x in range(24)]
        months.reverse()
        sentiment_scores = [np.random.normal(0.2, 0.1) for _ in range(24)]
        
    canales = ["Google Ads", "Facebook Ads", "Instagram", "Email"]
    
    # Base profiles for channels to make the data realistic
    # (Investment range, average CPC, average Conversion Rate, base ROAS)
    profiles = {
        "Google Ads":   {"inv": (10000, 20000), "cpc": 1.2, "cvr": 0.05, "base_roas": 3.5},
        "Facebook Ads": {"inv": (15000, 30000), "cpc": 0.8, "cvr": 0.03, "base_roas": 1.8}, # Prompt said FB had lowest ROAS (1.8x)
        "Instagram":    {"inv": (8000, 15000),  "cpc": 1.0, "cvr": 0.04, "base_roas": 2.5},
        "Email":        {"inv": (2000, 5000),   "cpc": 0.2, "cvr": 0.10, "base_roas": 6.0}  # Prompt said Email has lowest CAC
    }
    
    all_data = []
    
    for i, month in enumerate(months):
        # Current month sentiment
        actual_sentiment = sentiment_scores[i]
        
        # Previous month sentiment (for lag effect)
        prev_sentiment = sentiment_scores[i-1] if i > 0 else sentiment_scores[i]
        
        # Calculate sentiment delta
        sentiment_baseline = 0.2 # assume 0.2 is average base sentiment
        sentiment_delta = prev_sentiment - sentiment_baseline
        
        # "cuando el sentimiento promedio mensual sube, el ROAS del mes siguiente mejora 15-25%"
        # Let's say a 0.1 increase in sentiment leads to a ~8% increase in ROAS
        roas_multiplier = 1.0 + (sentiment_delta * 0.8) 
        
        for canal in canales:
            prof = profiles[canal]
            
            # Base logic
            inversion = np.random.uniform(prof["inv"][0], prof["inv"][1])
            
            # Add some randomness (gaussiano)
            noise = np.random.normal(0, 0.1)
            
            canal_roas = prof["base_roas"] * roas_multiplier * (1 + noise)
            
            # Bound ROAS
            canal_roas = max(1.0, min(canal_roas, 8.0))
            
            revenue = inversion * canal_roas
            
            # Clics y conversiones
            cpc_variation = np.random.normal(0, 0.1)
            actual_cpc = max(0.05, prof["cpc"] * (1 + cpc_variation))
            
            clics = int(inversion / actual_cpc)
            
            # Impresiones based on CTR (avg CTR 2-5%)
            ctr = np.random.uniform(0.015, 0.06)
            impresiones = int(clics / ctr)
            
            # Conversiones
            aov = 50.0 # Average Order Value
            conversiones = int(revenue / aov)
            
            # Recalculate exact Metrics
            ctr_real = clics / impresiones if impresiones > 0 else 0
            cac = inversion / conversiones if conversiones > 0 else 0
            
            all_data.append({
                "Month": month,
                "Canal": canal,
                "Inversion": round(inversion, 2),
                "Impresiones": impresiones,
                "Clics": clics,
                "Conversiones": conversiones,
                "Revenue": round(revenue, 2),
                "CAC": round(cac, 2),
                "ROAS": round(revenue / inversion, 2),
                "CTR": round(ctr_real, 4)
            })

    df = pd.DataFrame(all_data)
    df.to_csv("output/marketing_metrics.csv", index=False)
    log_qa(f"Generated {len(df)} marketing records.")
    
    # QA Checks
    qa_passed = True
    if (df['ROAS'] < 0.9).any() or (df['ROAS'] > 8.5).any():
        qa_passed = False
        log_qa("ERROR: ROAS out of bounds.")
    if (df['Inversion'] <= 0).any():
        qa_passed = False
        log_qa("ERROR: Negative or zero investment found.")
        
    if qa_passed:
        log_qa("--- PASO 2 QA: SUCCESS ---")
    else:
        log_qa("--- PASO 2 QA: FAILED ---")

if __name__ == "__main__":
    generate_marketing_data()
