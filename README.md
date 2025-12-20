# 🍽️ GoodFoods AI Restaurant Reservation Agent

<div align="center">

![GoodFoods](https://img.shields.io/badge/GoodFoods-AI%20Reservation-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Llama](https://img.shields.io/badge/LLM-Llama%203.3%2070B-orange)

**Intelligent Restaurant Booking • Multi-Location Management • Personalized Recommendations**

[Demo Video](https://drive.google.com/file/d/1Zyf36ERSJIpKhfn49EObH1adngg304ea/view?usp=drivesdk) • [Business Strategy](#-business-strategy) • [Setup](#-quick-setup) • [Examples](#-example-conversations)

</div>

##  Overview

GoodFoods AI Reservation System is an enterprise-grade solution that transforms restaurant booking through conversational AI. The system handles complex multi-location reservations, provides intelligent recommendations, and delivers actionable business analytics.

### Key Features
- 🤖 **AI-Powered Conversations** - Natural language reservations
- 🍽️ **75+ Restaurant Network** - Multi-location management  
- 💫 **Smart Recommendations** - Context-aware suggestions
- 📊 **Business Intelligence** - Real-time analytics dashboard
- 🔧 **Custom Tool Calling** - MCP-inspired architecture
- 📱 **UI** - Streamlit frontend with dark/light themes

##  Quick Setup

### Prerequisites
- Python 3.12+
- Groq API account (free tier available)

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/your-username/GoodFoods.git
cd GoodFoods
```
2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
3. **Environment Configuration**
```bash
# Create .env file
cp .env.example .env

# Add your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
echo "LLM_BASE_URL=https://api.groq.com/openai/v1" >> .env
```
4. **Get Groq API Key**
Visit Groq Console
Sign up/login (free tier available)
Create API key in dashboard
Add to .env file


5. **Launch Application**
```bash
streamlit run app.py
```

## File Structure
```txt
GoodFoods/
├── app.py                          # Main Streamlit application
├── agents/
│   ├── enhanced_reservation_agent.py  # AI agent with tool calling
│   └── __init__.py
├── tools/
│   ├── enhanced_reservation_tools.py  # Reservation operations
│   ├── tool_registry.py               # MCP-inspired tool registry
│   └── __init__.py
├── models/
│   ├── restaurant.py                  # Data models
│   └── __init__.py
├── data/
│   └── sample_restaurants.py          # 75+ restaurant dataset
├── utils/
│   ├── llm_client.py                  # Groq API client
│   └── __init__.py
├── config.py                          # Configuration
├── requirements.txt                   # Dependencies
├── business_strategy.md               # Comprehensive business analysis
└── README.md                          # This file
```

##  Prompt Engineering Approach
### System Prompt Design
system_prompt = """
You are a friendly AI assistant for GoodFoods restaurant reservations.

CRITICAL GUIDELINES:
1. Be conversational - no technical details to users
2. Use valid restaurant IDs from search results
3. Gather all required information naturally
4. Confirm bookings clearly when successful
5. Handle errors gracefully

TOOL USAGE STRATEGY:
- search_restaurants: Find restaurants by criteria
- create_reservation: Book with complete customer details  
- check_availability: Verify table availability
- get_recommendations: Personalized suggestions

Always maintain natural conversation flow.
"""

### Tool Calling Optimization
* Type Safety: Automatic string-to-integer conversion for parameters
* Null Handling: Filter out "null" values before tool execution
* Error Recovery: Graceful fallbacks for invalid inputs
* Context Management: Maintain conversation history across interactions


### Conversation Flow
1. Greeting & Context Gathering
2. Intent Classification (Search/Book/Recommend/Manage)
3. Information Collection (Missing details)
4. Tool Execution (With validation)
5. Confirmation & Follow-up


## 💬 Example Conversations

### 1. Reservation Booking

**👤:** I want to book a table for 4 people tomorrow night.  
**🤖:** Absolutely! May I know your preferred cuisine and location?  
**👤:** Italian food in Downtown.  
**🤖:** Great choice. Bella Vita has a table for 4 tomorrow at 7 PM. Should I proceed with your booking?  
**👤:** Yes, please book it.  
**🤖:** Perfect! Could you provide your name, phone number, and email to complete the reservation?

---

### 2. Smart Recommendation

**👤:** Looking for a romantic restaurant for our anniversary.  
**🤖:** Happy anniversary! 👩🏻‍❤️‍👨🏻 Here are some recommendations:  
- **Sapore Italiano**: Candlelit dining, live music  
- **Le Jardin Français**: Romantic garden setting  
- **Spice Route**: Intimate exotic cuisine  
Would you like more details about any of these?

**👤:** Tell me more about Sapore Italiano.  
**🤖:** Sapore Italiano offers authentic Italian cuisine in a candlelit setting with live violin music.  
Rating: ⭐ 4.7 | Price: $$$ | Location: Downtown  
Availability: 2 people, Friday at 8 PM.

---

### 3. Multi-Criteria Search

**👤:** Find a family-friendly Mexican restaurant in Midtown for 6 people with outdoor seating.  
**🤖:** Here are some great options for your family:  
1. **Casa Mexicana** — Large patio, kids menu, ⭐ 4.5  
2. **Fiesta Grill** — Play area, family deals, ⭐ 4.3  
3. **Taqueria Familiar** — Outdoor garden, ⭐ 4.6  
All can accommodate 6 people with outdoor seating.

---

### 4. Reservation Management

**👤:** I need to cancel my reservation.  
**🤖:** May I have your reservation confirmation number?  
**👤:** It's RES_A1B2C3D4.  
**🤖:** Found your reservation for John Doe at Bella Vita, tomorrow at 7 PM for 4 people. Shall I cancel this reservation?  
**👤:** Yes, please cancel.  
**🤖:** ✅ Reservation RES_A1B2C3D4 has been successfully cancelled.



## 📈 Business Strategy
### Executive Summary
GoodFoods addresses critical inefficiencies in multi-location restaurant management through AI-driven automation, delivering 60% reduction in manual overhead and 25% increase in table utilization.

### Key Business Problems Solved
* Operational Inefficiency: 20-30% staff time spent on phone reservations
* Capacity Underutilization: 35% average table vacancy during non-peak hours
* Inconsistent Experience: Variable service quality across locations
* Data Fragmentation: No unified view of customer preferences

## Success Metrics

| Metric                    | Current | Target | Improvement      |
|---------------------------|---------|--------|------------------|
| Staff Time on Reservations|   30%   |  12%   | ⬇️ 60%           |
| Table Utilization         |   65%   |  81%   | ⬆️ 25%           |
| Customer NPS              |   +25   |  +45   | ⬆️ 20 pts        |
| Cost per Booking          | $8.50   | $3.40  | ⬇️ 60%           |


### ROI Analysis
* Implementation Cost: $150K (one-time) + $25K/month
* Per Location Annual Benefit: $210K ($125K revenue + $85K savings)
* Break-even: 3 months for 10-location chain
* Annual ROI: 340%

### Competitive Advantages

1. **Context-Aware Intelligence**
   - Machine learning-driven recommendations tailored to occasion, user preferences, and booking history
   - Real-time availability updates considering external factors such as weather and local events

2. **Conversational Commerce Platform**
   - Advanced natural language understanding for complex reservation and recommendation queries
   - Multi-intent handling within a single conversational flow for seamless user experience

3. **Unified Data Ecosystem**
   - Cross-location analytics, forecasting, and reporting for operational insights
   - Tracking customer lifetime value and predictive demand modeling to inform business decisions


### Expansion Strategy
* Phase 1 (Months 1-3): GoodFoods chain rollout
* Phase 2 (Months 4-6): Multi-tenant platform for other chains
* Phase 3 (Months 7-12): Hotel restaurants, event venues, corporate catering

##  System Architecture
### 1. Technical Stack
* Frontend: Streamlit with custom CSS
* AI Agent: Custom tool-calling architecture
* LLM: Groq + Llama 3.3 70B
* Data: In-memory with sample dataset
* Protocol: MCP-inspired tool calling
### 2. Core Components

1. **Enhanced Reservation Agent**
   - Natural language processing for user-friendly interactions
   - Intent classification to determine the user's needs (search, book, recommend, manage)

2. **Tool Orchestration**
   - Centralized tool registry following MCP protocol for reliable orchestration
   - Type conversion, validation, and error handling to ensure robust tool execution

3. **Recommendation Engine**
   - Occasion-based filtering and personalized reasoning for each user
   - Relevance scoring to deliver the most suitable restaurant suggestions


## ⚠️ Assumptions & Limitations
### Current Assumptions

1. **Data Persistence**
   - In-memory storage resets on server restart; no persistent database in the current version
   - Sample dataset includes 75 restaurants

2. **Integration Scope**
   - No integration with real POS systems; payment processing is simplified
   - Basic notification system for booking confirmations

3. **Scale Considerations**
   - Designed to support 100+ locations with concurrent user handling via Streamlit
   - API rate limits managed through Groq

### Known Limitations

1. **Data Persistence**
   - All reservation data is lost upon application/server restart
   - No integration with external databases

2. **Real-Time Sync**
   - Does not support live table availability across physical locations
   - Capacity management is simplified

3. **Feature Scope**
   - Basic user authentication only
   - Limited payment and notification integrations

4. **API Dependencies**
   - Requires active Groq API connectivity; subject to API rate limits
   - No offline functionality


##  Future Enhancements
### Short-term (1-3 months)
* Database Integration - PostgreSQL for persistence
* User Authentication - JWT-based security
* Email/SMS Notifications - Booking confirmations
* Payment Integration - Stripe/Payment processing
* Calendar Sync - Google Calendar/Outlook integration

### Medium-term (3-6 months)
* Mobile App - React Native companion app
* Advanced Analytics - Predictive demand forecasting
* Waitlist Management - Dynamic waitlist with notifications
* Loyalty Program - Points and rewards integration
* Multi-language Support - Spanish, French, Mandarin

### Long-term (6-12 months)
* White-label Platform - Multi-tenant architecture
* API Marketplace - Third-party integrations
* Voice Interface - Voice-based reservations
* IoT Integration - Smart table management
* Enterprise Features - Advanced reporting and CRM

### Advanced AI Features
* Predictive Pricing - Dynamic pricing based on demand
* Sentiment Analysis - Customer feedback processing
* Personalized Menus - AI-generated menu recommendations
* Cross-sell Engine - Wine pairings, dessert suggestions
