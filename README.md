# 📚 AutoRevise - Intelligent Spaced Repetition Learning System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

> A web-based flashcard system powered by the SM-2 spaced repetition algorithm, designed to help students optimize their learning and retention.

## 🌟 Overview

AutoRevise is an intelligent learning platform that combines flashcards and multiple-choice questions (MCQs) with gamification elements to create an engaging study experience. Built with Flask and MySQL, it uses the scientifically-proven SM-2 algorithm to schedule reviews at optimal intervals for maximum retention.

## ✨ Key Features

### 🎴 Smart Flashcard System
- **SM-2 Algorithm**: Scientifically-proven spaced repetition scheduling
- **Custom Decks**: Organize cards by subject or topic
- **Bulk Import**: Upload flashcards via CSV files
- **Progress Tracking**: Monitor learning progress for each card
- **Four Difficulty Ratings**: Forgot, Hard, Good, Easy

### 📝 MCQ Practice Module
- **Category-Based Questions**: Organize by subject and difficulty
- **Instant Feedback**: Get explanations for correct/incorrect answers
- **Performance Analytics**: Track accuracy and progress over time
- **Admin Upload System**: Bulk upload questions via CSV

### 🏆 Gamification & Achievements
- **24 Unique Badges**: Unlock achievements as you progress
- **Points System**: Earn rewards for consistent studying
- **Streak Tracking**: Build daily study habits
- **Motivational Messages**: Stay encouraged throughout your journey

