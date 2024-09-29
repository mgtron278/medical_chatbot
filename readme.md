# Medical Chatbot

A Django-based medical chatbot that interacts with patients, handles appointment rescheduling requests, and integrates with a Neo4j knowledge graph for storing and retrieving patient information.

## Features
- **Patient Medical Information**: Retrieves and stores patient medical data.
- **Entity Extraction**: Utilizes OpenAI GPT for extracting entities related to medication, medical conditions, etc.
- **Conversation Management**: Maintains conversation history using LangChain.
- **Knowledge Graph**: Integrates with Neo4j Aura Cloud for storing and retrieving patient-related entities.

## Tech Stack
- **Backend**: Django
- **Database**: PostgreSQL 16.4-1 (Local)
- **Knowledge Graph**: Neo4j Aura Cloud
- **AI Integration**: OpenAI GPT (Version: 0.28), LangChain
- **Memory Handling**: ConversationBufferMemory (LangChain)
- **Python Version**: 3.10.9

## Prerequisites
- [PostgreSQL 16.4-1](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) installed locally
- [Python 3.10.9](https://www.python.org/downloads/release/python-3109/) installed
- Neo4j Aura Cloud account (for knowledge graph storage) or use the provided credentials
- OpenAI API Key (Version: 0.28)
- pgAdmin 4 (to manage PostgreSQL database)
- SQL scripts provided in the repository:
  - `sqlsetup.py`: Script to create the database, user, and set permissions.
  - `patient.py`: Script to add patient details to the database.

## API Keys and Neo4j Cloud Access
- **API Keys**: Ensure you have received all necessary API keys via email before setting up the project.
- **Neo4j Cloud**: You can either log in to the provided Neo4j Aura Cloud account using the credentials shared via email or create your own account by following the steps below.

### How to Create a Neo4j Aura Cloud Account

1. **Sign Up**:
   - Go to [Neo4j Aura Cloud](https://console.neo4j.io/) and sign up for a free account.

2. **Create a New Database**:
   - Once logged in, click on **Create a Free Database**.
   - Follow the on-screen instructions to set up a new Aura database.

3. **Obtain Connection Details**:
   - After the database is created, you’ll be provided with a connection URI, a username, and a password (a `.txt` file with credentials will be downloaded as soon as you create an instance). Note down these credentials as they will be used in your `.env` file for connecting to the database.

4. **Update Your `.env` File**:
   - If you choose to use your own Neo4j account, update the `.env` file in the project root directory with the following:
     ```bash
     NEO4J_URI=<your-uri>
     NEO4J_USERNAME=<your-username>
     NEO4J_PASSWORD=<your-password>
     ```

## Setup Instructions


### 1. Clone the Repository
```bash
git clone <repository-url>
cd project-directory
```

### 2. Create a Virtual Environment with Python 3.10.9
To avoid dependency issues and ensure the smooth flow of the project, create a virtual environment with Python 3.10.9:

#### On macOS/Linux:
```bash
python3.10 -m venv env
source env/bin/activate
```

#### On Windows:
```bash
python -m venv env
.\env\Scripts\activate
```

After activating the virtual environment, proceed to install the dependencies.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and Configure pgAdmin 4
- **Install pgAdmin 4**: Download and install [pgAdmin 4](https://www.pgadmin.org/download/) suitable for your operating system.
- **Set Up PostgreSQL Password**: During PostgreSQL installation, you set a password for the `postgres` user. Ensure you remember this password as it will be needed in subsequent steps.

### 5. Load API Keys into `.env` File
Before running migrations, ensure that all necessary API keys are loaded into the `.env` file.

1. **Create/Edit a `.env` File**:
   
   - You already have a `.env` file, edit it with the credentials provided via email.

2. **Add API Keys and Database Credentials**:
   - Open the `.env` file and add the following entries:
     ```bash
     # OpenAI API Key
     OPENAI_API_KEY=<your-openai-api-key>

     # Neo4j Credentials
     NEO4J_URI=<your-uri>
     NEO4J_USERNAME=<your-username>
     NEO4J_PASSWORD=<your-password>

     ```
   - **Note**: Replace `<your-...>` placeholders with your actual credentials. Ensure that the PostgreSQL credentials match those you set during installation.

### 6. Execute SQL Scripts to Setup Database and Add Patient Data

1. **Run `sqlsetup.py` Script**:
   - This script will create the necessary database, user, and assign appropriate permissions.
   - Execute the script using Python:
     ```bash
     python sqlsetup.py
     ```
   - Ensure that Pgadmin4 is running and "postgresql 16" server is available. The script will use the credentials provided in the `.env` file.

2. **Run Migrations**:
   - Apply Django migrations to set up the database schema.
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Run `patient.py` Script to Add Patient Details**:
   - This script will populate the database with initial patient data.
     ```bash
     python patient.py
     ```

### 7. Run the Application
```bash
python manage.py runserver
```

### 8. Access the Application
- Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage
- Start a conversation by selecting a patient and interacting with the chatbot.
- The chatbot can handle appointment rescheduling requests and provide information based on the stored medical data.

## Working Flow

The Medical Chatbot enables seamless patient interactions by integrating Django, LangChain, OpenAI GPT, and Neo4j. Here's a concise overview of its workflow:

1. **Chat Initialization**:
   - Patient accesses the chat interface .

2. **Loading Patient Data**:
   - Retrieves patient details from PostgreSQL.
   - Provides context for the conversation.

3. **Handling User Messages**:
   - **Intent Recognition**: Determines if the message is a question or appointment request.
   - **Entity Extraction**: Extracts relevant information using OpenAI GPT.
   - **Knowledge Graph Interaction**:
     - Stores extracted entities in Neo4j.
     - Retrieves information from Neo4j if needed.

4. **Generating Responses**:
   - Uses LangChain’s `LLMChain` with a prompt template to craft responses.
   - Maintains conversation history for context.

5. **Conversation Management**:
   - Saves both user and AI messages in PostgreSQL.
   - Summarizes interactions and updates the session summary.


### Key Components

- **Django Backend**: Manages requests and serves the chat interface.
- **PostgreSQL**: Stores patient information and conversation logs.
- **Neo4j**: Handles and retrieves patient-related entities.
- **LangChain & OpenAI GPT**: Powers the AI-driven interactions.
- **Session Management**: Maintains conversation summaries.

This streamlined workflow ensures efficient handling of patient interactions, accurate responses, and comprehensive record-keeping to enhance user experience.

## Troubleshooting

- **Script Execution Errors**:
  - Make sure you are operating within the activated virtual environment.
  - Ensure all dependencies are installed correctly via `pip install -r requirements.txt`.

- **API Key Issues**:
  - Double-check that the OpenAI API key is correctly set in the `.env` file.

- **Neo4j Connection Issues**:
  - Verify the Neo4j connection details in the `.env` file.
  - Ensure that the Neo4j database is accessible and not restricted by firewall rules.



## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

