# LLM and RAG-Powered Accommodation Recommendation System

## Overview

This project is an advanced tourism recommendation system that utilizes open datasets from **Booking.com** to provide personalized accommodation suggestions based on users' natural language queries and detailed preferences.  
The system combines a **Retrieval-Augmented Generation (RAG)** architecture for semantic search, user-specific contextual re-ranking mechanisms, and **Large Language Models (LLM)** to justify its recommendations.

The system leverages two fundamental datasets:
1. **Behavioral Dataset**: Over 1.16 million reservation records containing users' booking habits in multi-destination trips.
2. **Textual Dataset**: Over 1.6 million hotel reviews reflecting users' opinions about their accommodation experiences.

By combining these two datasets, a holistic recommendation engine has been created that understands not only **"what"** is liked, but also **"why"** and **"by whom"**.

---

## System Architecture

The project adopts a modern client-server model for its web application architecture.

### 1. Backend (Python & Flask) — The Recommendation Engine

The heart of the system is a Python-based **Flask API**. This API executes a complex **RAG-based pipeline** to generate recommendations.

- **Data Loading and Caching**: To enhance performance, processed reviews, vector embeddings, and relational data are cached using `pickle` and `numpy` files.
- **Pre-filtering**: The pool of potential accommodations is narrowed down based on structured preferences entered by the user (e.g., accommodation type, star rating, country, location features).

#### Semantic Search (Retrieval)
- **Embedding**: All hotel reviews are converted into semantic vectors using the `all-MiniLM-L6-v2` model.
- **Similarity Search**: The user's query is also vectorized, and the most relevant reviews are found at high speed using `FAISS` (Facebook AI Similarity Search).

#### Advanced Re-ranking
- **Review Helpfulness**: `review_helpful_votes` are logarithmically scaled.
- **Aspect-Based Sentiment Analysis (ABSA)**: Implicit expectations like `"quiet room"` or `"good breakfast"` are identified using `PyABSA`.
- **Contextual Matching**: Factors like `guest_type`, `guest_country`, `month`, and `room_nights` are used to match historical performance.

#### Generation with Large Language Model
- The top re-ranked reviews and accommodation details are passed to the `deepseek-r1:1.5b` model running on **Ollama**.
- The LLM generates human-readable explanations for recommendations.

---

### 2. Frontend (React & Ant Design) — User Interface

A modern and reactive web interface where users interact with the system.

- **Technology**: Developed using `React` and `Vite`. Uses the `Ant Design` library for UI components.
- **Functionality**: Supports a wide range of filters — accommodation type, star rating, country, location preferences (beach, ski, downtown), guest profile, travel details, plus a natural language input.
- **Interaction**: When submitted, a request is sent to the backend, and results are displayed as structured, user-friendly cards.

---

## Key Features

✅ **Natural Language Understanding** — Handles complex queries like *"family-friendly hotel near a pool."*  
✅ **Multi-faceted Filtering** — Combines structured + semantic filters.  
✅ **Context-Aware Recommendations** — Uses guest type, travel time, and user history.  
✅ **Aspect-Based Sentiment Analysis (ABSA)** — Focuses on aspects like cleanliness, staff, location.  
✅ **Behavioral Persona Integration** — Uses historical booking patterns for personalization.  
✅ **Explainable AI (XAI)** — Explains why a hotel is recommended.  
✅ **Interactive UI** — Built with `React` + `Ant Design` for easy, intuitive use.

---

## Technical Implementation Details

- **Backend**: Flask, Sentence-Transformers, PyABSA, Faiss, Ollama, Pandas, Numpy  
- **Frontend**: React, TypeScript, Vite, Ant Design, Tailwind CSS

### Models
- Embedding → `all-MiniLM-L6-v2` (semantic similarity)  
- ABSA → `ATEPCCheckpointManager` (aspect-based sentiment)  
- Generation → `deepseek-r1:1.5b` (via Ollama)

### Datasets
- `booking_train.csv`: 1.16M reservations  
- `booking_reviews.csv`: 1.6M reviews

---

## Setup and Execution

Follow the steps below to run the project on your local machine.

### Requirements

- Python 3.9+ and pip  
- Node.js and npm  
- **Ollama** installed, with `deepseek-r1:1.5b` model pulled locally:
  
```bash
ollama pull deepseek-r1:1.5b

1. Backend Setup

# Clone the repository and navigate to backend
cd backend/

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server (default port: 5001)
python main.py

2. Frontend Setup

# Navigate to frontend
cd frontend/

# Install Node.js packages
npm install

# Start the development server
npm run dev

The app will be available at → http://localhost:5173 (or another port assigned by Vite).
