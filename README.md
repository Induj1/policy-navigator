# Policy Navigator

## Overview
The Policy Navigator is a full-stack application designed to assist citizens in interpreting government policies, verifying eligibility for benefits, and matching them with suitable programs. It utilizes a multi-agent AI system to streamline these processes, ensuring accurate and efficient service delivery.

## Tech Stack
- **Backend**: 
  - FastAPI
  - Python 3.10+
  - Pydantic
  - Uvicorn
  - p3ai-agent==0.1.0 (Zynd / P3 protocol)
  - langchain-openai

- **Frontend**: 
  - Next.js 14 (App Router)
  - TypeScript
  - TailwindCSS

## Folder Structure
The project is organized into two main directories: `backend` and `frontend`.

### Backend
- `app/`: Contains the main application logic, including routes, agents, and schemas.
- `infra/`: Contains infrastructure-related code, including the P3 client.
- `requirements.txt`: Lists the required Python packages.
- `.env.example`: Example environment configuration.
- `pyproject.toml`: Project metadata and dependencies.

### Frontend
- `app/`: Contains the Next.js application pages.
- `components/`: Contains reusable UI components.
- `lib/`: Contains API utility functions.
- Configuration files for npm, TypeScript, TailwindCSS, and PostCSS.

## Setup Instructions

### Backend
1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Run the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install the dependencies:
   ```
   npm install
   ```
3. Start the Next.js application:
   ```
   npm run dev
   ```

## Usage
- Visit the landing page to navigate to different sections of the application.
- Use the citizen page to input income and state to check eligibility for benefits.
- Use the policies page to interpret policy text and view extracted rules.
- Use the benefits page to see matched policies based on eligibility.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.