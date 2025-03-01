# Mason Erman
# Txt Youtube Downloader
#
# Open .txt files with youtube links to download them to mp3/mp4
# Alternatively, submit links directly to the application
#
# Little to no error handling, be warned


from tkinter import *                                       # Useful for the application GUI
from tkinter import filedialog as fd                        # Needed for the file selection interface
import yt_dlp as youtube_dl                                 # Needed for downloading videos, renamed to match


# Populate the main window with initial buttons/labels that call functions
def main():

    # Text entry panel
    e = Entry(root, width = 50)
    e.insert(0, "Type link here")
    e.grid(row = 0, column = 0)

    # Button to submit text entry as youtube link
    submitlink = Button(root, text = "Submit Link", command = lambda: linksubmission(e), bg = "blue", padx = 40)
    submitlink.grid(row = 0, column = 1)

    # Button to upload txt file with links
    openfile = Button(root, text = "Open .txt File", command = txtparser, bg = "yellow", padx = 40)
    openfile.grid(row = 0, column = 2)

    root.mainloop()
    

# Function to download youtube videos from urls
def dwl_vid(video_url, ext):

    options={}

    # Selects MP3 filepath/options
    if ext == "mp3":
        file_path = fd.asksaveasfilename(title="Save As",
                                         defaultextension=".mp3",
                                         filetypes=[("MP3", "*.mp3"), ("All files", "*.*")])
        options={'format':'bestaudio/best',
                 'keepvideo':False,
                 'outtmpl': file_path,
                 'quiet': True,
                 'no_warnings': True,}
    
    # Selects MP4 filepath/options
    else:
        file_path = fd.asksaveasfilename(title="Save As",
                                         defaultextension=".mp4",
                                         filetypes=[("MP4", "*.mp4"), ("All files", "*.*")])
        options={'outtmpl': file_path,
                 'quiet': True,
                 'no_warnings': True,}
    
    # Downloads url to filepath with specified options
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])


# Parses through a .txt file creating video title labels and download buttons
def txtparser():

    # Opens a requested .txt file
    filepath = fd.askopenfilename()
    file = open(filepath,"r")

    # Calculates current grid size so we can append new items
    x = root.grid_size()
    rowcount = x[1]

    # Creating Lists to store element links, labels, and download buttons for each newline
    # Could switch with a class if more attributes are included
    links = []                                                  
    labelname = []
    mp3down = []
    mp4down = []

    # Iterate through the file appending links to new list
    count = 0
    for line in file:
        links.append(line.strip())
        count += 1
    file.close()

    # Iterate through the links to create labels with video titles
    i = 0
    while i != count:
        title = get_video_info(links[i])
        labelname.append(Label(root, text = title,
                               fg = "blue", padx = 50, pady = 8))
        labelname[i].grid(row = i+rowcount+1, column = 0)
        i += 1

    # Iterate to make buttons for MP3
    i = 0
    while i < count:
        mp3down.append(Button(root, text = "MP3 Download",
                              command = lambda i=i: dwl_vid(links[i], "mp3"),
                              bg = "purple", padx = 40))
        mp3down[i].grid(row = i+rowcount+1, column = 1)
        i += 1

    # Iterate to make buttons for MP4
    i = 0
    while i < count:
        mp4down.append(Button(root, text = "MP4 Download",
                              command = lambda i=i: dwl_vid(links[i], "mp4"),
                              bg = "green", padx = 40))
        mp4down[i].grid(row = i+rowcount+1, column = 2)
        i += 1


# Creates labels and buttons for a submitted youtube link
def linksubmission(e):

    # Pull link from text entry panel, deletes text inside afterwards
    url = e.get()
    e.delete(0, END)
    e.insert(0, "")

    # Calculates current grid size so we can append new items
    x = root.grid_size()
    rowcount = x[1]
    
    # Creates a label with video title
    title = get_video_info(url)
    lbl = Label(root, text = title, fg = "blue", padx = 50, pady = 8)
    lbl.grid(row = rowcount+1, column = 0)

    # Creates button to download MP3
    mp3 = Button(root, text = "MP3 Download",
                 command = lambda: dwl_vid(url, "mp3"),
                 bg = "purple", padx = 40)
    mp3.grid(row = rowcount+1, column = 1)

    # Creates button to download MP4
    mp4 = Button(root, text = "MP4 Download",
                 command = lambda: dwl_vid(url, "mp4"),
                 bg = "green", padx = 40)
    mp4.grid(row = rowcount+1, column = 2)


# Function to return video info such as title, length, etc...
def get_video_info(url):
    title = ""
    if url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ" or "https://www.youtube.com/watch?v=XGxIE1hr0w4" or "https://www.youtube.com/watch?v=3BFTio5296w":
        title = "Mysterious Video"
    else:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        title = info["title"]
    return title


# Root interface
root = Tk()
root.geometry("900x400")


main()
