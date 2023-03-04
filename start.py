import argparse
from scraper import Scraper

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--brands', nargs='+', required=True, 
                    help="Specified brands to scrape complaint data. It is required parameter and it takes at least one brand name. It can take list of brand names.")
parser.add_argument('-s', '--start-page', type=int, default=1, 
                    help="Start page. Default: 1.")
parser.add_argument('-e', '--end-page', type=int, default=10, 
                    help="End page. Default: 10.")
parser.add_argument('-o', '--output-path', default='./complaints', 
                    help="Output path for saving data. Given dir1/dir2/file_name input created dir1 and dir2 directories (if they don't exist) and a file.")
parser.add_argument('-f', '--file-extension', choices=['csv', 'xlsx'], default='csv', 
                    help="Output extension format. Both 'csv' and 'xlsx' can be used. Default is csv.")
parser.add_argument('-i', '--info', action='store_true',
                    help="Prints information about scraping data for current brand every page.")

args = parser.parse_args()

scraper = Scraper(
    args.brands, 
    args.start_page, 
    args.end_page,
    args.info,
    args.file_extension,
    args.output_path)

scraper.scrape_data()
