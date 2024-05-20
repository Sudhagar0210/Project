import pyodbc
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from datetime import datetime
import isodate
import pandas as pd
from streamlit_lottie import st_lottie


api_key = "AIzaSyB8IubhIwhGqcfq421oO3bNWiTABCpdo_M"

def connect_to_database():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Sudhakar\\SQLEXPRESS01;DATABASE=Local_database;UID=sa;PWD=123')
        return conn
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
        return None
# Channel Data Insert to SQL Statement
def insert_channel_data(channel_data, conn):
    try:
        cursor = conn.cursor()
        sql_insert = """
        INSERT INTO Channel (channel_id, Channel_Name, channel_type, channel_description, channel_views,Channel_Total_Videos)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        data_to_insert = (
            channel_data["channel_id"],
            channel_data["channel_name"],
            channel_data["channel_type"],
            channel_data["channel_description"],
            channel_data["Channel_Views"],
            channel_data["Channel_Total_Videos"]
        )
        cursor.execute(sql_insert, data_to_insert)
        conn.commit()
        cursor.close()
        print("Channel data inserted successfully.")
    except Exception as e:
        print("An error occurred while inserting channel data:", e)

# Video Data Insert to SQL Statement
def duration_to_seconds(duration):
    return isodate.parse_duration(duration).total_seconds()

def insert_video_data(video_data, conn):
    try:
        cursor = conn.cursor()
        sql_insert = """
        INSERT INTO Video (video_id, playlist_id,channel_name, video_name,Publish_date, video_description, view_count, like_count, favorite_count, comment_count, video_duration, video_thumbnails, caption_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
        """
        for video in video_data:

            video_duration_seconds = duration_to_seconds(video["Video_duration"])

            data_to_insert = (
                video["video_id"],
                video["playlist_id"],
                video["channel_name"],
                video["Video_name"],
                video["Publish_date"],
                video["Video_description"],           
                video["View_Count"],
                video["Like_Count"],
                video["Favorite_Count"],
                video["Comment_Count"],
                video_duration_seconds,
                #video["Video_duration"],
                video["Video_thumbnails"],
                video["Caption_status"]
            )
            cursor.execute(sql_insert, data_to_insert)
        conn.commit()
        cursor.close()
        print("Video data inserted successfully.")
    except Exception as e:
        print("An error occurred while inserting video data:", e)

# Comment Data Insert to SQL Statement
def insert_comment_data(comment_data, conn):
    try:
        cursor = conn.cursor()
        sql_insert = """
        INSERT INTO Comment (comment_id, video_id, comment_author, Comment_Publish_Date, comment_text)
        VALUES (?, ?, ?, ?, ?)
        """
        for comment in comment_data:
            data_to_insert = (
                comment["comment_id"],
                comment["video_id"],
                comment["comment_author"],
                comment["Comment_Publish_Date"],
                comment["comment_text"]
            )
            cursor.execute(sql_insert, data_to_insert)
        conn.commit()
        cursor.close()
        print("Comment data inserted successfully.")
    except Exception as e:
        print("An error occurred while inserting comment data:", e)
        
youtube = build("youtube", "v3", developerKey=api_key)
def get_channel_data(api_key, channel_id):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        channel_response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        ).execute()

        if 'items' in channel_response and channel_response['items']:
            channel_info = channel_response["items"][0]
        else:
            print("No channel data found.")
            return None

        playlist_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()


        if 'items' in playlist_response and playlist_response['items']:
            playlist_id = playlist_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        else:
            print("No playlist data found" , channel_id)
            return None
        

        video_data = []
        next_page_token = None

        while True:
            videos_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            if 'items' in videos_response and videos_response['items']:
               videos = videos_response["items"]
            else:
             print("No videos found in the playlist.",channel_id)
             return None
            

            for video in videos:
                resource = video["snippet"].get("resourceId", {})
                video_id = resource.get("videoId")
                
                if video_id:
                    video_info = youtube.videos().list(
                        part="snippet,statistics,contentDetails",
                        id=video_id
                    ).execute()["items"][0]
                   

                    video_data.append({
                        "video_id": video_id,
                        "playlist_id": playlist_id,
                        "channel_name": channel_info["snippet"]["title"],
                        "Video_name": video_info["snippet"]["title"],
                        "Video_description": video_info["snippet"]["description"],
                        "Publish_date": video_info["snippet"]["publishedAt"],
                        "View_Count": video_info["statistics"]["viewCount"],                        
                        "Like_Count": video_info["statistics"].get("likeCount", 0),
                        "Favorite_Count": video_info["statistics"]["favoriteCount"],
                        "Comment_Count": video_info["statistics"].get("commentCount", 0),
                        "Video_duration": video_info["contentDetails"]["duration"],
                        "Video_thumbnails": video_info["snippet"]["thumbnails"]["default"]["url"],
                        "Caption_status": video_info["contentDetails"]["caption"]
                    })

            next_page_token = videos_response.get("nextPageToken")
            if not next_page_token:
                break

        return {
            "channel_id": channel_id,
            "channel_name": channel_info["snippet"]["title"],
            "channel_type": channel_info['kind'],
            "Channel_Views": channel_info['statistics']['viewCount'],
            "channel_description": channel_info['snippet']['description'],
            "channel_published": channel_info['snippet']['publishedAt'],
            "Channel_Total_Videos": channel_info['statistics']['videoCount'],
            "videos": video_data
        }
    except HttpError as e:
        print("An  error in fetching channel data:", e)
        return None

def get_video_comments( video_id, conn):
    try:    
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=500
        ).execute()   

        comments = comments_response["items"]

        if not comments:
            print("No comments found.")
        else:
            comment_data = []
            for comment in comments:
                comment_id = comment['id']
                video_id = comment['snippet']['videoId']  
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                Comment_Publish_Date = comment['snippet']['topLevelComment']['snippet']['publishedAt']

                comment_data.append({
                    "comment_id": comment_id,
                    "video_id": video_id,
                    "comment_author": comment_author,
                    "Comment_Publish_Date": Comment_Publish_Date,
                    "comment_text": comment_text
                })

            insert_comment_data(comment_data, conn)

    except HttpError as e:
        print("An HTTP error occurred:")
        print(e)


if __name__ == "__main__":
 


 
 # Query Execution

 def execute_query(query):
     conn = connect_to_database()
     if conn:
         cursor = conn.cursor()
         cursor . execute(query)
         result = cursor.fetchall()
         data =[tuple(row) for row in result]
         columns = [column[0] for column in cursor.description]
         cursor.close()
         conn.close()
         return data, columns
     else:
        return None, None
     
 def query_1():
     return execute_query("select top 5 Channel_Name , Video_Name from Video order by 1 asc") 

 def query_2():
     return execute_query("select top 1  Channel_Name , count(Video_Id) as Video_count from Video group by Channel_Name order by Video_count desc")

 def query_3():
     return execute_query("select top 10 Video_Name, Channel_Name,View_Count from video order by View_Count desc")
 
 def query_4():
     return execute_query("select v.Video_Name , v.Video_Id, count(Comment_Id) as Comment_Count from Comment c join video v on c.Video_Id = v.video_id group by v.Video_Name, v.video_id order by Comment_Count desc")

 def query_5():
     return execute_query("select top 1 Like_Count, Video_Name ,Channel_Name  from Video order by Like_Count desc")   

 def query_6():
     return execute_query("select Like_Count,Video_Name  from Video order by Like_Count desc") 

 def query_7():
     return execute_query("select Channel_Views, Channel_Name from Channel order by 2 desc")  

 def query_8():
     return execute_query("select top 10 * from Video where Publish_date > 2022-01-01")     
 
 def query_9():
     return execute_query("select Channel_Name, avg(Video_duration) as Average_Duration from Video group by Channel_Name") 

 def query_10():
     return execute_query("select top 10 V.Video_Name,v.Channel_Name ,max(Comment_Count) as Maximun_Comment_Count from Video v join Comment c on v.Video_Id=c.Video_Id group by v.Video_Name, v.Channel_Name order by Maximun_Comment_Count desc")                  


# Streamlit Code

 def main():
    
    st.title("YouTube Data Harvesting and Warehousing")

    #sidebar menu 
    menu_selection = st.sidebar.radio("Menu", ["Home", "Extract and Transform", "View"])

    # selected menu option
    if menu_selection == "Home":
        render_home()
    elif menu_selection == "Extract and Transform":
        render_extract()
    elif menu_selection == "View":
        render_view()


def render_home():
    
    #st.title("YouTube API Data Fetcher")
    st.image("YouTube_img.JPG", caption='Your Project Logo', use_column_width=True)



def render_extract():
    st.title("EXTRACT TRANSFORM")     
    st.write("Enter Channel_ID Below:")

    channel_id = st.text_input("Enter YouTube Channel ID")

    if st.button("Fetch Data"):
      if channel_id:
        channel_data = get_channel_data(api_key, channel_id)
        if channel_data:
            st.session_state['channel_data'] = channel_data
            st.success("Data fetched successfully. Ready to Upload Database.")
        else:    
         st.warning("Please enter a YouTube Channel ID.")

    if 'channel_data' in st.session_state and st.session_state['channel_data']:      
      if st.button("Upload Data"):
        conn = connect_to_database()
        if conn:
            insert_channel_data(st.session_state['channel_data'], conn)
            insert_video_data(st.session_state['channel_data']['videos'], conn)
            for video in st.session_state['channel_data']['videos']:
                get_video_comments(video["video_id"], conn)
            conn.close()
            st.success("All data uploaded successfully.")


def render_view():
    st.title("QUERIES")
    #st.write("Search Query")
    
    options = [
        "Select Query",
        "Q1.What are the names of all the videos and their corresponding channel?",
        "Which channel has the most number of videos, and how many videos do they have?",
        "What are the top 10 most viewed videos and their respective channels?",
        "How many comments were made on each video, and what are their corresponding video names?",
        "Which videos have the highest number of likes, and what are their corresponding channel names?",
        "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        "What is the total number of views for each channel, and what are their corresponding channel names?",
        "What are the names of all the channels that have published videos in the year  2022?",
        "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        "Which videos have the highest number of comments, and what are their corresponding channel names? "        

    ]

    select_option = st.selectbox("Select an Option",options)

    if st.button ("Sumbit"):
        if select_option == options[1]:
            results, columns = query_1()
        elif select_option == options[2]:
            results, columns = query_2()
        elif select_option == options[3]:
            results, columns = query_3()
        elif select_option == options[4]:
            results, columns = query_4()
        elif select_option == options[5]:
            results, columns = query_5()
        elif select_option == options[6]:
            results, columns = query_6()
        elif select_option == options[7]:
            results, columns = query_7()
        elif select_option == options[8]:
            results, columns = query_8()
        elif select_option == options[9]:
            results, columns = query_9()
        elif select_option == options[10]:
            results, columns = query_10()
        else:
            st.warning("Please select Vaild Option")
            return  
        
        # st.write("Results:", results)
        # st.write("Columns:", columns)        

        if results:
            df = pd.DataFrame(results, columns=columns)
            st.dataframe(df)
       
        else:
            st.write("No results found or an error occurred.")


    
if __name__ == "__main__":
    main()






