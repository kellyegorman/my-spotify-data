import tkinter as tk
from tkinter import Text
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Function to fetch the user's top song and display it in the text box
def fetch_top_song():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-top-read"
        ))
        
        # Get the user's top track
        top_tracks = sp.current_user_top_tracks(limit=1)

        if top_tracks['items']:
            top_track = top_tracks['items'][0]
            song_name = top_track['name']
            artist_name = top_track['artists'][0]['name']
            track_info = f"Your top song is:\n\n{song_name} by {artist_name}"
        else:
            track_info = "No top songs found!"

        # Clear the text box and display the result
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, track_info)
    except Exception as e:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, f"An error occurred: {e}")

def fetch_top_artist():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-top-read"
        ))
        
        # Get the user's top artist
        top_artist_data = sp.current_user_top_artists(limit=1)

        if top_artist_data['items']:
            top_artist = top_artist_data['items'][0]['name']
            artist_info = f"Your top artist is: {top_artist}"
        else:
            artist_info = "No top artists found!"

        # Clear the text box and display the result
        text_box_2.delete(1.0, tk.END)
        text_box_2.insert(tk.END, artist_info)
    except Exception as e:
        text_box_2.delete(1.0, tk.END)
        text_box_2.insert(tk.END, f"An error occurred: {e}")


# Create the main application window
root = tk.Tk()

# Set the window title and size
root.title("My Spotify API Question")
window_width, window_height = 600, 400
root.geometry(f"{window_width}x{window_height}")

# Set the background color of the main window to light green
root.configure(bg="#90EE90")  # Light green hex color

# Calculate the position to center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Make sure the window is always on top
root.attributes("-topmost", True)

# Common font for both text boxes
font_style = ("Arial", 10)

# Create a frame to hold the textboxes side by side
frame = tk.Frame(root, bg="lightgreen")  # Corrected color
frame.configure(bg="lightgreen")  # Corrected color
frame.pack(pady=20)

# Create the first Text widget (for the top song), smaller size
text_box = Text(frame, wrap=tk.WORD, height=6, width=25, font=font_style, bd=2, relief="solid")
text_box.pack(side=tk.LEFT, padx=10)

# Create the second Text widget (for the top artist), smaller size
text_box_2 = Text(frame, wrap=tk.WORD, height=6, width=25, font=font_style, bd=2, relief="solid")
text_box_2.pack(side=tk.LEFT, padx=10)

# Automatically fetch and display the user's top song and top artist when the window opens
root.after(100, fetch_top_song)  # Schedule the function to run after 100ms
root.after(1000, fetch_top_artist)  # Schedule the function to run after 1000ms


# Run the application
root.mainloop()
