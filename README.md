# Spotify Social Network Analysis

## Required libraries

The required libraries are specified in the requirements.txt file. You need to install:

- pandas
- scikit-learn
- plotly
- matplotlib
- seaborn
- networkx

## Data

If you want to skip the scraping stage, which in total takes cca. 17h, I have published 
the already scraped data:

    URL
    
Download the file and unzip it in the folder "data/". You will get also the already generated GEXF graph files.
 
Scraping takes a long time due to the Spotify API limits. This limits are not clearly specified and we 
have to err on the side of caution to not get banned.

Scraping times for 10000 artists:

- Artists: cca. 3h
- Top 10 artist tracks and their audio features: cca. 6h
- Writers of top 10 artist tracks: cca. 23h

Due to the large amount of time it takes to scrape the top 10 song writers we limited the scraping to 
only top 3 songs per artist which brings the scraping time for writers down to cca. 8h.

### Scraping instructions

Edit main.py and set (at the top of the file) your CLIENT_ID and CLIENT_SECRET from Spotify API. In addition 
you will have to collect your "Bearer token" from your browser when you login to https://open.spotify.com/ and
also save it at the top of the file in the TOKEN variable.

#### Collecting the "Bearer token"

Because the 

## Data analysis and graph generation

Once you have the scraped files in data/raw/ folder you can open the Jupyter Notebook
notebooks/scraped_data_analysis.ipynb and run it to load the data, clean it and generate GEXF graph files.
