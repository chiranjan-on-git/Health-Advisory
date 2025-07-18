# Health Advisory

Your Personal Public Health Advisory Assistant

Health Advisory is a web application that helps you quickly find the top 5 most relevant and current official public health advisories issued by government or public health authorities for a specified state and country. It leverages the power of Perplexity AI to retrieve timely and summarized information.

<p align="center">
  <img src="https://github.com/user-attachments/assets/877a1938-df1d-4d06-96c0-db9e42228cb6" width="400" alt="image" />
</p>

## Features

*   **Location-Based Advisories:** Get health advisories specific to a `State, Country` format.
*   **AI-Powered Summaries:** Utilizes Perplexity AI's online models to fetch and summarize official advisories.
*   **Latest Information:** Focuses on advisories issued or updated within the last 30 days.
*   **Clear & Concise Output:** Presents information as structured bullet points, including the date, issuing agency, and a summary.
*   **User-Friendly Interface:** Simple HTML/CSS/JS frontend for easy interaction.
*   **Theme Toggle:** Switch between light and dark modes for comfortable viewing.
*   **Robust Error Handling:** Provides clear messages for API issues, invalid input, or no advisories found.

## Technologies Used

### Backend (FastAPI - Python)

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn:** An ASGI server for running FastAPI applications.
*   **Requests:** For making HTTP requests to the Perplexity AI API.
*   **Pydantic:** Data validation and settings management using Python type hints.
*   **python-dotenv:** For loading environment variables from a `.env` file.
*   **Logging:** Built-in Python logging for application insights.

### Frontend (HTML, CSS, JavaScript)

*   **HTML5:** Structure of the web application.
*   **CSS3:** Styling and theme management (light/dark mode).
*   **JavaScript (Vanilla JS):** Handles user interaction, API calls (`fetch` API), and dynamic content updates.
*   **Font Awesome:** For icons (e.g., theme toggle).

### AI Service

*   **Perplexity AI (API):** Specifically using models like `sonar-pro` to access up-to-date information from the web and summarize it.

## Project Structure

<img src="https://github.com/user-attachments/assets/cc0c6bb8-74e5-427a-8f78-f484129a5f07" width="300" alt="image"/>

## Setup and Installation

Follow these steps to set up and run Health Advisory locally.

### 1. Prerequisites

*   **Python 3.8+:** Make sure Python is installed on your system.
*   **Perplexity AI API Key:** You will need an API key from [Perplexity AI](https://www.perplexity.ai/settings/api).

### 2. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd Health-Advisory/backend
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    First, create a `requirements.txt` file in the `backend/` directory with the following content:
    ```
    fastapi
    uvicorn[standard]
    requests
    python-dotenv
    pydantic
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Perplexity API Key:**
    Create a file named `.env` in the `backend/` directory (next to `app.py`) and add your Perplexity AI API key:
    ```dotenv
    PERPLEXITY_API_KEY="your_perplexity_api_key_here"
    ```
    **Important:** Replace `"your_perplexity_api_key_here"` with your actual key. Do not share this key publicly.

### 3. Frontend Setup

The frontend is built with plain HTML, CSS, and JavaScript, so no specific installation steps are required beyond having a web browser.

## How to Run

### 1. Start the Backend Server

1.  Ensure your virtual environment is active (from Backend Setup step 3).
2.  From the `Health-Advisory/backend` directory, run the FastAPI application using Uvicorn:
    ```bash
    uvicorn app:app --reload --host 0.0.0.0 --port 5001
    ```
    You should see output indicating that the server is running, typically on `http://127.0.0.1:5001` or `http://localhost:5001`.

### 2. Open the Frontend Application

1.  Navigate to the `Health-Advisory/frontend` directory.
2.  Open the `index.html` file in your web browser.
    *   You can usually do this by double-clicking the `index.html` file.
    *   **Recommended:** For better local development experience (especially with CORS), use a local server extension for your code editor (e.g., "Live Server" for VS Code). This typically serves the page on `http://127.0.0.1:5500`.

    **Note on CORS:** The backend `app.py` is configured to allow requests from `http://127.0.0.1:5500` (common for Live Server), `http://localhost:3000`, `http://localhost:5173`, etc. If you're running your frontend on a different port, you might need to add that origin to the `origins` list in `app.py`.

## Usage

1.  Once the frontend is open in your browser, you will see an input field labeled "Enter State, Country".
2.  **Enter a location** in the format `State, Country` (e.g., `California, United States` or `Maharashtra, India`).
3.  Click the **"Get Advisories"** button.
4.  The application will display "Loading..." while fetching data.
5.  If successful, the top 5 medical advisories will appear. If no advisories are found for the last 30 days, a specific message will be shown.
6.  You can also use the **theme toggle button** (sun/moon icon) in the header to switch between light and dark themes.

## Error Handling

*   **Missing API Key:** The backend will return a 500 error if `PERPLEXITY_API_KEY` is not configured.
*   **Invalid Location Format:** If the location input is not in the `State, Country` format, a 400 error will be returned.
*   **Perplexity API Issues:** Network errors or errors from the Perplexity API (e.g., rate limits, invalid requests) will be caught and displayed with a 503 (Service Unavailable) error.
*   **No Advisories Found:** If the AI model genuinely cannot find relevant advisories for the given location and criteria, it will explicitly state that "No relevant official medical advisories were found...".

## Future Enhancements

*   **Autocomplete for Location:** Implement a location search API (e.g., Google Places API) for more accurate and user-friendly input.
*   **More Granular Filtering:** Allow users to filter advisories by date range, specific keywords, or issuing agency.
*   **Backend Caching:** Implement caching for frequent requests to reduce API calls and improve response times.
*   **Deployment Guides:** Add instructions for deploying the application to cloud platforms (e.g., Heroku, Render, AWS, Azure).
*   **Dockerization:** Provide Dockerfiles for easy containerization and deployment.
*   **User Interface Improvements:** Enhance responsiveness, add animations, or integrate a more robust UI framework.
---
