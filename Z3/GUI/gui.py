from idlelib.configdialog import changes

import pygame
import requests
import asyncio
from GUI.button import Button

# Initialize Pygame
pygame.init()

# OMDB API key
api_key = "da2b34ef"
#api_key = ""
CARD_CONTENT_OFFSET = 10
card_content_offset = CARD_CONTENT_OFFSET
display_recommend = (1, 1, 1)
screen_width = 800
screen_height = 600
CARD_HEIGHT = 200
card_height = CARD_HEIGHT
CARD_OFFSET = 40
card_offset = CARD_OFFSET
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Movie Recommendation System')
max_scroll_offset = 0
scroll_offset = 0

font = pygame.font.SysFont('Arial', 15)
font_button = pygame.font.SysFont('Arial', 20)

# Cache for storing movie data per user
user_movie_data_cache = {}
current_user = None  # Track the currently selected user

def search_film_by_title(title, api_key=api_key):
    """
    Fetches movie data from the OMDB API based on the given title.
    Args:
        title (str): Title of the movie to search for.
        api_key (str): API key for accessing OMDB.
    Returns:
        dict: Response data from OMDB API as a dictionary.
    """
    r = requests.get(f'http://www.omdbapi.com/?apikey={api_key}&t={title}')
    return r.json()

def render_text(text, x, y, color=(255, 255, 255), font=font):
    """
    Renders text on the Pygame screen at the specified position.
    Args:
        text (str): The text to render.
        x (int): X-coordinate of the text position.
        y (int): Y-coordinate of the text position.
        color (tuple): RGB color of the text.
        font (pygame.font.Font): Font to use for rendering.
    """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def display_poster(image_path, x, y):
    """
    Displays a poster image at the specified position on the screen.
    Args:
        image_path (str): Path to the image file.
        x (int): X-coordinate of the poster's position.
        y (int): Y-coordinate of the poster's position.
    """
    try:
        poster = pygame.image.load(image_path)
        poster = pygame.transform.scale(poster, ((3/4)*card_height * 4/5, card_height-20))
        screen.blit(poster, (x, y))
    except pygame.error as e:
        print(f"Error loading image: {e}")

def get_user_movie_data(user, dataset, recommend_function):
    """
    Retrieves and caches movie data for a user.
    Args:
        user (str): The selected user's name.
        dataset (dict): The dataset of users and their preferences.
        recommend_function (function): Function to generate recommendations.
    Returns:
        tuple: (recommended_movies, non_recommended_movies) with detailed data.
    """
    global user_movie_data_cache
    if user in user_movie_data_cache:
        # Return cached data if it exists
        return user_movie_data_cache[user]
    # Fetch recommendations
    recommended_movies, non_recommended_movies = recommend_function(dataset, user)
    print(recommended_movies)
    # Fetch detailed data for each movie
    detailed_recommended = []
    for movie in recommended_movies:
        data = search_film_by_title(movie)
        if data.get('Response') == 'False':
            detailed_recommended.append({"Title": movie, "Details": "No additional data available"})
        else:
            detailed_recommended.append(data)


    detailed_non_recommended = []
    for movie in non_recommended_movies:
        data = search_film_by_title(movie)
        if data.get('Response') == 'False':
            detailed_non_recommended.append({"Title": movie, "Details": "No additional data available"})
        else:
            detailed_non_recommended.append(data)

    # Cache the data
    user_movie_data_cache[user] = (detailed_recommended, detailed_non_recommended)

    return user_movie_data_cache[user]

def create_movie_card(movie_id,movie_data, x, y, width, is_recommended=True):
    """
    Creates a card for a movie with a title, poster, and additional details from OMDB API.
    Args:
        movie_id (int): id movie
        movie_data (dict): Movie data, including title, poster URL, director, year, etc.
        x (int): X-coordinate of the card's position.
        y (int): Y-coordinate of the card's position.
        width (int): Width of the card.
        is_recommended (bool): Whether the card represents a recommended movie.
    """
    card_width = width
    card_border_color = (100, 200, 100) if is_recommended else (200, 100, 100)

    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, card_width, card_height), border_radius=5)
    pygame.draw.rect(screen, card_border_color, pygame.Rect(x, y, card_width, card_height), 1, border_radius=5)

    # Display poster, if available
    poster=f'assets/temp_poster_{"r" if is_recommended == True else "a"}_{movie_id}.jpg'
    if 'Poster' in movie_data and movie_data['Poster'] != 'N/A':
        poster_url = movie_data.get('Poster', 'assets/default-movie.jpg')
        if changes:
            print("dowland")
            try:

                poster_response = requests.get(poster_url, stream=True)
                if poster_response.status_code == 200:
                    with open(poster, 'wb') as f:
                        f.write(poster_response.content)
                    display_poster(poster, x + 10, y + 10)
                else:
                    display_poster('assets/default-movie.jpg', x + 10, y + 10)
            except Exception as e:
                print(f"Error downloading poster: {e}")
                display_poster('assets/default-movie.jpg', x + 10, y + 10)
        else:
            display_poster(poster, x + 10, y + 10)
    else:
        # Display default poster if no valid poster URL
        display_poster('assets/default-movie.jpg', x + 10, y + 10)

    # Render movie title and other details if available
    details_x = x + ((3 / 4) * card_height * 4 / 5) + 20
    render_text(f"Title: {movie_data.get('Title', 'Unknown Title')}", details_x, y + 10 + card_content_offset)

    # Render director if available
    if 'Director' in movie_data:
        render_text(f"Director: {movie_data.get('Director', 'Unknown Director')}", details_x, y + 40 + card_content_offset)

    # Render year if available
    if 'Year' in movie_data:
        render_text(f"Year: {movie_data.get('Year', 'Unknown Year')}", details_x, y + card_height//2 + card_content_offset)


def create_button(text, x, y, width, height, font=font_button, bg_color=(34, 139, 34), border_color=(54, 159, 54)):
    """
    Creates and renders a button on the screen.
    Args:
        text (str): Text displayed on the button.
        x (int): X-coordinate of the button.
        y (int): Y-coordinate of the button.
        width (int): Width of the button.
        height (int): Height of the button.
        font (pygame.font.Font): Font for the button's text.
        bg_color (tuple): Background color of the button.
        border_color (tuple): Border color of the button.
    Returns:
        pygame.Rect: Rectangle representing the button's area.
    """
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, bg_color, button_rect, border_radius=5)
    pygame.draw.rect(screen, border_color, button_rect, 3, border_radius=5)
    render_text(text, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2, (40, 40, 40), font=font)
    return button_rect
