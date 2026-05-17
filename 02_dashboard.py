import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
import re

# ==========================================
# 1. BRAND ARCHITECTURE & DESIGN SYSTEM
# ==========================================
st.set_page_config(
    page_title="MHJ | Brilliance AI & Performance Hub", 
    page_icon="💍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# PEAK DETAILING CSS: Glassmorphism, Onyx Dark Mode, Gold Glow Animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    
    /* 1. Complete App Background (Onyx Gradient) */
    .stApp {
        background: linear-gradient(135deg, #0a0a0c 0%, #1a1a1f 100%);
        color: #F5F5F5;
    }
    
    /* 2. Hide Streamlit Clutter for a "Real App" feel */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 3. Typography Overrides */
    .block-container { padding-top: 1rem; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: #D4AF37 !important; text-shadow: 0px 2px 4px rgba(0,0,0,0.5); }
    p, span, div { color: #EAEAEA; }
    
    /* 4. Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(20, 20, 25, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(212, 175, 55, 0.15);
    }
    
    /* 5. Luxury Metric Cards with Hover Glow */
    [data-testid="metric-container"] {
        background: rgba(30, 30, 35, 0.4);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 3px solid #D4AF37; /* Signature Gold Base */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        background: rgba(40, 40, 45, 0.6);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.15); /* Gold Glow */
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 600; }
    [data-testid="stMetricLabel"] { color: #A0A0A0 !important; font-weight: 500; letter-spacing: 0.5px; text-transform: uppercase; font-size: 0.85rem;}
    
    /* 6. Tab Navigation Polish */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif; font-weight: 500; color: #888888; background-color: transparent;}
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; background-color: rgba(212,175,55,0.05);}
    
    /* 7. Brilliance AI Chat Styling */
    .stChatMessage { background: rgba(30, 30, 35, 0.4); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 10px; }
    
    /* 8. Fix Slider Colors */
    .stSlider [data-baseweb="slider"] div { background-color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# Main Corporate Header (Using pure text/HTML for perfect dark mode blending)
st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; padding-bottom: 10px;">
    <div style="background: linear-gradient(135deg, #D4AF37 0%, #AA8529 100%); width: 6px; height: 60px; margin-right: 20px; border-radius: 3px;"></div>
    <div>
        <h1 style='margin: 0px; padding: 0px; letter-spacing: 4px; font-size: 2.5rem; line-height: 1.1;'>MICHAEL HILL</h1>
        <p style='color: #A0A0A0; font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase; margin: 0px;'>Enterprise Telemetry & Brilliance AI Hub <span style="color:#D4AF37;">● LIVE</span></p>
    </div>
</div>
<hr style='border: 0; height: 1px; background-image: linear-gradient(to right, rgba(212, 175, 55, 0.5), rgba(255, 255, 255, 0)); margin-bottom: 30px;'>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA PIPELINE (Using Local CSV for stability)
# ==========================================
@st.cache_data
def load_performance_data():
    file_path = os.path.expanduser("~/Desktop/jewellery_retail_data.csv")
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df['MonthYear'] = df['Date'].dt.to_period('M').astype(str)
        return df
    except Exception:
        return pd.DataFrame()

df = load_performance_data()

if df.empty:
    st.error("⚠️ Data file not found. Please ensure 'jewellery_retail_data.csv' is on your Mac Desktop.")
else:
    # ==========================================
    # 3. CONTROL PANEL (SIDEBAR)
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
            "📈 Commercial Performance", 
            "🌱 2025 ESG & Sustainability", 
            "🚚 Operational Latency",
            "🤖 Brilliance AI Assistant"
        ])
        
        # ------------------------------------------
        # TAB 1: COMMERCIAL PERFORMANCE
        # ------------------------------------------
        with tab1:
            st.markdown("<h3 style='margin-top: 10px;'>Revenue & Transaction Velocity</h3>", unsafe_allow_html=True)
            total_rev = filtered_df['TotalRevenue'].sum()
            total_volume = len(filtered_df)
            atv = total_rev / total_volume if total_volume > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Gross Revenue Receipts", f"${total_rev:,.0f}")
            col2.metric("Total Transaction Volume", f"{total_volume:,}")
            col3.metric("Average Transaction Value", f"${atv:,.2f}")
            col4.metric("CX Sentiment Score", f"{filtered_df['CustomerRating'].mean():.2f} / 5.0")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            daily_rev = filtered_df.groupby('Date')['TotalRevenue'].sum().reset_index()
            daily_rev['7-Day Smooth Trend'] = daily_rev['TotalRevenue'].rolling(window=7, min_periods=1).mean()
            
            # Dark Mode Plotly Upgrade
            fig_trend = go.Figure()
            # Added fill='tozeroy' and an emerald/gold glow effect for premium feel
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
        # TAB 2: ESG & SUSTAINABILITY
        # ------------------------------------------
        with tab2:
            st.markdown("<h3 style='margin-top: 10px;'>2025 Corporate Responsibility</h3>", unsafe_allow_html=True)
            
            col_esg1, col_esg2, col_esg3 = st.columns(3)
            col_esg1.metric("Lab-Grown Diamond Share", "42.5%", "+8.2% YoY")
            col_esg2.metric("Re:cycle Gold Recovered", "12.4 kg", "On Target")
            col_esg3.metric("Carbon Intensity per Boutique", "-14.1%", "Scope 2 Reduction")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            esg_chart_col1, esg_chart_col2 = st.columns(2)
            with esg_chart_col1:
                st.markdown("<h4 style='color:#EAEAEA;'>Responsible Sourcing Trajectory</h4>", unsafe_allow_html=True)
                esg_trend = filtered_df.groupby([pd.Grouper(key='Date', freq='M'), 'ProductCategory'])['TotalRevenue'].sum().reset_index()
                fig_esg = px.area(esg_trend, x="Date", y="TotalRevenue", color="ProductCategory", 
                                  color_discrete_sequence=['#D4AF37', '#7f8c8d', '#bdc3c7', '#34495e', '#ecf0f1'])
                fig_esg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
                fig_esg.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                fig_esg.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                st.plotly_chart(fig_esg, width="stretch")

            with esg_chart_col2:
                st.markdown("<h4 style='color:#EAEAEA;'>The Michael Hill Foundation</h4>", unsafe_allow_html=True)
                st.info("**Key 2025 ESG Pillars:**\n\n1. **Empowering Women:** Over $1.5M contributed to aligned charities.\n2. **Restoring Nature:** Over 200,000 trees planted via global partnerships.\n3. **Re:cycle Program:** Expanding circular economy trade-ins across all flagships to reduce reliance on newly mined gold.")

        # ------------------------------------------
        # TAB 3: OPERATIONAL LATENCY
        # ------------------------------------------
        with tab3:
            st.markdown("<h3 style='margin-top: 10px;'>Fulfillment & Brand Advocacy Tracking</h3>", unsafe_allow_html=True)
            col_op1, col_op2 = st.columns(2)
            
            with col_op1:
                st.markdown("<h4 style='color:#EAEAEA;'>Average Fulfillment Latency (Days)</h4>", unsafe_allow_html=True)
                delay_data = filtered_df.groupby('StoreLocation')['DeliveryDelayDays'].mean().reset_index().sort_values('DeliveryDelayDays', ascending=False)
                fig_delay = px.bar(delay_data, x='StoreLocation', y='DeliveryDelayDays', color_discrete_sequence=['#D4AF37'])
                fig_delay.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
                fig_delay.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                st.plotly_chart(fig_delay, width="stretch")
                
            with col_op2:
                st.markdown("<h4 style='color:#EAEAEA;'>Customer Sentiment Tiering</h4>", unsafe_allow_html=True)
                sentiment_data = filtered_df.groupby(['StoreLocation', 'SentimentLabel']).size().reset_index(name='Volume')
                fig_sentiment = px.bar(sentiment_data, x='StoreLocation', y='Volume', color='SentimentLabel', barmode='stack', 
                                       color_discrete_map={'Positive': '#D4AF37', 'Neutral': '#7f8c8d', 'Negative': '#e74c3c'})
                fig_sentiment.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#A0A0A0"))
                fig_sentiment.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                st.plotly_chart(fig_sentiment, width="stretch")

        # ------------------------------------------
        # TAB 4: BRILLIANCE AI ASSISTANT (NLP Chatbot)
        # ------------------------------------------
        with tab4:
            st.markdown("<h3 style='margin-top: 10px;'>🤖 Brilliance AI: Natural Language Intelligence</h3>", unsafe_allow_html=True)
            st.caption("Ask questions about the current dataset. E.g., 'What is the revenue for March 2026?' or 'Which store has the highest sales?'")
            
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
                    month_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s(2024|2025|2026)', p_lower)
                    
                    if "revenue" in p_lower and month_match:
                        month_str = month_match.group(0).title()
                        month_dt = pd.to_datetime(month_str, format='%B %Y').to_period('M').astype(str)
                        month_df = df[df['MonthYear'] == month_dt]
                        if not month_df.empty:
                            m_rev = month_df['TotalRevenue'].sum()
                            response = f"The total gross revenue for **{month_str}** was **${m_rev:,.2f}**."
                        else:
                            response = f"I couldn't find any trading data for {month_str}."
                            
                    elif "highest" in p_lower and ("store" in p_lower or "location" in p_lower):
                        top_store = filtered_df.groupby('StoreLocation')['TotalRevenue'].sum().idxmax()
                        top_rev = filtered_df.groupby('StoreLocation')['TotalRevenue'].sum().max()
                        response = f"Based on your current filters, the highest performing boutique is **{top_store}** with a revenue of **${top_rev:,.2f}**."
                        
                    elif "esg" in p_lower or "sustainability" in p_lower or "recycle" in p_lower:
                        response = "According to the 2025 ESG Directives, Michael Hill is aggressively expanding the **Re:cycle program** to reduce reliance on mined gold, alongside pushing **Lume LAB** laboratory-grown diamonds to reduce carbon intensity per boutique."
                        
                    elif "average" in p_lower or "atv" in p_lower or "aov" in p_lower:
                        atv_val = filtered_df['TotalRevenue'].sum() / len(filtered_df)
                        response = f"The Average Transaction Value (ATV) for the current filtered data is **${atv_val:,.2f}**."
                        
                    else:
                        response = f"To ensure absolute accuracy, I can currently calculate total revenues by specific months (e.g., 'Revenue for March 2026'), identify top performing stores, calculate ATV, or discuss ESG initiatives. Could you rephrase your question?"
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})