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

- Friend Search: 
- Friend Request: Users hit the "Friend" button in the search results to send a friend request to the other user. 
- Friend List: Users can see their friends' usernames, online status, and what they are currently watching on the Friends List on the homepage. 

Database:

    The friending system uses Django-friendships, which stores friendships in a SQLite table and manages friendship requests. The friendships table stores from_user, to_user, and date created. 

Real-Time Chat
--------------
..
    Suggestions from ChatGPT
    Purpose: Enables direct chat between friends.
    Technology Stack: If using WebSockets or similar for real-time updates, specify the framework/library (e.g., Django Channels).
    Chat Interface:
    Describe how the chat window opens (e.g., clicking a friend’s name) and its features (like sending messages, seeing read receipts).
    Mention UI/UX elements, such as timestamps or user avatars.
    Data Handling:
    Explain how messages are stored and retrieved, and any message history features.
    Security considerations, such as end-to-end encryption if applicable.