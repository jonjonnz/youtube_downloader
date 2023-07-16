import streamlit as st
from pytube import YouTube, Playlist

# Custom CSS styles
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #f63366;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #ed3a66;
            color: black; /* Change text color to black on hover */
        }
        .stTextInput>div>div>input {
            background-color: #f5f5f5;
            color: black;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        .stTextInput>div>div>input:focus {
            box-shadow: 0 0 5px #f63366;
        }
        .stMarkdown {
            font-size: 16px;
            line-height: 1.6;
        }
        .stFooter {
            color: #888;
            font-size: 14px;
        }
        img {  
            max-width: 40%;  
            height: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def download_content(url, content_type):
    try:
        if "playlist" in url.lower():
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                if content_type == "audio":
                    download_single_audio(video_url)
                else:
                    download_single_video(video_url)
        else:
            if content_type == "audio":
                download_single_audio(url)
            else:
                download_single_video(url)

        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


def download_single_audio(url):
    try:
        # Get the YouTube video
        yt = YouTube(url)

        # Extract the audio stream (highest quality available, in this case)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        # Set the output file path and download the audio
        audio_stream.download(output_path="./downloads")

        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


def download_single_video(url):
    try:
        # Get the YouTube video
        yt = YouTube(url)

        # Set the output file path and download the video
        yt.streams.get_highest_resolution().download(output_path="./downloads")

        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


def main():
    title_col,img_col = st.columns([2, 1])

    img_col.image("logo.png", use_column_width=True)  # Add your logo image path here
    title_col.title("YouTube Downloader")

    # Input box for URL
    url = st.text_input("Enter the YouTube video or playlist URL", "")

    # Create two columns for the buttons and place them side by side
    col1, col2 = st.columns(2)

    # Download buttons with custom style
    if col1.button("Download Audio"):
        if url:
            success = download_content(url, "audio")
            if success:
                st.success("Audio downloaded successfully!")
        else:
            st.warning("Please enter a valid YouTube video or playlist URL.")

    if col2.button("Download Video"):
        if url:
            success = download_content(url, "video")
            if success:
                st.success("Video downloaded successfully!")
        else:
            st.warning("Please enter a valid YouTube video URL.")

    # Add a footer with additional information
    st.markdown(
        """
        **Note**: Please ensure that you have the necessary permissions to download content from YouTube and respect copyright laws.
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
