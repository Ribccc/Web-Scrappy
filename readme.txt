#  Web Scraper

## Overview
The ** Web Scraper** is a GUI-based application that allows users to scrape websites efficiently. Built using Python, it extracts headings, paragraphs, lists, and tables from web pages and saves the data in multiple formats (TXT, JSON, or CSV). The application includes advanced features like adjustable scraping depth, real-time progress updates, and a user-friendly interface using Tkinter.

## Features
- **GUI Interface:** Simple and intuitive Tkinter-based UI.
- **Customizable Scraping:** Select headings, paragraphs, lists, or tables.
- **Multiple Output Formats:** Save scraped data as TXT, JSON, or CSV.
- **Scraping Depth Control:** Specify the level of depth for web crawling.
- **Real-time Progress Updates:** Displays scraping status and progress bar.
- **Multi-threading Support:** Runs scraping in the background without freezing the UI.
- **Save & Open Output:** Easily save data or open the output folder.

## Technologies Used
- **Python Libraries:** `requests`, `BeautifulSoup`, `tkinter`, `csv`, `json`, `threading`, `os`, `time`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Riccc/Web-Scrappy.git
   ```
2. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
3. Run the application:
   ```bash
   python web_scraper.py
   ```

## Usage
1. Enter the target website URL.
2. Select the content to scrape (Headings, Paragraphs, Lists, Tables).
3. Choose the output format (TXT, JSON, CSV).
4. Set the scraping depth.
5. Click "Start Scraping" and monitor progress.
6. Save or view the scraped data.

## Contributions
Contributions are welcome! Feel free to submit a pull request with new features or bug fixes.

