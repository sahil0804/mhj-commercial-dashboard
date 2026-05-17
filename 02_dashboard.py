import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import datetime
import random
import re

# ==========================================
# 1. BRAND ARCHITECTURE & DESIGN SYSTEM
# ==========================================
st.set_page_config(page_title="MHJ | Brilliance AI & Performance Hub", page_icon="💍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp { background: linear-gradient(135deg, #0a0a0c 0%, #1a1a1f 100%); color: #F5F5F5; }
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    
    .block-container { padding-top: 1rem; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: #D4AF37 !important; text-shadow: 0px 2px 4px rgba(0,0,0,0.5); }
    p, span, div { color: #EAEAEA; }
    
    [data-testid="stSidebar"] {
        background: rgba(20, 20, 25, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(212, 175, 55, 0.15);
    }
    
    [data-testid="metric-container"] {
        background: rgba(30, 30, 35, 0.4);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 3px solid #D4AF37; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        background: rgba(40, 40, 45, 0.6);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.15); 
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 600; }
    [data-testid="stMetricLabel"] { color: #A0A0A0 !important; font-weight: 500; letter-spacing: 0.5px; text-transform: uppercase; font-size: 0.85rem;}
    
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif; font-weight: 500; color: #888888; background-color: transparent;}
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; background-color: rgba(212,175,55,0.05);}
    
    .stChatMessage { background: rgba(30, 30, 35, 0.4); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 10px; }
    .stSlider [data-baseweb="slider"] div { background-color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; padding-bottom: 10px;">
    <div style="background: linear-gradient(135deg, #D4AF37 0%, #AA8529 100%); width: 6px; height: 60px; margin-right: 20px; border-radius: 3px;"></div>
    <div>
        <h1 style='margin: 0px; padding: 0px; letter-spacing: 4px; font-size: 2.5rem; line-height: 1.1;'>MICHAEL HILL</h1>
        <p style='color: #A0A0A0; font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase; margin: 0px;'>Enterprise Telemetry & Machine Learning Hub <span style="color:#D4AF37;">● LIVE CLOUD</span></p>
    </div>
</div>
<hr style='border: 0; height: 1px; background-image: linear-gradient(to right, rgba(212, 175, 55, 0.5), rgba(255, 255, 255, 0)); margin-bottom: 30px;'>
""", unsafe_allow_html=True)

# ==========================================
# 2. BULLETPROOF DATA ENGINE
# ==========================================
@st.cache_data
def load_performance_data():
    file_path = "jewellery_retail_data.csv"
    try:
        # First, try to load the real file
        df = pd.read_csv(file_path)
    except Exception:
        # FALLBACK: If file is missing, generate synthetic data instantly
        np.random.seed(42)
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=90)
        dates = [start_date + datetime.timedelta(days=random.randint(0, 90)) for _ in range(800)]
        stores = ["Sydney CBD Flagship", "Melbourne Bourke St", "Brisbane Queen St", "Auckland Queen St"]
        categories = ["Lume LAB Bridal", "Everyday Silver", "Bespoke Luxury", "Watches", "Fine Gold"]

        data = {
            'TransactionID': range(1000, 1800),
            'Date': dates,
            'StoreLocation': np.random.choice(stores, 800),
            'ProductCategory': np.random.choice(categories, 800, p=[0.25, 0.35, 0.1, 0.15, 0.15]),
            'Quantity': np.random.randint(1, 4, 800),
            'UnitValue': np.random.uniform(90, 4500, 800),
            'DeliveryDelayDays': np.random.randint(0, 6, 800),
            'CustomerRating': np.random.uniform(3.5, 5.0, 800)
        }
        df = pd.DataFrame(data)
        df['TotalRevenue'] = df['Quantity'] * df['UnitValue']
        
        def get_sentiment(rating):
            if rating >= 4.5: return "Positive"
            elif rating >= 4.0: return "Neutral"
            else: return "Negative"
        df['SentimentLabel'] = df['CustomerRating'].apply(get_sentiment)

    # Process dates regardless of source
    df['Date'] = pd.to_datetime(df['Date'])
    df['MonthYear'] = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_performance_data()

# ==========================================
# 3. GOVERNANCE CONTROLS
# ==========================================
st.sidebar.markdown("<h3 style='color: #D4AF37; margin-top:0px;'>🎛️ Governance</h3>", unsafe_allow_html=True)

min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
date_selection = st.sidebar.slider("Trading Window", min_value=min_date, max_value=max_date, value=(min_date, max_date))
all_stores = sorted(df['StoreLocation'].unique())
selected_stores = st.sidebar.multiselect("Boutique Footprint", options=all_stores, default=all_stores)

mask = (df['Date'].dt.date.between(*date_selection)) & (df['StoreLocation'].isin(selected_stores))
filtered_df = df[mask]

if filtered_df.empty:
    st.warning("📊 No trading records found for the selected parameters.")
else:
    # ==========================================
    # 4. ENTERPRISE TABS
    # ==========================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Commercial Telemetry", 
        "🔮 AI Demand & Clustering", 
        "🌱 ESG & Supply Chain",
        "🤖 Brilliance AI"
    ])
    
    # ------------------------------------------
    # TAB 1: COMMERCIAL TELEMETRY
    # ------------------------------------------
    with tab1:
        total_rev = filtered_df['TotalRevenue'].sum()
        total_volume = len(filtered_df)
        atv = total_rev / total_volume if total_volume > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Gross Revenue Receipts", f"${total_rev:,.0f}")
        col2.metric("Transaction Volume", f"{total_volume:,}")
        col3.metric("Average Transaction Value", f"${atv:,.2f}")
        col4.metric("CX Sentiment Score", f"{filtered_df['CustomerRating'].mean():.2f} / 5.0")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        daily_rev = filtered_df.groupby('Date')['TotalRevenue'].sum().reset_index()
        daily_rev['7-Day Smooth Trend'] = daily_rev['TotalRevenue'].rolling(window=7, min_periods=1).mean()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=daily_rev['Date'], y=daily_rev['7-Day Smooth Trend'], 
                                       mode='lines', name='Gross Trend', 
                                       line=dict(color='#D4AF37', width=3),
                                       fill='tozeroy', fillcolor='rgba(212, 175, 55, 0.1)'))
        fig_trend.update_layout(
            title=dict(text="Rolling Trading Revenue Velocity", font=dict(color="#EAEAEA")), 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            hovermode="x unified", font=dict(color="#A0A0A0")
        )
        fig_trend.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        fig_trend.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig_trend, width="stretch")

    # ------------------------------------------
    # TAB 2: AI DEMAND & CLUSTERING
    # ------------------------------------------
    with tab2:
        col_ml1, col_ml2 = st.columns(2)
        
        with col_ml1:
            st.markdown("<h4 style='color:#EAEAEA;'>🔮 30-Day Predictive Forecasting</h4>", unsafe_allow_html=True)
            st.caption("Linear Regression AI projecting upcoming baseline revenue demand.")
            
            daily_rev['DateOrdinal'] = pd.to_datetime(daily_rev['Date']).map(datetime.datetime.toordinal)
            X = np.array(daily_rev['DateOrdinal']).reshape(-1, 1)
            y = np.array(daily_rev['TotalRevenue'])
            model = LinearRegression().fit(X, y)
            
            future_dates = [daily_rev['Date'].max() + datetime.timedelta(days=i) for i in range(1, 31)]
            future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
            predictions = model.predict(future_ordinals)
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=daily_rev['Date'], y=daily_rev['TotalRevenue'], mode='lines', name='Historical', line=dict(color='#888888', width=2)))
            fig_forecast.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines', name='AI Projection', line=dict(color='#D4AF37', dash='dash', width=3)))
            fig_forecast.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified", font=dict(color="#A0A0A0"))
            fig_forecast.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            fig_forecast.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_forecast, width="stretch")

        with col_ml2:
            st.markdown("<h4 style='color:#EAEAEA;'>👥 Autonomous Customer Segmentation</h4>", unsafe_allow_html=True)
            st.caption("K-Means Clustering identifying high-value buyer cohorts.")
            
            cluster_data = filtered_df[['UnitValue', 'CustomerRating', 'ProductCategory']].dropna().sample(n=min(800, len(filtered_df)), random_state=42)
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            cluster_data['Segment'] = kmeans.fit_predict(cluster_data[['UnitValue', 'CustomerRating']])
            
            segment_map = {0: "Everyday Silver", 1: "Lume LAB Bridal", 2: "Bespoke Luxury"}
            cluster_data['Cohort'] = cluster_data['Segment'].map(segment_map)
            
            fig_cluster = px.scatter(cluster_data, x='CustomerRating', y='UnitValue', color='Cohort', 
                                     color_discrete_sequence=['#888888', '#D4AF37', '#EAEAEA'])
            fig_cluster.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
            fig_cluster.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            fig_cluster.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_cluster, width="stretch")

    # ------------------------------------------
    # TAB 3: ESG & SUPPLY CHAIN
    # ------------------------------------------
    with tab3:
        col_esg, col_ops = st.columns(2)
        
        with col_esg:
            st.markdown("<h4 style='color:#EAEAEA;'>🌱 ESG: Responsible Sourcing Mix</h4>", unsafe_allow_html=True)
            st.caption("Tracking shift toward Re:cycle gold and Laboratory-Grown diamonds.")
            esg_trend = filtered_df.groupby([pd.Grouper(key='Date', freq='M'), 'ProductCategory'])['TotalRevenue'].sum().reset_index()
            fig_esg = px.area(esg_trend, x="Date", y="TotalRevenue", color="ProductCategory", 
                              color_discrete_sequence=['#D4AF37', '#555555', '#888888', '#222222', '#EAEAEA'])
            fig_esg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
            fig_esg.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            fig_esg.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_esg, width="stretch")

        with col_ops:
            st.markdown("<h4 style='color:#EAEAEA;'>🚚 Regional Fulfillment Latency</h4>", unsafe_allow_html=True)
            st.caption("Identifying operational bottlenecks in dispatch days.")
            delay_data = filtered_df.groupby('StoreLocation')['DeliveryDelayDays'].mean().reset_index().sort_values('DeliveryDelayDays', ascending=False)
            fig_delay = px.bar(delay_data, x='StoreLocation', y='DeliveryDelayDays', color_discrete_sequence=['#D4AF37'])
            fig_delay.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
            fig_delay.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            st.plotly_chart(fig_delay, width="stretch")

    # ------------------------------------------
    # TAB 4: BRILLIANCE AI CHATBOT
    # ------------------------------------------
    with tab4:
        st.markdown("<h3 style='margin-top: 10px;'>🤖 Brilliance AI: Natural Language Queries</h3>", unsafe_allow_html=True)
        st.caption("Type questions like: 'Which store has the highest sales?' or 'What is the ATV?'")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Welcome to Brilliance AI. How can I assist you with the Michael Hill performance data today?"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question about the data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = ""
            p_lower = prompt.lower()
            
            with st.chat_message("assistant"):
                if "highest" in p_lower and ("store" in p_lower or "location" in p_lower):
                    top_store = filtered_df.groupby('StoreLocation')['TotalRevenue'].sum().idxmax()
                    top_rev = filtered_df.groupby('StoreLocation')['TotalRevenue'].sum().max()
                    response = f"Based on your current filters, the highest performing boutique is **{top_store}** with a gross revenue of **${top_rev:,.2f}**."
                    
                elif "average" in p_lower or "atv" in p_lower or "aov" in p_lower:
                    atv_val = filtered_df['TotalRevenue'].sum() / len(filtered_df)
                    response = f"The Average Transaction Value (ATV) for the current filtered data is **${atv_val:,.2f}**."
                    
                elif "esg" in p_lower or "sustainability" in p_lower:
                    response = "According to the 2025 ESG Directives, Michael Hill is aggressively expanding the **Re:cycle program** to reduce reliance on mined gold, alongside pushing **Lume LAB** laboratory-grown diamonds to reduce carbon intensity per boutique."
                    
                elif "revenue" in p_lower:
                    total_r = filtered_df['TotalRevenue'].sum()
                    response = f"The total revenue for the selected timeframe is **${total_r:,.2f}**."
                    
                else:
                    response = f"I can currently identify top performing stores, calculate ATV, summarize total revenues, or discuss ESG initiatives. Could you rephrase your question?"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
