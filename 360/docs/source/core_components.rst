Core Components
========================

User Authentication
-------------------
Purpose:

    This feature allows users to register for the site and login securely using Django's built-in user authentication to access a session on the site. 

:Key Components:

- Registration: users can register using their first and last name, a unique username of their choice, and a password at least 6 characters long. 
- Login: users can login using their username and password that they created during registration. 
- Profile: users can change their username and password on the settings page of the site.  

Database:

    The user table is Django's built in user authentication table, which stores the user's username, password, first name, last name, whether the user is active or not, staff or not, superuser or not, and date they joined. 

Security:

    The login and session security uses Django's built-in user authentication security features such as its password hashing, session management, and CSRF protection. 

Video Sharing
-------------

Purpose:

    Allows users to put in what video they are watching and displays the video info for all the users friends to see.

:Key Components:
- Video Search/URL Input: User will type/copy&paste the URL of the current video they are watching into the search bar and then hit the search button.
- Video Delete: User will have a video in the database and if they want to manually delete the video then press the red delete button.
- Video Hyperlink: User will have a hyperlink on the You Tube block that can be pressed to be directed to the exact video.

Database:

    The video storing system uses Django-backend, which stores the video info in a SQLite table. The video table stores the user, video url, video name.
..
    Suggestions from ChatGPT
    Purpose: Describe how users share and display YouTube videos in the app.
    Functionality:
    URL Input: Explain the field where users paste the YouTube URL.
    Video Embedding: Describe how the application renders the video using embedded YouTube links.
    Backend Processing: Mention any validation of URLs or storage of user video choices.
    Friending System

Friending System
----------------

Purpose:

    Allows users to search for others, send friend requests, and manage friend lists.

:Key Components:

.. 
    Describe how users search by username and the search algorithm used.

- Friend Search: Users can search for friends by typing a username. If users are found, their usernames are dynamically displayed along with an "Add Friend" button next to each result.
- Friend Request: Users hit the "Friend" button in the search results to send a friend request to the other user. 
- Friend List: Users can see their friends' usernames, online status, and what they are currently watching on the Friends List on the homepage. The online status of a user is indicated by a green dot on their friend card

Database:

    The friending system uses Django-friendships, which stores friendships in a SQLite table and manages friendship requests. The friendships table stores from_user, to_user, and date created. 

Real-Time Chat
--------------

Purpose:

    Allows users to be able to directly chat with their friends.

:Key Components:

- Connection(Django Channels): Users are connect when both users open the chat. This connection is by peer-to-peer.
- Chat Interface: Users can message each other through a widget. This widget pops up when the user clicks their friend block. The widget will appear on the bottom-right corner.
- Messaging: Users can message each by typing in the typing bar on the widget. To send the message they will need to press the send button.

Database:

Purpose: 

    Allows the storage of the history of the messages.
    
:Key Components:

- Sender: Allows the message and admin to know who sent the message.
- Receiver: Allows the message and admin to know where the message is suppose to go.
- Timestamp: Allows the Admin know when this message was sent.
- Message: Allows the admin and message know what the message says.

