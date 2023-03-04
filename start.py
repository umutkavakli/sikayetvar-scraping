import argparse
from scraper import Scraper

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--brands', nargs='+', required=True, 
                    help="brands that are used to scrape data")
parser.add_argument('-s', '--start-page', type=int, default=1, 
                    help="start page (between 1-500). default: 1")
parser.add_argument('-e', '--end-page', type=int, default=10, 
                    help="end page (between 1-500). default: 10")
parser.add_argument('-o', '--output-path', default='./complaints', 
                    help="outpuh for saving data. dir1/dir2/file_name can be created nested two directory and a file")
parser.add_argument('-f', '--file-extension', choices=['csv', 'xlsx'], default='csv', 
                    help="output extension format")
parser.add_argument('-i', '--info', action='store_true',
                    help="prints information for current brand every page")

args = parser.parse_args()

scraper = Scraper(
    args.brands, 
    args.start_page, 
    args.end_page,
    args.info,
    args.file_extension,
    args.output_path)

scraper.scrape_data()
