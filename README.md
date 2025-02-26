# meetkadence

A "reverse CRM" that helps users nurture valuable relationships directly from their email inbox through AI-enhanced, fully-baked message suggestions.

## Overview

meetkadence is designed to help professionals maintain and grow relationships through consistent, high-value communication. Instead of traditional CRM management, it pushes suggested outreach messages directly to your inbox.

### Key Features

- Email-centric workflow
- Category-based contact management
- AI-powered message suggestions
- Customizable outreach cadences
- Personal rules and instructions per contact

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
meetkadence/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md             # This file
├── models/               # Data models and schemas
│   └── schemas.py        # Pydantic models
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── sample_data.py    # Sample data generation
│   └── helpers.py        # Helper functions
└── pages/               # Streamlit pages
    ├── contacts.py      # Contact management
    ├── categories.py    # Category management
    └── settings.py      # System settings
```

## Contributing

This is a prototype version focusing on UX/UI demonstration. Core functionality like email integration and LLM integration are simulated for demonstration purposes. 