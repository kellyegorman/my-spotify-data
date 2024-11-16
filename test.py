import tkinter as tk
from tkinter import Text, Label
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk
import requests
from io import BytesIO

# song
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
            track_info = f"Your top song is:\n{song_name} by {artist_name}"
        else:
            track_info = "No top songs found!"

        # Clear the text box and display the result
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, track_info)
    except Exception as e:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, f"An error occurred: {e}")

# artist
def fetch_top_artist():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-top-read"
        ))
        
        top_artist_data = sp.current_user_top_artists(limit=1)

        if top_artist_data['items']:
            top_artist = top_artist_data['items'][0]['name']
            artist_info = f"Your top artist is:\n{top_artist}"
        else:
            artist_info = "No top artists found!"

        text_box_2.delete(1.0, tk.END)
        text_box_2.insert(tk.END, artist_info)
    except Exception as e:
        text_box_2.delete(1.0, tk.END)
        text_box_2.insert(tk.END, f"An error occurred: {e}")

#  album cover
def fetch_album_cover():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-top-read"
        ))

        #  track
        top_tracks = sp.current_user_top_tracks(limit=1)
        
        if top_tracks['items']:
            top_track = top_tracks['items'][0]
            album = top_track['album']
            album_cover_url = album['images'][0]['url']  # Get the URL of the album cover

            #  image
            response = requests.get(album_cover_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((200, 200))  # fit

            # covert
            album_cover = ImageTk.PhotoImage(img)

            album_cover_label.config(image=album_cover)
            album_cover_label.image = album_cover  
        else:
            album_cover_label.config(image='', text='') 
    except Exception as e:
        album_cover_label.config(image='', text=f"An error occurred: {e}")


# window and label
root = tk.Tk()
root.title("My Spotify Stats")
window_width, window_height = 440, 700
root.geometry(f"{window_width}x{window_height}")
welcome_label = Label(root, text="Welcome!", bg="#457e59", font=("Helvetica", 20, 'bold'), fg="black")
welcome_label.pack(pady=20)
root.configure(bg="#457e59")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

frame = tk.Frame(root, bg="#457e59")
frame.pack(pady=20)

# text
font_style = ("Helvetica", 12, 'bold')
text_box = Text(frame, wrap=tk.WORD, height=5, width=15, font=font_style, bd=2, relief="flat", bg="#f0f0f0", fg="#333")
text_box_2 = Text(frame, wrap=tk.WORD, height=5, width=15, font=font_style, bd=2, relief="flat", bg="#f0f0f0", fg="#333")
text_box.pack(side=tk.LEFT, padx=10)
text_box_2.pack(side=tk.LEFT, padx=10)

# album cover 
album_cover_label = Label(root, bg="#457e59")
album_cover_label.pack(pady=10)

# Start fetching data
root.after(10, fetch_top_song)
root.after(10, fetch_top_artist)
root.after(10, fetch_album_cover)
root.resizable(True, True)
# Run the application


# progress = ttk.Progressbar(root, length=200, mode='indeterminate')
# progress.pack(pady=20)
# progress.start() 

root.mainloop()
