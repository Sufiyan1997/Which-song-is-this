# What song is this

Have you used Shazam or asked siri `what song is this?` to identify the song  currently being played? Basically, these systems record a song with mic and compare the recording with existing database of the songs. The project is basically same thing.

## Installation

### 1. clone this repo
### 2. Install packages mentioned in requirements.txt
```shell
pip install -r requirements.txt
```
### 3. install ffmpeg
On linux you can do it by
```shell
sudo apt install ffmpeg
```
On windows you can download build from [here](https://ffmpeg.zeranoe.com/builds/)

### 4. set path of ffmpeg in `config.json`
If path to ffmpeg is already in PATH then just write `ffmpeg`

That's it :smiley:

## Usage

### Creating a database
First you need to create a database of songs which can be searched to identify a song.

1. To do that put the songs that you want to include in db in the `raws` folder. You can put them somewhere else as well, if you do that just put the absolute path to that folder in `config.json`
2. Run db creator script
```shell
python audio_db_creator.py
```
   
You will see 2 files (`db.pickle` and `metadata.pickle`) in `db` folder. That is your database of songs. Again, you can put them somewhere else as well, just set absolute path in `config.json`

### Searching

Record songs with your computer/phone and put them in `recordings` folder. If you wish to put them somewhere else set path in `config.json`

Run the matcher script
```shell
python audio_matcher.py
```
And ***voila*** you will see which recording matches with songs

## How it works?

*Note : I am currently in process of improving the search algorithm*

A detailed explaination of the algorithm can be found [here](http://coding-geek.com/how-shazam-works/)


