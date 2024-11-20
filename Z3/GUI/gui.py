import pygame
import requests
from GUI.button import Button
from contourpy.array import concat_offsets

# Initialize Pygame
pygame.init()

# Your OMDB API key
api_key = "YOUR_API_KEY"  # Provide your API key here

display_recommend = (1, 1, 1)
screen_width = 800
screen_height = 600
CARD_HEIGHT = 200
card_height = CARD_HEIGHT
CARD_OFFSET = 40
card_offset = CARD_OFFSET
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Movie Recommendation System')

# Define fonts
font = pygame.font.SysFont('Arial', 20)
font_button = pygame.font.SysFont('Arial', 25)

# Function to fetch movie data from OMDB API
def search_film_by_title(title, api_key=api_key):
    r = requests.get(f'http://www.omdbapi.com/?apikey={api_key}&t={title}')
    return r.json()

# Function to render text
def render_text(text, x, y, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to display movie poster (Placeholder for simplicity)
def display_poster(image_path, x, y):
    try:
        poster = pygame.image.load(image_path)
        poster = pygame.transform.scale(poster, ((3/4)*card_height * 4/5,(3/4)*card_height ))
        screen.blit(poster, (x, y))
    except pygame.error as e:
        print(f"Error loading image: {e}")

# Function to create a movie card
def create_movie_card(movie_title, x, y, width, is_recommended=True):
    card_width = width
    card_border_color = (100, 200, 100) if is_recommended else (200, 100, 100)

    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, y, card_width, card_height), border_radius=5)
    pygame.draw.rect(screen, card_border_color, pygame.Rect(x, y, card_width, card_height), 1, border_radius=5)
    display_poster('assets/default-movie.jpg', x + 10, y + 10)
    render_text(movie_title, x + ((3/4)*card_height * 2/5)/2, y+(card_height*3/4)+15)

# Function to create a button
def create_button(text, x, y, width, height, font=font_button, bg_color=(34, 139, 34), border_color=(54, 159, 54)):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, bg_color, button_rect, border_radius=5)
    pygame.draw.rect(screen, border_color, button_rect, 3, border_radius=5)
    render_text(text, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2,(40,40,40), font=font)
    return button_rect
menu_offset = 35
buttons = [
        Button(screen_width-150, menu_offset, 30, 30, "V", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((True, False, False),0)),
        Button(screen_width-100, menu_offset, 30, 30, "X", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((False, True, False),1)),
        Button(screen_width-50, menu_offset, 30, 30, "B", (100, 100, 100), (200, 200, 200), lambda: set_display_recommend((False, False, True),2))
    ]
# Function to handle display modes
def set_display_recommend(setting,id_button):
    global display_recommend
    global card_height
    global card_offset
    display_recommend = setting
    for i,button in enumerate(buttons):
        if id_button == i:
            if i == 0:
                button.set_color((100, 200, 100))
                card_height = CARD_HEIGHT * 2
                card_offset = CARD_OFFSET * 2
            elif i == 1:
                button.set_color((200, 100, 100))
                card_height = CARD_HEIGHT * 2
                card_offset = CARD_OFFSET * 2
            elif i == 2:
                button.set_color((100, 100, 200))
                card_height = CARD_HEIGHT
                card_offset = CARD_OFFSET
        else:
            button.set_color((100, 100, 100))


# Main function to run the Pygame interface
def run_gui(dataset, recommend_function):
    user_dropdown = list(dataset.keys())
    selected_user = None
    list_open = False
    scroll_offset = 0
    dropdown_button = pygame.Rect(20, 50, 200, 30)
    user_buttons = []
    max_scroll_offset=0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_offset = max(0, scroll_offset - 20)
                elif event.button == 5:  # Scroll down
                    scroll_offset = min(max_scroll_offset, scroll_offset + 20)

                if dropdown_button.collidepoint(event.pos):
                    list_open = not list_open

                if list_open:
                    for i, button in enumerate(user_buttons):
                        if button.collidepoint(event.pos):
                            selected_user = user_dropdown[i]
                            list_open = False

            for button in buttons:
                button.handle_event(event)

        screen.fill((30, 30, 30))
        content_y_offset = 130 - scroll_offset
        if selected_user is not None:
            recommended_movies, non_recommended_movies = recommend_function(dataset, selected_user)
            max_scroll_offset = content_y_offset+card_offset

            if display_recommend[2]:
                for i, movie in enumerate(recommended_movies):
                    create_movie_card(movie, 15, content_y_offset + i * (card_height +card_offset), (screen_width - 40) // 2, is_recommended=True)
                    max_scroll_offset = max(max_scroll_offset,content_y_offset + i * (card_height +card_offset))
                for i, movie in enumerate(non_recommended_movies):
                    create_movie_card(movie, ((screen_width - 40) // 2) +20, content_y_offset + i * (card_height +card_offset), (screen_width - 40) // 2, is_recommended=False)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height +card_offset))
            elif display_recommend[0]:
                for i, movie in enumerate(recommended_movies):
                    create_movie_card(movie, 20, content_y_offset + i * (card_height +card_offset), screen_width - 40, is_recommended=True)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height +card_offset))
            elif display_recommend[1]:
                for i, movie in enumerate(non_recommended_movies):
                    create_movie_card(movie, 20, content_y_offset + i * (card_height +card_offset), screen_width - 40, is_recommended=False)
                    max_scroll_offset = max(max_scroll_offset, content_y_offset + i * (card_height +card_offset))
        # Management Panel (always on top)
        pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(0, 0, screen_width, 100))
        if selected_user:
            for button in buttons:
                button.render(screen)
            render_text(f"Selected User: {selected_user}", 300, menu_offset, color=(255, 255, 255))

        if list_open:
            pygame.draw.rect(screen, (60, 60, 60), (15, menu_offset-5, 210, len(user_dropdown) * 40))
            user_buttons = []
            for i, user in enumerate(user_dropdown):
                button_rect = pygame.Rect(20, 90 + i * 40, 200, 30)
                create_button(user, 20, 90 + i * 40, 200, 30)
                user_buttons.append(button_rect)
        create_button("Select User", 20, menu_offset, 200, 30)
        pygame.display.flip()

    pygame.quit()
