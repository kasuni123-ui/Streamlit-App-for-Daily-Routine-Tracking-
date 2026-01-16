import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from PIL import Image
import requests
import base64
import io
import time
import random
import json

# Page configuration
st.set_page_config(
    page_title="Eternal Vows - Wedding Portal",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.weddingwire.com',
        'Report a bug': "mailto:planner@eternalvows.com",
        'About': "# Eternal Vows Wedding Portal\n### A Beautiful Celebration of Love"
    }
)

# Try to import streamlit_lottie, but handle if it's not available
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
    
    @st.cache_data
    def load_lottieurl(url: str):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
        except:
            return None
    
except ImportError:
    LOTTIE_AVAILABLE = False
    st_lottie = None
    load_lottieurl = None
    st.warning("✨ For animations, install: pip install streamlit-lottie")

# Advanced CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400;600&family=Cormorant+Garamond:wght@300;400;600&display=swap');
    
    /* Main background with beautiful gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #d4af37 50%, #e73c7e 75%, #23a6d5 100%);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Wedding title with shine effect */
    .wedding-title {
        font-family: 'Dancing Script', cursive;
        font-size: 5rem !important;
        background: linear-gradient(45deg, #FFD700, #FF8C00, #FF69B4, #9370DB);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 4s ease-in-out infinite alternate;
        text-align: center;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 0;
        padding: 20px;
    }
    
    @keyframes shine {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    
    .couple-names {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        color: white;
        text-align: center;
        margin-top: 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        animation: float 6s ease-in-out infinite;
        padding-bottom: 30px;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .section-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem;
        color: white;
        border-bottom: 3px solid rgba(255, 215, 0, 0.5);
        padding-bottom: 15px;
        margin-top: 40px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        padding-left: 20px;
    }
    
    .section-header::before {
        content: '❦';
        position: absolute;
        left: 0;
        color: #FFD700;
        font-size: 2rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Glass morphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 215, 0, 0.4);
    }
    
    .glass-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        transition: 0.5s;
    }
    
    .glass-card:hover::after {
        left: 100%;
    }
    
    /* Countdown boxes */
    .countdown-box {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        color: white;
        padding: 25px 15px;
        border-radius: 20px;
        text-align: center;
        margin: 10px;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px solid rgba(255, 255, 255, 0.25);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .countdown-box:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-5px);
        border-color: rgba(255, 215, 0, 0.5);
    }
    
    .countdown-number {
        font-size: 3.2rem;
        font-weight: bold;
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(45deg, #FFD700, #FF69B4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: countdownPulse 3s infinite;
    }
    
    @keyframes countdownPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.9; }
    }
    
    .countdown-label {
        font-size: 1.1rem;
        opacity: 0.9;
        font-family: 'Cormorant Garamond', serif;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 10px;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(45deg, #FFD700, #FF8C00);
        color: white;
        border: none;
        padding: 15px 35px;
        border-radius: 30px;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
        z-index: 1;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }
    
    .btn-primary:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
    }
    
    .btn-primary:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Guest cards */
    .guest-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .guest-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 215, 0, 0.3);
    }
    
    /* Photo gallery */
    .photo-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .gallery-item {
        border-radius: 15px;
        overflow: hidden;
        position: relative;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        aspect-ratio: 4/3;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .gallery-item:hover {
        transform: scale(1.08) rotate(1deg);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        z-index: 10;
        border-color: rgba(255, 215, 0, 0.5);
    }
    
    /* Timeline */
    .timeline-item {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        position: relative;
        border-left: 5px solid;
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
        border-color: #FFD700;
    }
    
    @keyframes slideIn {
        from { 
            transform: translateX(-30px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    .timeline-item:hover {
        transform: translateX(10px);
        border-color: #FF69B4;
    }
    
    /* Progress bars */
    .progress-container {
        margin: 20px 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        color: white;
        font-family: 'Montserrat', sans-serif;
    }
    
    .progress-bar {
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFD700, #FF69B4, #9370DB);
        border-radius: 6px;
        position: relative;
        transition: width 1s ease-out;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Floating elements */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Sparkle effect */
    .sparkle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: white;
        border-radius: 50%;
        box-shadow: 0 0 10px 2px white;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 10px 15px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 40px 0;
        position: relative;
    }
    
    .divider::before,
    .divider::after {
        content: '❦';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        color: #FFD700;
        font-size: 1.5rem;
    }
    
    .divider::before { left: 20%; }
    .divider::after { right: 20%; }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for floating hearts (works without any packages)
st.markdown("""
<script>
// Create floating hearts animation
document.addEventListener('DOMContentLoaded', function() {
    const container = document.createElement('div');
    container.id = 'floating-hearts';
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    document.body.appendChild(container);
    
    function createHeart() {
        const heart = document.createElement('div');
        heart.innerHTML = '❤️';
        heart.style.cssText = `
            position: fixed;
            font-size: ${Math.random() * 20 + 15}px;
            left: ${Math.random() * 100}vw;
            top: 105vh;
            opacity: ${Math.random() * 0.4 + 0.3};
            z-index: -1;
            pointer-events: none;
            animation: floatHeart ${Math.random() * 4 + 4}s linear forwards;
            filter: drop-shadow(0 0 5px rgba(255, 69, 69, 0.5));
        `;
        
        // Add custom animation
        const style = document.createElement('style');
        if (!document.querySelector('#heart-animation')) {
            style.id = 'heart-animation';
            style.textContent = `
                @keyframes floatHeart {
                    0% {
                        transform: translateY(0) rotate(0deg) scale(1);
                        opacity: 0.8;
                    }
                    100% {
                        transform: translateY(-110vh) rotate(${Math.random() * 360}deg) scale(0.5);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        container.appendChild(heart);
        
        // Remove heart after animation
        setTimeout(() => {
            if (heart.parentNode) {
                heart.remove();
            }
        }, 6000);
    }
    
    // Create hearts periodically
    setInterval(createHeart, 800);
    
    // Create initial hearts
    for (let i = 0; i < 15; i++) {
        setTimeout(createHeart, i * 200);
    }
    
    // Add sparkle effects
    function createSparkle() {
        const sparkle = document.createElement('div');
        sparkle.style.cssText = `
            position: fixed;
            width: 3px;
            height: 3px;
            background: white;
            border-radius: 50%;
            box-shadow: 0 0 8px 2px white;
            animation: sparkle 1.5s ease-out forwards;
            z-index: -1;
        `;
        
        sparkle.style.left = Math.random() * 100 + 'vw';
        sparkle.style.top = Math.random() * 100 + 'vh';
        
        if (!document.querySelector('#sparkle-animation')) {
            const sparkleStyle = document.createElement('style');
            sparkleStyle.id = 'sparkle-animation';
            sparkleStyle.textContent = `
                @keyframes sparkle {
                    0% { opacity: 0; transform: scale(0); }
                    50% { opacity: 1; transform: scale(1); }
                    100% { opacity: 0; transform: scale(0); }
                }
            `;
            document.head.appendChild(sparkleStyle);
        }
        
        container.appendChild(sparkle);
        
        setTimeout(() => {
            if (sparkle.parentNode) {
                sparkle.remove();
            }
        }, 1500);
    }
    
    // Create sparkles periodically
    setInterval(createSparkle, 300);
});
</script>
""", unsafe_allow_html=True)

# Sample data
def generate_sample_data():
    guests = pd.DataFrame({
        'Name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown',
                'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Ivy Garcia', 'Jack Martinez'],
        'RSVP': ['Confirmed', 'Pending', 'Confirmed', 'Declined', 'Confirmed',
                'Confirmed', 'Pending', 'Confirmed', 'Confirmed', 'Declined'],
        'Guests': [2, 1, 2, 0, 1, 2, 2, 1, 3, 0],
        'Meal': ['Vegetarian', 'Non-Veg', 'Vegetarian', None, 'Non-Veg',
                'Vegetarian', 'Non-Veg', 'Vegetarian', 'Non-Veg', None],
        'Table': [1, 2, 1, None, 3, 2, 3, 1, 4, None]
    })
    
    timeline = [
        {'time': '14:00', 'event': 'Guests Arrival & Welcome Drinks', 'icon': '🥂', 'color': '#FFD700'},
        {'time': '14:30', 'event': 'Bride\'s Entrance & Ceremony Begins', 'icon': '👰', 'color': '#FF69B4'},
        {'time': '15:30', 'event': 'Exchange of Vows & Rings', 'icon': '💍', 'color': '#9370DB'},
        {'time': '16:00', 'event': 'Photo Session', 'icon': '📸', 'color': '#1E90FF'},
        {'time': '17:00', 'event': 'Cocktail Hour', 'icon': '🍹', 'color': '#32CD32'},
        {'time': '18:00', 'event': 'Reception & Dinner', 'icon': '🍽️', 'color': '#FF8C00'},
        {'time': '20:00', 'event': 'First Dance & Party', 'icon': '💃', 'color': '#FF1493'},
        {'time': '22:00', 'event': 'Cake Cutting', 'icon': '🎂', 'color': '#DAA520'},
        {'time': '23:00', 'event': 'Farewell & Send-off', 'icon': '🎆', 'color': '#4682B4'}
    ]
    
    budget = pd.DataFrame({
        'Category': ['Venue', 'Catering', 'Photography', 'Music', 'Decorations', 
                    'Attire', 'Invitations', 'Flowers', 'Transportation', 'Miscellaneous'],
        'Budget': [5000, 4000, 2000, 1500, 2500, 3000, 800, 1200, 1000, 1000],
        'Actual': [5200, 3800, 2100, 1400, 2300, 3200, 750, 1300, 950, 1100]
    })
    
    return guests, timeline, budget

# Function to create beautiful image placeholder
def create_image_placeholder(width=300, height=200, text="Beautiful Image"):
    # Create a gradient image with text
    img = Image.new('RGB', (width, height), color='black')
    return img

# Sidebar Navigation
with st.sidebar:
    # Animated header with emojis if Lottie is not available
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOTTIE_AVAILABLE and load_lottieurl:
            lottie_heart = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_vnikrcia.json")
            if lottie_heart:
                st_lottie(lottie_heart, height=120, key="sidebar_heart")
        else:
            # Fallback: Use animated emojis
            st.markdown("""
            <div style='text-align: center; animation: floating 3s ease-in-out infinite;'>
                <span style='font-size: 4rem;'>💖</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3 style='color: #FFD700; font-family: "Dancing Script", cursive; font-size: 2.8rem; 
                   text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);'>
            Eternal Vows
        </h3>
        <p style='color: white; font-family: "Playfair Display", serif; font-size: 1.4rem;'>
            Sarah & Michael
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation with icons
    page_options = {
        "🏠 Home Dashboard": "home",
        "📅 Wedding Details": "details",
        "👥 Guest Management": "guests",
        "💰 Budget Tracker": "budget",
        "📸 Photo Gallery": "gallery",
        "🎁 Gift Registry": "gifts",
        "🗺️ Venue & Accommodation": "venue",
        "💌 Contact & Messages": "contact",
        "🎵 Song Requests": "music"
    }
    
    page = st.selectbox(
        "🎯 Navigate",
        list(page_options.keys())
    )
    
    st.markdown("---")
    
    # Countdown in sidebar
    wedding_date = datetime(2024, 12, 15, 16, 0, 0)
    current_date = datetime.now()
    time_left = wedding_date - current_date
    
    st.markdown(f"""
    <div class='glass-card' style='text-align: center; margin: 20px 0;'>
        <div style='font-size: 2rem; color: #FFD700; margin-bottom: 10px;'>⏳</div>
        <h4 style='color: white; margin-bottom: 15px;'>Countdown to Our Wedding</h4>
        <div style='font-size: 1.8rem; color: white; font-weight: bold; font-family: "Montserrat", sans-serif;'>
            {time_left.days} <span style='font-size: 1rem;'>days</span>
        </div>
        <div style='color: rgba(255, 255, 255, 0.8); margin-top: 10px;'>
            {time_left.seconds // 3600}h {(time_left.seconds % 3600) // 60}m
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calendar emoji animation if Lottie not available
    if not LOTTIE_AVAILABLE:
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <div style='font-size: 4rem; animation: floating 3s ease-in-out infinite;'>📅</div>
        </div>
        """, unsafe_allow_html=True)

# Main content
if page == "🏠 Home Dashboard":
    # Hero Section
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <h1 class='wedding-title'>Eternal Vows</h1>
            <h2 class='couple-names'>Sarah & Michael</h2>
            <div style='margin-top: 20px;'>
                <span style='display: inline-block; animation: floating 3s ease-in-out infinite 0.2s; 
                           font-size: 2rem; margin: 0 10px;'>💍</span>
                <span style='display: inline-block; animation: floating 3s ease-in-out infinite 0.4s; 
                           font-size: 2rem; margin: 0 10px;'>✨</span>
                <span style='display: inline-block; animation: floating 3s ease-in-out infinite 0.6s; 
                           font-size: 2rem; margin: 0 10px;'>💕</span>
            </div>
            <p style='text-align: center; font-size: 1.5rem; color: white; 
                     font-family: "Cormorant Garamond", serif; margin-top: 20px;'>
                December 15, 2024 • The Grand Palace • 4:00 PM
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Animated rings (fallback if no Lottie)
    if LOTTIE_AVAILABLE and load_lottieurl:
        lottie_rings = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_cq5jqerh.json")
        if lottie_rings:
            st_lottie(lottie_rings, height=300, key="home_rings")
    else:
        st.markdown("""
        <div style='text-align: center; margin: 40px 0;'>
            <div style='display: inline-block; animation: floating 4s ease-in-out infinite; 
                       font-size: 8rem; filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.5));'>
                💍
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Countdown Section
    st.markdown("<div class='section-header'>🎊 Countdown to Our Special Day</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    countdown_data = [
        {"value": time_left.days, "label": "DAYS", "emoji": "📅"},
        {"value": time_left.seconds // 3600, "label": "HOURS", "emoji": "⏰"},
        {"value": (time_left.seconds % 3600) // 60, "label": "MINUTES", "emoji": "⏳"},
        {"value": time_left.seconds % 60, "label": "SECONDS", "emoji": "⚡"}
    ]
    
    for idx, data in enumerate(countdown_data):
        with [col1, col2, col3, col4][idx]:
            st.markdown(f"""
            <div class='countdown-box'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>{data['emoji']}</div>
                <div class='countdown-number'>{data['value']}</div>
                <div class='countdown-label'>{data['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("<div class='section-header'>✨ Wedding Overview</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        {"icon": "👥", "title": "Total Guests", "value": "142", "change": "+8", "color": "#FFD700"},
        {"icon": "✅", "title": "RSVP Confirmed", "value": "128", "change": "90%", "color": "#32CD32"},
        {"icon": "💰", "title": "Budget Used", "value": "$21,500", "change": "$1,500", "color": "#FF69B4"},
        {"icon": "🎁", "title": "Gifts Received", "value": "45", "change": "12 pending", "color": "#9370DB"}
    ]
    
    for idx, stat in enumerate(stats):
        with [col1, col2, col3, col4][idx]:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; border-top: 3px solid {stat['color']};'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>{stat['icon']}</div>
                <div style='font-size: 1.2rem; color: white; margin-bottom: 10px;'>{stat['title']}</div>
                <div style='font-size: 2.2rem; color: {stat['color']}; font-weight: bold;'>{stat['value']}</div>
                <div style='font-size: 1rem; color: rgba(255, 255, 255, 0.8); margin-top: 5px;'>
                    {stat['change']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("<div class='section-header'>📝 Recent Activity</div>", unsafe_allow_html=True)
    
    # Animated flowers if Lottie available
    if LOTTIE_AVAILABLE and load_lottieurl:
        lottie_flowers = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_ygiqnxd3.json")
        if lottie_flowers:
            st_lottie(lottie_flowers, height=200, key="home_flowers")
    
    with st.expander("✨ View Recent Updates", expanded=True):
        activities = [
            {"icon": "🎁", "text": "Emily Johnson sent a beautiful crystal vase", "time": "2 hours ago"},
            {"icon": "✅", "text": "Robert Brown confirmed attendance for 2 guests", "time": "Yesterday"},
            {"icon": "📸", "text": "Photographer booked for pre-wedding shoot in Central Park", "time": "2 days ago"},
            {"icon": "💐", "text": "Florist finalized decoration plan with peonies and roses", "time": "3 days ago"},
            {"icon": "🍰", "text": "Cake tasting completed - Chocolate & Raspberry flavor selected", "time": "4 days ago"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class='guest-card'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <span style='font-size: 1.8rem; animation: floating 2s ease-in-out infinite;'>
                        {activity['icon']}
                    </span>
                    <div style='flex: 1;'>
                        <div style='color: white; font-size: 1.1rem;'>{activity['text']}</div>
                        <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 5px;'>
                            {activity['time']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Continue with other pages similarly...

# Footer
st.markdown("""
<div class='divider'></div>

<div style='text-align: center; padding: 40px 0;'>
    <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;'>
        <span style='font-size: 3rem; animation: floating 3s ease-in-out infinite;'>✨</span>
        <span style='font-size: 3rem; animation: floating 3s ease-in-out infinite 0.2s;'>💍</span>
        <span style='font-size: 3rem; animation: floating 3s ease-in-out infinite 0.4s;'>✨</span>
    </div>
    
    <p style='color: white; font-family: "Cormorant Garamond", serif; font-size: 1.4rem; 
              margin-bottom: 10px;'>
        Made with infinite love for Sarah & Michael's Wedding
    </p>
    <p style='color: rgba(255, 255, 255, 0.8); font-size: 1.1rem; margin-bottom: 30px;'>
        December 15, 2024 • The Grand Palace • New York
    </p>
    
    <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;'>
        <button class='btn-primary' style='background: linear-gradient(45deg, #FFD700, #FF8C00);'>
            📧 Contact Us
        </button>
        <button class='btn-primary' style='background: linear-gradient(45deg, #9370DB, #8A2BE2);'>
            📱 Download App
        </button>
        <button class='btn-primary' style='background: linear-gradient(45deg, #32CD32, #228B22);'>
            💌 Send Blessings
        </button>
        <button class='btn-primary' style='background: linear-gradient(45deg, #1E90FF, #4169E1);'>
            📸 Share Photos
        </button>
    </div>
    
    <div style='margin-top: 40px; color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;'>
        <p>© 2024 Eternal Vows Wedding Portal. All rights reserved.</p>
        <p>Need assistance? Email us at: planner@eternalvows.com</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Celebration animation at the bottom
if LOTTIE_AVAILABLE and load_lottieurl:
    lottie_celebration = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_0fhjvtlj.json")
    if lottie_celebration:
        st_lottie(lottie_celebration, height=250, key="final_celebration")
else:
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <div style='display: inline-block; animation: floating 3s ease-in-out infinite; 
                   font-size: 5rem; filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.5));'>
            🎉
        </div>
        <div style='display: inline-block; animation: floating 3s ease-in-out infinite 0.3s; 
                   margin-left: 30px; font-size: 5rem; filter: drop-shadow(0 0 15px rgba(255, 69, 69, 0.5));'>
            🥂
        </div>
        <div style='display: inline-block; animation: floating 3s ease-in-out infinite 0.6s; 
                   margin-left: 30px; font-size: 5rem; filter: drop-shadow(0 0 15px rgba(147, 112, 219, 0.5));'>
            ✨
        </div>
    </div>
    """, unsafe_allow_html=True)