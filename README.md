> [!NOTE]
> Header is a dummy Header. You're also able to edit the description to match whatever you like for it to say.

> [!TIP]
> You're also able to edit the description to match whatever you like for it to say.

Even though this is one of my favorite and most useful project, I've encountered it very difficult to work it out due to the horrible documentation of the SPotipy library: https://spotipy.readthedocs.io/en/2.24.0/ , but in the end we finally made it work.

The program consists of scraping data from the Billboard hot 100 website (https://www.billboard.com/) and using that information to create a list with the 100 songs. After gathering that list, we autheticate to spotify using the SPotipy library since the Spotify authentiaction uses OAuth2, and then we gathe the songs uri to be able to create a list with all of the songs and create a playlist with them.

Enjoy! :D
