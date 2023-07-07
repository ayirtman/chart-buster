# Chart-Buster 🎵🚀

_Because why should time travellers have all the fun!_

Chart-Buster is a nifty Python script that blasts you into the past, reviving those old, gold hits from the year you wish. It scrapes chart data from Top 40 Weekly, cleans it, and downloads the music tracks from YouTube right into your system. Pretty rad, huh? Time to relive the 70s, the 80s, or any decade you fancy, with Chart-Buster!

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Web Scraping**: The script uses Beautiful Soup to scrape the top 40 songs of any given week from the past.
- **Data Cleaning**: It parses and cleans the scrapped data and neatly arranges it in a tabular CSV file.
- **YouTube Search and Download**: Finally, it uses `yt_dlp` to search and download the corresponding music tracks from YouTube.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

- Python 3.6 or later
- `beautifulsoup4`
- `requests`
- `pandas`
- `yt_dlp`

You can install these packages using pip:

```bash
pip install beautifulsoup4 requests pandas yt_dlp
```

### Installing
1. Clone this repository:

```bash
git clone https://github.com/ayirtman/chart-buster.git
```

2. Change to the chart-buster directory:

```bash
cd chart-buster
```

3. Run the script:

```bash
python chart_buster.py
```

## Usage
Modify the URL in the script to the chart of your desired week:

```python
url = "https://top40weekly.com/1972-all-charts/"
```

The script will download the top songs of that week and store them in the same directory.

## Contributing
Feel free to submit pull requests to help me improve this script. All your inputs are wholeheartedly welcomed!

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

---

_Note: Please make sure you have the rights to download and listen to the songs. This script was made for personal use and educational purposes only._