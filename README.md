# Career Compass Bot

A conversational AI chatbot that helps users explore career paths across various fields including Science, Arts, Business, Engineering, Healthcare, Law, Education, Environment, Sports, and Social Sciences.

## Features

- **Interactive Career Exploration**: Navigate through different career fields and specializations
- **Comprehensive Career Information**: Get details about skills, daily tasks, salary ranges, education requirements, and job outlook for various roles
- **Natural Language Processing**: Ask questions about specific careers using natural language
- **Real-time Typing Effect**: Engaging conversation experience with typing animations
- **Responsive Design**: Clean, modern UI that works across different screen sizes

## Tech Stack

### Backend
- **Flask**: Python web framework for API endpoints
- **Flask-CORS**: Cross-origin resource sharing support
- **scikit-learn**: Machine learning for intent classification
- **pandas**: Data manipulation and analysis
- **joblib**: Model serialization

### Frontend
- **React**: JavaScript library for building user interfaces
- **Axios**: HTTP client for API requests
- **CSS-in-JS**: Inline styling for component design

## Project Structure

```
chatbot3/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── data.py               # Training data for NLP model
│   ├── train_model.py        # Script to train the intent classification model
│   ├── roles_data.json       # Detailed career information
│   ├── requirements.txt      # Python dependencies
│   ├── intent_model.joblib   # Trained NLP model (generated)
│   └── myvenv/              # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── index.js         # Entry point
│   ├── public/
│   │   └── index.html       # HTML template
│   └── package.json         # Node.js dependencies
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Setup and Activation of the virtual environment**:
   ```bash
   #Setup of venv
   python -m venv venv

   #Activation
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the NLP model** (if not already present):
   ```bash
   python train_model.py
   ```

5. **Start the Flask server**:
   ```bash
   python app.py
   ```

   The backend will be running on `http://127.0.0.1:5000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   # For newer Node.js versions that require legacy OpenSSL
   export NODE_OPTIONS=--openssl-legacy-provider && npm start
   
   # Or for Windows PowerShell
   $env:NODE_OPTIONS="--openssl-legacy-provider"; npm start
   
   # For standard setup (if no OpenSSL issues)
   npm start
   ```

   The frontend will be running on `http://localhost:3000`

## Usage

1. **Start the conversation**: The bot will greet you and ask about your field of interest
2. **Select a field**: Choose from options like Science, Arts, Business, etc.
3. **Choose a specialization**: Pick a specific area within your chosen field
4. **Explore careers**: View career suggestions and ask specific questions
5. **Ask detailed questions**: Inquire about skills, salary, education, job outlook, or daily tasks for any role

### Example Conversation Flow
```
Bot: Hey there! I'm here to help you explore career paths. What field are you interested in?
User: [Selects "Science"]
Bot: Great! Within Science, what specific area are you interested in? You can choose from: Coding, Physics, Biology, Chemistry, Mathematics, Earth science.
User: [Selects "Coding"]
Bot: For Coding within Science, you might consider careers like: Software Engineer, Web Developer, AI/ML Engineer, Full Stack Developer, Data Scientist, Blockchain Developer, Cybersecurity Analyst, Game Developer, DevOps Engineer, Cloud Architect, Mobile App Developer, Site Reliability Engineer. Is there a specific role you'd like to know more about?
User: "What skills do I need for Software Engineer?"
Bot: [Provides detailed skills information]
```

## API Endpoints

### POST /ask
Processes user messages and returns bot responses.

**Request Body**:
```json
{
  "message": "user input text",
  "field": "current selected field (optional)",
  "interest": "current selected interest (optional)"
}
```

**Response**:
```json
{
  "answer": "bot response text",
  "choices": ["array", "of", "options"] // optional
}
```

## Troubleshooting

### Common Issues

1. **scikit-learn version warnings**: 
   - These are compatibility warnings and don't affect functionality
   - To fix: Retrain the model with `python train_model.py`

2. **OpenSSL legacy provider error**:
   - Use the legacy provider flag when starting the frontend
   - `export NODE_OPTIONS=--openssl-legacy-provider && npm start`

3. **CORS errors**:
   - Ensure both backend (port 5000) and frontend (port 3000) are running
   - Check that Flask-CORS is properly installed

4. **Virtual environment issues**:
   - Make sure you're in the correct virtual environment
   - Reinstall dependencies if needed

### Development Notes

- The NLP model uses TF-IDF vectorization with Linear SVM for intent classification
- Career data is stored in both `app.py` (career_map) and `roles_data.json`
- The conversation flow prioritizes context-based matching over NLP predictions
- Debug logging is enabled in the backend for troubleshooting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- Add more career fields and roles
- Implement user authentication and conversation history
- Add career assessment questionnaires
- Include salary data by location
- Add career path recommendations based on user interests
- Implement voice interaction capabilities