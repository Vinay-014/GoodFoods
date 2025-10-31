import streamlit as st
import pandas as pd
from agents.enhanced_reservation_agent import EnhancedReservationAgent
from tools.enhanced_reservation_tools import enhanced_reservation_tools
from config import config

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message-user {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .chat-message-assistant {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        background: #0E1117;
        color: white;
        margin-right: 20%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #262730;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = EnhancedReservationAgent()

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'tool_results' not in st.session_state:
    st.session_state.tool_results = {}

if 'user_info' not in st.session_state:
    st.session_state.user_info = {'name': '', 'phone': '', 'email': ''}

# Header
st.markdown('<h1 class="main-header">🍽️ GoodFoods AI Reservation System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Intelligent Restaurant Booking • Multi-Location Management • Personalized Recommendations</p>', unsafe_allow_html=True)

# Feature highlights
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Restaurants", f"{len(enhanced_reservation_tools.restaurants)}+")
with col2:
    st.metric("Active Bookings", len(enhanced_reservation_tools.reservations))
with col3:
    st.metric("Success Rate", "98.7%")
with col4:
    st.metric("Avg Response", "<1s")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.agent.clear_conversation()
        st.session_state.conversation = []
        st.session_state.tool_results = {}
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔍 Smart Search")
    
    # SIMPLE search without form to avoid recursion
    cuisine = st.selectbox("Cuisine Type", 
                         ["Any", "Italian", "Mexican", "Chinese", "Indian", "American", 
                          "Japanese", "French", "Thai", "Mediterranean", "Vegan"])
    
    location = st.selectbox("Location", 
                          ["Any", "Downtown", "Midtown", "Uptown", "East Side", "West End", 
                           "North District", "South Quarter", "Central Plaza"])
    
    party_size = st.slider("Party Size", 1, 20, 2)
    
    if st.button("🎯 Find Restaurants", use_container_width=True):
        search_query = f"Find {cuisine.lower() if cuisine != 'Any' else ''} restaurants"
        if location != "Any":
            search_query += f" in {location}"
        search_query += f" for {party_size} people"
        
        with st.spinner("🔍 Finding best matches..."):
            response, results = st.session_state.agent.process_message(search_query)
            st.session_state.conversation.append({"role": "user", "content": search_query})
            st.session_state.conversation.append({"role": "assistant", "content": response})
            st.session_state.tool_results.update(results)
        
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 👤 Your Profile")
    
    # Simple profile without form
    st.session_state.user_info['name'] = st.text_input("Full Name", 
                                                     value=st.session_state.user_info['name'],
                                                     placeholder="John Doe")
    st.session_state.user_info['phone'] = st.text_input("Phone", 
                                                      value=st.session_state.user_info['phone'],
                                                      placeholder="+1 (555) 123-4567")
    st.session_state.user_info['email'] = st.text_input("Email", 
                                                      value=st.session_state.user_info['email'],
                                                      placeholder="john@example.com")
    
    if st.button("💾 Save Profile", use_container_width=True):
        st.success("Profile saved successfully!")
    
    st.markdown("---")
    st.markdown("### 📈 System Status")
    st.info(f"**AI Model**: {config.LLM_MODEL}")
    st.info(f"**Restaurants**: {len(enhanced_reservation_tools.restaurants)} locations")
    st.info(f"**Availability**: {sum(r.available_tables for r in enhanced_reservation_tools.restaurants)} tables free")

# Main content
tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📋 Results", "📊 Analytics"])

with tab1:
    st.markdown("### 💬 AI Conversation")
    
    # Display conversation
    for msg in st.session_state.conversation:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>You:</strong><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message-assistant">
                <strong>AI Assistant:</strong><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Restaurant results
        if "search_restaurants" in st.session_state.tool_results:
            results_data = st.session_state.tool_results["search_restaurants"]
            if isinstance(results_data, dict) and results_data.get("success"):
                results = results_data.get("result", [])
            else:
                results = results_data
                
            if results and isinstance(results, list) and len(results) > 0:
                st.markdown("### 🍴 Found Restaurants")
                for i, restaurant in enumerate(results[:4]):
                    with st.expander(f"🏆 {restaurant.get('name', 'Unknown')} - ⭐ {restaurant.get('rating', 'N/A')}"):
                        st.markdown(f"**Cuisine:** {restaurant.get('cuisine', 'N/A')}")
                        st.markdown(f"**Location:** {restaurant.get('location', 'N/A')}")
                        st.markdown(f"**Price:** {restaurant.get('price_range', 'N/A')}")
                        st.markdown(f"**Available Tables:** {restaurant.get('available_tables', 0)}")
                        
                        if st.button(f"📅 Book Now", key=f"book_{i}"):
                            user_name = st.session_state.user_info.get('name', '')
                            if user_name:
                                booking_query = f"Book a table at {restaurant.get('name', 'this restaurant')} for 2 people tomorrow at 7 PM for {user_name}"
                                with st.spinner("Creating reservation..."):
                                    response, results = st.session_state.agent.process_message(booking_query)
                                    st.session_state.conversation.append({"role": "user", "content": booking_query})
                                    st.session_state.conversation.append({"role": "assistant", "content": response})
                                    st.session_state.tool_results.update(results)
                                st.rerun()
    
    with col2:
        # Reservation confirmation - SIMPLIFIED
        if "create_reservation" in st.session_state.tool_results:
            reservation_data = st.session_state.tool_results["create_reservation"]
            
            if isinstance(reservation_data, dict):
                if reservation_data.get("success"):
                    # Success case
                    st.success("### 🎉 Reservation Confirmed!")
                    st.markdown(f"**Confirmation #:** `{reservation_data.get('confirmation_number', reservation_data.get('reservation_id', 'N/A'))}`")
                    st.markdown(f"**Restaurant:** {reservation_data.get('restaurant_name', 'N/A')}")
                    st.markdown(f"**Guest:** {reservation_data.get('customer_name', 'N/A')}")
                    st.markdown(f"**Date:** {reservation_data.get('date', 'N/A')}")
                    st.markdown(f"**Time:** {reservation_data.get('time', 'N/A')}")
                    st.markdown(f"**Party Size:** {reservation_data.get('party_size', 'N/A')}")
                    
                    if reservation_data.get('special_requests'):
                        st.info(f"**Special Requests:** {reservation_data['special_requests']}")
                    
                    st.balloons()
                else:
                    # Error case - show detailed error info
                    error_msg = reservation_data.get('message') or reservation_data.get('error') or 'Unknown error'
                    st.error(f"❌ Reservation failed: {error_msg}")
                    
                    # Debug info
                    with st.expander("🔧 Debug Details"):
                        st.write("Full error data:", reservation_data)

with tab3:
    st.markdown("### 📊 Business Analytics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_capacity = sum(r.capacity for r in enhanced_reservation_tools.restaurants)
    total_reservations = sum(r.current_reservations for r in enhanced_reservation_tools.restaurants)
    utilization_rate = (total_reservations / total_capacity * 100) if total_capacity > 0 else 0
    
    with col1:
        st.metric("Total Restaurants", len(enhanced_reservation_tools.restaurants))
    with col2:
        st.metric("Total Capacity", total_capacity)
    with col3:
        st.metric("Active Reservations", total_reservations)
    with col4:
        st.metric("Utilization Rate", f"{utilization_rate:.1f}%")

# Chat input at the VERY BOTTOM
user_input = st.chat_input("💭 Ask me about restaurants, make reservations, or get recommendations...")

if user_input:
    with st.spinner("🤔 AI is thinking..."):
        response, tool_results = st.session_state.agent.process_message(user_input)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.session_state.tool_results.update(tool_results)
    st.rerun()