import argparse
from scraper import Scraper

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--brands', nargs='+', required=True)
parser.add_argument('-c', '--complaint-type', choices=['unsolved', 'solved', 'both'], default='unsolved')
parser.add_argument('-s', '--start-page', type=int, default=1)
parser.add_argument('-e', '--end-page', type=int, default=500)
parser.add_argument('-o', '--output-path')
parser.add_argument('-f', '--file-output-type', choices=['csv', 'xlsl'], default='csv')
parser.add_argument('-i', '--info')

args = parser.parse_args()

scraper = Scraper(
    args.brands, 
    args.complaint_type, 
    args.start_page, 
    args.end_page)

scraper.scrape_data()