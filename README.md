# mangawatcher
Get notifications of new manga in your watch list via pushbullet!
## Requirement

  - a functional pushbullet account and api key
  - pushbullet.py
  - sqlite3

## Installation

```sh
$ git clone https://github.com/gy199445/mangawatcher.git
$ sudo pip install pushbullet.py
```

## Initialize database and api_key

```sh
$ cd mangawatcher
$ sqlite3 manga.db < schema.sql
```

And don't forget to open a new file `pushbullet_key.py` and add a line `api_key = xxxx`

## Add your favorate manga and its url

Currently only the mangas from http://m.seemh.com are supported. The name and url are stored in the manga.txt, separated by '@'.

After adding your favorate manga, write it to the database.

```sh
python update_watchlist.py
```

## Run the mangawatcher.py first time

```sh
python mangawatcher.py -u
```

The `-u` parameter here 'remember' the publised episodes and prevent the program from pushing every captured episode. If you don't use it, you may get lots of pushbullet messages on your phone or something.

## Q&A

### How to get my pushbullet api key?

First, you need the access token, available on your pushbullet (web) settings. Then use `curl --header 'Access-Token: <your_access_token_here>' https://api.pushbullet.com/v2/users/me`
