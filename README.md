# Burger Bash Map

This is an unofficial Halifax Burger Bash map for 2026.

I created this to help me easily find where the burgers are located, maybe it will help you too.

Map preview: https://benhovinga.github.io/burgerbash-map/

Official Burger Bash Website: https://burgerbash.ca/

Go enjoy some burgers!

## How it was built

Inside the `tools/` directory you will find the python scripts I used.

I first created `scraper.py` to scrape the Burger Bash website and get a list of burgers. Then I used `cleanup.py` to cleanup and normalize the data. Some of the data was still inaccurate so I did some manual cleanup as well.

After getting the data I created a simple Leaflet map and loaded the data onto the map.

This was all built in a day, so it's not using all the best practices and I suspect are still errors in the data.
