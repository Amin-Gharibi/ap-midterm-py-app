# IMDB M.M.

This project is the front-end component of the mid-term assignment for the Advanced Programming course at Ilam University, supervised by Dr. Bag-Mohammadi.
this project is based on the CustomTkinter package.

## Table Of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

## Overview
This project is a movie rating system similar to IMDB, where admins can create movies, casts. and Critics and Normal users can sign up, and upon approval by an admin, they can start rating and commenting on movies and casts. Critics' ratings have a doubled effect compared to normal users. All users can publish articles, which others can rate and comment on.

## Features
- Show Latest Movies Added
- Show Random Genre Top Rated Movies
- Show Latest Articles Added
- Show Top Rated Cast
- Universal Search
- Exclusive Search for Movies, Articles, Casts
- User Profile Editing by User or Admin
- Admin Features:
  - Add, Edit, or Delete Movies (as draft or published)
  - Add, Edit, or Delete Casts
  - Approve or Reject Comments
  - See and Manage All Articles (delete if not approved)
- User Features:
  - Add Articles (as draft or published), Edit or Delete Them
  - Comment on Cast, Movie, Article; Like, Dislike, Reply to Comments
  - Add Movies, Articles to Favorite List, Remove from List

## Usage
To use this application, follow these steps:

1. Clone or download the backend side of the project from [here](https://github.com/Amin-Gharibi/ap-midterm-backend) and run the server. A tutorial on running the server is available on the backend page.
2. Ensure Redis is installed on your system and run the Redis server.
3. Navigate to the frontend folder and create a `.env` file with the following fields:
    ```plaintext
    BASE_URL=<COMMON-PART-OF-THE-BACKEND-APIS e.g., http://localhost:3000/api>
    REDIS_HOST=<REDIS HOST e.g., localhost>
    REDIS_PORT=<REDIS PORT e.g., 6379>
    ```
4. Run `main.py`.

Done!

## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

###### Redis has been used to store user access tokens.
