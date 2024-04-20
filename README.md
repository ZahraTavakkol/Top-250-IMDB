# Top 250 IMDB Movies

## Overview
This project scrapes the top 250 movies from IMDB using Selenium and BeautifulSoup. The scraped data is then used to create a MySQL database. Finally, Power BI is employed to create an interactive dashboard and visualize the data.

## Features
- Scrapes the top 250 movies from IMDB.
- Creates a MySQL database based on the scraped data.
- Utilizes Power BI for interactive dashboard creation and data visualization.

## Implementation Details
1. **Scraping:** Selenium and BeautifulSoup are used to extract data from IMDB's top 250 movies list.
2. **Database Creation:** The gathered data is structured into a MySQL database.
3. **Visualization:** Power BI is utilized to visualize the data and create an interactive dashboard.

## Files
- `Scrap_Functions.py`: Required Functions for scraping data.
- `crawl.py` and `selenium.py`: Python script for scraping IMDB data.
- `db.py`: Script for creating the MySQL database structure.
- `dashboared.pbix`: Power BI file containing the interactive dashboard.

## Usage
1. Run `crawl.py` and `selenium.py` to scrape IMDB data.
2. Execute `db.py` to create the MySQL database structure.
3. Import the generated database into your MySQL environment.
4. Open `dashboared.pbix` in Power BI to explore the interactive dashboard and visualize the data.

## Dependencies
- Python (with Selenium and BeautifulSoup)
- MySQL
- Power BI
