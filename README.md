# ai-nurse-companion

## Overview
The Agentic AI for Smart Health Triage (AI Nurse Companion) is designed to assist users in evaluating their health symptoms through conversational AI. By leveraging the Gemini API, the application provides preliminary analyses, urgency levels, and lifestyle suggestions based on user input.

## Features
- User symptom input via text and voice.
- Clarifying questions to gather more information.
- Preliminary analysis of symptoms.
- Urgency level determination.
- Lifestyle suggestions for better health management.
- Integration with Google Fit API for personalized health insights.

## Project Structure
```
ai-nurse-companion
├── src
│   ├── api
│   ├── core
│   ├── models
│   └── utils
├── tests
├── frontend
├── config
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-nurse-companion.git
   cd ai-nurse-companion
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in the `.env` file.

## Usage
- Start the backend server:
  ```bash
  python -m src.api.main
  ```

- Run the frontend application:
  ```bash
  cd frontend
  npm install
  npm start
  ```

## Testing
To run the tests, use:
```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.