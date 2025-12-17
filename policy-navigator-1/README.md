# Policy Navigator

## Overview
Policy Navigator is a multi-agent AI system designed to assist with government policy interpretation, eligibility verification using verifiable credentials, and benefit matching. The application leverages advanced AI techniques to provide users with accurate and timely information regarding government policies and benefits.

## Features
- **Policy Interpretation**: Analyze and interpret complex government policies to extract structured rules.
- **Eligibility Verification**: Validate citizen credentials against policy rules to determine eligibility for benefits.
- **Benefit Matching**: Match citizens with a list of eligible policies based on their credentials and needs.

## Architecture
The project is structured into two main components: the backend and the frontend.

### Backend
The backend is built using FastAPI and includes:
- **Agents**: Responsible for interpreting policies, verifying eligibility, and matching benefits.
- **API**: Exposes endpoints for frontend interaction.
- **Models**: Defines data structures for policies, credentials, benefits, and user profiles.
- **Services**: Contains business logic for handling policies and credentials.
- **Database**: Manages data storage and retrieval.

### Frontend
The frontend is developed using Next.js and includes:
- **Pages**: User interfaces for policy interpretation, eligibility checking, and benefit matching.
- **Components**: Reusable UI components for building the application.
- **Hooks**: Custom hooks for managing state and API interactions.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js and npm
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd policy-navigator
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies using Poetry:
     ```
     poetry install
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies using npm:
     ```
     npm install
     ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` in the `backend` directory and fill in the required values.

### Running the Application

- To start the backend, run:
  ```
  poetry run start
  ```

- To start the frontend, run:
  ```
  npm run dev
  ```

### Docker Deployment
To run the application using Docker, use the provided `docker-compose.yml` file:
```
docker-compose up
```

## Testing
To run tests for the backend, navigate to the `backend` directory and run:
```
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.