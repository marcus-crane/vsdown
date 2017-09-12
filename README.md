# VSDown - Game asset downloader

![A screenshot of the script downloading a game manifest](/docs/downloading.png?raw=true)

## What to heck?

I've been slowly trying to pull apart a mobile game I've been playing for a while now and I figured I'd "anonymise" some of my scripts and release them to show I'm actually doing things on github dot com (i need my cubes!)

This script is something quick I whipped up that downloads game assets from a cloudfront server directly to my laptop.

Normally the game client would download these directly and encrypt them at runtime but some packet sniffing using my test phone pointed out that each update has its own manifest list.

What this program does is parse said manifest list which is basically a CSV with some header bits, downloads them and optionally, runs the program `strings` on them.

## Why strings?

Well, a lot of the files aren't obvious at first as to what they are. While you could use a hex editor, it's easier, in my opinion, to just convert them to text files in the first place and manually scan them.

![An example of a file passed through strings](/docs/stringfile.png?raw=true)

Here's `C004_SND.pkg` for example which, as the filename would imply, is actually a sound file as give away by the `LANE3.99.5` strings.

Majority of the files I've figured out or mostly figured out while others are still a mystery. Anyway, that's a story for another time.

## This looks like it was written by a beginner in Python! There's no error checking or XYZ! Where are the tests!

This was written by a beginner in Python yup
