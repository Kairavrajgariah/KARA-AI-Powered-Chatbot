# KARA-AI-Powered-Chatbot

# Restaurant Chatbot - Sattva🍽️

An intelligent restaurant ordering and tracking system built with modern web technologies. This project demonstrates a full-stack chatbot solution that enables customers to place orders through natural language processing and track their orders in real-time.

## 🚀 Key Features

Natural Language Processing: Integrated with Google Dialogflow for intelligent conversation handling
Real-time Order Tracking: Live order status updates for enhanced customer experience
Restaurant Management: Comprehensive order management system for restaurant operations
User-friendly Interface: Clean, responsive web interface for seamless customer interaction
Database Integration: Robust MySQL database for order and customer data management

## 🛠️ Technology Stack

Backend: FastAPI (Python) - High-performance web framework
Frontend: HTML, CSS - Responsive web interface
Database: MySQL - Relational database management
NLP: Google Dialogflow - Natural language understanding
API: RESTful APIs for seamless data communication
Deployment: Ngrok for local development and testing

## 📁 Project Structure
```
restaurant-chatbot/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── db_helper.py         # Database connection and queries
│   ├── generic_helper.py    # Utility functions and helpers
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html          # Web interface
├── database/
│   └── pandeyji_eatery.sql # Database schema and initial data
├── README.md
└── LICENSE
```
🔧 Installation & Setup
Prerequisites

Python 3.7+
MySQL Server
Ngrok
Google Dialogflow account

Step 1: Install Dependencies

bash
```
cd backend
```
```
pip install -r requirements.txt
```

Step 2: Database Setup

Import the database schema:

sqlmysql -u username -p < database/pandeyji_eatery.sql

Step 3: Configure Ngrok

bash
```
ngrok http 8000
```
Copy the generated HTTPS URL for Dialogflow configuration.

Step 4: Dialogflow Integration

Go to your Dialogflow console
Navigate to Fulfillment settings
Paste the ngrok HTTPS URL as the webhook URL

Step 5: Run the Application

bash
```
cd backend
```
```
uvicorn main:app --reload
```
The application will be available at http://localhost:8000

## 💡 How It Works

Customer Interaction: Users interact with the chatbot through natural language
Intent Recognition: Dialogflow processes user inputs and identifies intents
Order Processing: Backend handles order creation, validation, and database storage
Real-time Updates: Customers receive live updates on their order status
Restaurant Management: Restaurant staff can manage and track all orders efficiently

## 🎯 Key Achievements

Intelligent Conversation Flow: Implemented context-aware dialogues for natural ordering experience
Scalable Architecture: Built with FastAPI for high performance and scalability
Real-time Tracking: Developed live order tracking system improving customer satisfaction
Database Optimization: Designed efficient MySQL schema for order and customer management
Cross-platform Compatibility: Responsive design works across all devices

## 📊 Business Impact

Enhanced Customer Experience: Streamlined ordering process with natural language interface
Operational Efficiency: Automated order management reduces manual work
Real-time Visibility: Live tracking improves customer satisfaction and reduces support queries
Scalable Solution: Architecture supports growth and additional features

## 🔮 Future Enhancements

Integration with payment gateways
Multi-language support
Voice-based ordering
Mobile application
Analytics dashboard for restaurant insights

## 📝 Technical Skills Demonstrated

Backend Development: FastAPI, Python, RESTful APIs
Database Management: MySQL, Database design, Query optimization
NLP Integration: Google Dialogflow, Intent recognition, Context management
Frontend Development: HTML, CSS, Responsive design
DevOps: Local deployment, API integration, Testing
Problem Solving: Real-time systems, User experience optimization

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any improvements.
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Project Highlights for Resume:

Built intelligent restaurant chatbot using Google Dialogflow and FastAPI
Implemented real-time order tracking system with MySQL database
Designed scalable backend architecture serving RESTful APIs
Created responsive web interface for seamless customer experience
Demonstrated full-stack development skills with modern technologies
