# Authors
Jakub Pobłocki | Kacper Pecka

# 🎬 Movie Recommendation and Anti-Recommendation System

This project is a personalized movie recommendation system that leverages clustering algorithms to analyze user similarities.  
The system takes a JSON database with user profiles and recommends movies based on the preferences of users with similar tastes.  
Additionally, it generates "anti-recommendations" for movies that are popular among users with distinctly different preferences.

## How It Works 🚀
- **Data Loading** – The system imports user data from a JSON database containing movie ratings and individual preferences.
- **Preference Comparison** – The system uses clustering algorithms (e.g., K-means) to analyze the calling user’s profile and compare it with others in the database to determine similarity.
- **Recommendations & Anti-Recommendations** – Based on the clustering results, the system outputs:
   - A list of 5 recommended movies (from the most similar user).
   - A list of 5 anti-recommended movies (from the most different user).

## User Interface in Pygame 🎮

The user interface consists of the following elements:

1. **Dropdown list of users** – The user can select one of the available users from the dropdown list to load their data and recommendations.
2. **Buttons:**
   - **"V"** – When pressed, only recommendations for the selected user will be displayed.
   - **"X"** – When pressed, only anti-recommendations for the selected user will be displayed.
   - **"B"** – When pressed, both recommendations and anti-recommendations for the selected user will be displayed.

3. **Movie Cards** – After the data is fetched, recommendations and anti-recommendations are displayed in the form of movie cards. Each card contains:
   - **Movie poster** – The poster is fetched once and saved to a temporary folder, so there's no need to fetch it again.
   - **Movie title** – Displayed next to the poster.
   - **Director and year of production** – Displayed below the title, providing more information about the movie.

## Optimized Functionality in Pygame

The system runs in the Pygame environment, providing interactive display of the movie data card. Key functional elements include:

- **Fetching movie posters**: Posters are fetched only once for the selected user and stored in a temporary folder. Once a new user is selected, new posters for their recommendations are fetched.
- **Efficient management of movie cards**: Movie cards with posters are displayed dynamically. If a movie does not have a poster available, a default poster ("default-movie.jpg") is shown.

## Example of what the system looks like
[Watch the demo video](https://youtu.be/oKf95yz9ZeM)

## Prerequisites
- Ensure that Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

You can install the required libraries using the command:  

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
