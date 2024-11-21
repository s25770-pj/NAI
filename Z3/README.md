# Authors 
Jakub Pobłocki |  Kacper Pecka

# 🎬 Movie Recommendation and Anti-Recommendation System

This project is a personalized movie recommendation system that leverages clustering algorithms to analyze user similarities.
The system takes a JSON database with user profiles and recommends movies based on the preferences of users with similar tastes.
Additionally, it generates "anti-recommendations" for movies that are popular among users with distinctly different preferences.

## How It Works 🚀
- Data Loading – The system imports user data from a JSON database, containing movie ratings and individual preferences.
- Preference Comparison – Using clustering algorithms (such as K-means), the system analyzes the calling user’s profile and compares it with others in the database to determine similarity.
- Recommendations & Anti-Recommendations – Based on the clustering results, the system outputs a list of 5 recommended movies (from the most similar user) and 5 anti-recommended movies.

## An example of what the system looks like
[Watch the demo video](https://youtu.be/cHLMgfb8OpE)

## Prerequisites
- Ensure that Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).


You can install the required libraries using the command:
Firstly you have to create and activate virtual environment.
Before running the command, navigate to the `Z3` directory.

```bash
pip install -r requirements.txt
```

## Cloning the Repository
To get started with the program for film advising and dissuading, you need to clone the repository. Use the following command in your terminal:

```git clone https://github.com/s25770-pj/NAI_CHOMP.git```

### Running the Program
1. **Open a Terminal**:
   - Navigate to the directory where you cloned the repository.
   - Go to Z3 dictionary.

2. **Run the Program**:
   - Use the command `python main.py` to start the program.