menu_offset = 35
buttons = [
    Button(screen_width-150, menu_offset, 30, 30, "V", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((True, False, False), 0)),
    Button(screen_width-100, menu_offset, 30, 30, "X", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((False, True, False), 1)),
    Button(screen_width-50, menu_offset, 30, 30, "B", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((False, False, True), 2))
]
def set_display_recommend(setting, id_button):
    """
    Adjusts the display settings based on user interaction.

    Args:
        setting (tuple): New display recommendation setting.
        id_button (int): ID of the button that was clicked.
    """
    global display_recommend, card_height, card_offset, max_scroll_offset, scroll_offset,card_content_offset
    scroll_offset = 0
    max_scroll_offset = 0
    display_recommend = setting
    for i, button in enumerate(buttons):
        if id_button == i:
            if i == 0:
                button.set_color((100, 200, 100))
                card_height = CARD_HEIGHT * 2
                card_offset = CARD_OFFSET * 2
                card_content_offset = CARD_CONTENT_OFFSET *4
            elif i == 1:
                button.set_color((200, 100, 100))
                card_height = CARD_HEIGHT * 2
                card_offset = CARD_OFFSET * 2
                card_content_offset = CARD_CONTENT_OFFSET * 4
            elif i == 2:
                button.set_color((100, 100, 200))
                card_height = CARD_HEIGHT
                card_offset = CARD_OFFSET
                card_content_offset = CARD_CONTENT_OFFSET
        else:
            button.set_color((100, 100, 100))

selected_user = None
changes = False
async def run_gui(dataset, recommend_function):
    """
    Main loop to run the Pygame GUI interface.
    Args:
        dataset (dict): Dataset of users and their movie preferences.
        recommend_function (function): Function to generate recommendations.
    """
    global current_user, scroll_offset, max_scroll_offset,selected_user,changes
    user_dropdown = list(dataset.keys())
    list_open = False
    dropdown_button = pygame.Rect(20, 50, 200, 30)
    user_buttons = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_offset = max(0, scroll_offset - 20)
                elif event.button == 5:
                    scroll_offset = min(max_scroll_offset, scroll_offset + 20)
                if dropdown_button.collidepoint(event.pos):
                    list_open = not list_open
                if list_open:
                    for i, button in enumerate(user_buttons):
                        if button.collidepoint(event.pos):
                            selected_user = user_dropdown[i]
                            list_open = False
                            changes =True
                            # Reset cache if user changes
                            if selected_user != current_user:
                                current_user = selected_user
                                scroll_offset = 0
                                max_scroll_offset = 0

            for button in buttons:
                button.handle_event(event)

        screen.fill((30, 30, 30))
        content_y_offset = 130 - scroll_offset

        if selected_user is not None:
            # Get cached or fresh data for the user
            recommended_movies, non_recommended_movies = get_user_movie_data(
                selected_user, dataset, recommend_function
            )
            if display_recommend[2]:
                for i, movie_data in enumerate(recommended_movies):
                    create_movie_card(i,movie_data, 15, content_y_offset + i * (card_height + card_offset),
                                      (screen_width - 40) // 2, is_recommended=True)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height + card_offset))
                for i, movie_data in enumerate(non_recommended_movies):
                    create_movie_card(i,movie_data, ((screen_width - 40) // 2) + 20, content_y_offset + i * (card_height + card_offset),
                                      (screen_width - 40) // 2, is_recommended=False)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height + card_offset))
            elif display_recommend[0]:
                for i, movie_data in enumerate(recommended_movies):
                    create_movie_card(i,movie_data, 20, content_y_offset + i * (card_height + card_offset),
                                      screen_width - 40, is_recommended=True)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height + card_offset))
            elif display_recommend[1]:
                for i, movie_data in enumerate(non_recommended_movies):
                    create_movie_card(i,movie_data, 20, content_y_offset + i * (card_height + card_offset),
                                      screen_width - 40, is_recommended=False)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height + card_offset))
            changes = False
        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(0, 0, screen_width, 100))
        if selected_user:
            for button in buttons:
                button.render(screen)
            render_text(f"Selected User: {selected_user}", 300, menu_offset, color=(255, 255, 255))

        if list_open:
            pygame.draw.rect(screen, (60, 60, 60), (15, menu_offset - 5, 210, len(user_dropdown) * 40+60))
            user_buttons = []
            for i, user in enumerate(user_dropdown):
                button_rect = pygame.Rect(20, 90 + i * 40, 200, 30)
                create_button(user, 20, 90 + i * 40, 200, 30)
                user_buttons.append(button_rect)
        create_button("Select User", 20, menu_offset, 200, 30)
        pygame.display.flip()

    pygame.quit()