### 📊 Analytics Dashboard
- **Study Statistics**: Visualize your learning patterns
- **Performance Metrics**: Cards reviewed, accuracy rates, time invested
- **Progress Charts**: Track improvement over time
- **Streak Calendar**: Never lose your momentum

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **MySQL 8.0+** server running
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shaikh-Anas00/AutoRevise.git
   cd AutoRevise
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd Backened
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your database credentials
   # Required settings:
   # - DB_PASSWORD: Your MySQL password
   # - SECRET_KEY: Generate a random secret key
   ```

5. **Set up the database**
   ```bash
   # Login to MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE autorevise_db;
   USE autorevise_db;
   
   # Run schema files in order
   SOURCE schema2.sql;
   SOURCE schema_mcq_update.sql;
   SOURCE schema_mcq_categories.sql;
   SOURCE schema_performance_indexes.sql;
   
   # OR use the Python setup scripts
   python run_mcq_schema_safe.py
   python run_mcq_categories_schema.py
   ```

6. **Run the application**
   ```bash
   python App1.py
   ```

7. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage Guide

### Getting Started

1. **Register an Account**
   - Navigate to the registration page
   - Create your account with username, email, and password
   - Passwords are securely hashed with bcrypt

2. **Create Your First Deck**
   - Click "Create New Deck" on the dashboard
   - Give it a name and description
   - Add flashcards manually or import from CSV

3. **Start Studying**
   - Click "Study Now" on any deck
   - Review cards and rate your recall:
     - **Forgot (Again)**: Card reappears tomorrow
     - **Hard**: Short review interval
     - **Good**: Standard SM-2 interval
     - **Easy**: Extended interval

4. **Practice MCQs**
   - Navigate to MCQ Practice from dashboard
   - Select a category or link MCQs to your decks
   - Answer questions and get instant feedback

### CSV Import Format

**Flashcards CSV:**
```csv
front,back
What is Python?,A high-level programming language
Define API,Application Programming Interface
```

**MCQs CSV:**
```csv
question,option_a,option_b,option_c,option_d,correct_answer,explanation,difficulty,category
What is 2+2?,2,3,4,5,C,Basic arithmetic,Easy,Mathematics
```

## 🏗️ Project Structure

```
AutoRevise/
├── Backened/                    # Flask backend
│   ├── App1.py                  # Main application
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── schema2.sql              # Main database schema
│   ├── schema_mcq_update.sql    # MCQ tables
│   ├── schema_mcq_categories.sql
│   ├── schema_performance_indexes.sql
│   ├── run_mcq_schema_safe.py   # Schema setup scripts
│   ├── run_mcq_categories_schema.py
│   ├── make_admin.py            # Admin utility
│   └── sample_mcqs.csv          # Sample data
│
├── Frontened 1/                 # Frontend files
│   ├── index.html               # Landing page
│   ├── login-page.html
│   ├── register-page.html
│   ├── dashboard-connected.html # Main dashboard
│   ├── deck-view.html
│   ├── study-session.html
│   ├── mcq-practice.html
│   ├── achievements.html
│   ├── admin-mcq-upload.html
│   │
│   ├── css/                     # Stylesheets
│   │   ├── style.css
│   │   ├── auth.css
│   │   ├── dashboard.css
│   │   ├── deck-view.css
│   │   ├── study-session.css
│   │   └── achievements.css
│   │
│   └── js/                      # JavaScript files
│       ├── config.js            # API configuration
│       ├── api-app1.js          # API client
│       ├── dashboard-connected.js
│       ├── deck-view-connected.js
│       ├── study-session-connected.js
│       ├── achievements-connected.js
│       └── mcq-integration-example.js
│
├── Documentation/               # Project documentation
│   ├── COMPLETE_PROJECT_DOCUMENTATION.md
│   ├── PROJECT_WORKING_PROCESS_AND_METHODOLOGY.md
│   └── ... (additional docs)
│
├── sample_*.csv                 # Sample data files
├── .gitignore
└── README.md
```

## 🛠️ Technology Stack

**Backend:**
- **Flask 3.0** - Python web framework
- **MySQL 8.0** - Relational database
- **bcrypt** - Password hashing
- **python-dotenv** - Environment management
- **Flask-CORS** - Cross-origin resource sharing

**Frontend:**
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox/Grid
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - Asynchronous HTTP requests

**Algorithms:**
- **SM-2 Spaced Repetition** - Optimal review scheduling
- **Achievement System** - Gamification logic
- **Streak Calculation** - Habit tracking

## 🔐 Security Features

- **Password Hashing**: bcrypt with cost factor 12
- **Session Management**: Secure cookie-based authentication
- **CORS Protection**: Configured allowed origins
- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: Server-side validation
- **Environment Variables**: Sensitive data in .env files

## 📚 Documentation

Comprehensive documentation available in the `/Documentation` folder:

- **[Complete Project Documentation](Documentation/COMPLETE_PROJECT_DOCUMENTATION.md)** - Full technical details
- **[Working Process & Methodology](Documentation/PROJECT_WORKING_PROCESS_AND_METHODOLOGY.md)** - Development approach
- **[SQL Queries Explained](Documentation/SQL_QUERIES_EXPLAINED.md)** - Database operations
- **[Query Optimization Guide](Documentation/QUERY_OPTIMIZATION_AND_INDEXING.md)** - Performance tuning
- **[Troubleshooting Guide](Documentation/TROUBLESHOOTING_500_ERRORS.md)** - Common issues

## 🎯 Features in Detail

### SM-2 Algorithm Implementation

The system calculates the next review date based on:
- **Easiness Factor (EF)**: Adjusted based on recall quality
- **Repetition Number**: How many times you've reviewed
- **Interval**: Days until next review

```python
# Simplified logic
if rating == "Easy":    EF increases, longer interval
if rating == "Good":    Standard interval
if rating == "Hard":    EF decreases, shorter interval
if rating == "Forgot":  Reset to day 1
```

### Achievement System

Unlock badges by:
- **Study Consistency**: Daily streaks (3, 5, 7, 30, 100 days)
- **Volume Milestones**: Cards reviewed (50, 100, 500)
- **Time Investment**: Study hours (1, 10+ hours)
- **Points Earned**: Cumulative points (1K, 2K, 5K, 10K)
- **Deck Creation**: Building your library
- **Special Achievements**: Early bird, Night owl, etc.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation if needed

## 🐛 Known Issues & Limitations

- Frontend and backend must run on same domain (127.0.0.1) for cookies
- Session cookies require browser refresh after login on some setups
- MCQ categories require manual assignment to decks
- Mobile responsiveness needs improvement

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Collaborative decks (share with friends)
- [ ] Image support in flashcards
- [ ] Audio pronunciation
- [ ] Dark mode theme
- [ ] Export/import deck bundles
- [ ] Leaderboards and social features
- [ ] AI-generated flashcards
- [ ] Offline mode with sync


**Built with ❤️ for students who want to study smarter, not harder.**

*Last Updated: December 2025*

