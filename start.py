import argparse
from scraper import Scraper

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--brands', nargs='+', required=True)
parser.add_argument('-s', '--start-page', type=int, default=1)
parser.add_argument('-e', '--end-page', type=int, default=10)
parser.add_argument('-o', '--output-path', default='./complaints')
parser.add_argument('-f', '--file-extension', choices=['csv', 'xlsx'], default='csv')
parser.add_argument('-i', '--info', action='store_true')

args = parser.parse_args()

scraper = Scraper(
    args.brands, 
    args.start_page, 
    args.end_page,
    args.info,
    args.file_extension,
    args.output_path)

scraper.scrape_data()
