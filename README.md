# Sikayetvar Scraping

A scraping tool for customer complaints of specified brands to use in NLP tasks.
<hr>


## Usage

Clone repository:
```
git clone https://github.com/umutkavakli/sikayetvar-scraping.git
```
Move to project directory:
```
cd sikayetvar-scraping/
```
Run format:
```
python3 start.py [-h] [-t [TEST]] -b BRANDS [BRANDS ...] [-s START_PAGE] [-e END_PAGE] [-o OUTPUT_PATH] [-f {csv,xlsx}] [-i] [--frequency FREQUENCY]
```

## Parameters

<b>-t, &nbsp;&nbsp;--test</b>: Test parameter to see if frequency is enough to pull data without rejected request.
<b>-b, &nbsp;&nbsp;--brands</b>: Specified brands to scrape complaint data. It is required parameter and it takes at least one brand name. It can take list of brand names.
<br><b>-s, &nbsp;&nbsp;--start-page</b>: Start page. Default: 1.
<br><b>-e, &nbsp;&nbsp;--end-page</b>: End page. Default: 10.
<br><b>-o, &nbsp;&nbsp;--output-path</b>: Output path for saving data. Given dir1/dir2/file_name input created dir1 and dir2 directories (if they don't exist) and a file.
<br><b>-f, &nbsp;&nbsp;--file-extension</b>: Output extension format. Both 'csv' and 'xlsx' can be used. Default is csv.
<br><b>-i, &nbsp;&nbsp;--info</b>: Prints information about scraping data for current brand every page.  
<br><b>--frequency</b>: Frequency range for sending request, default=0.5 second.
 
## Example

```
python3 start.py -b brand1 brand2 brand3 -s 10 -e 20 -o my_directory/complaints -f xlsx
```

<b>Output:</b>
<br>Creates complaints.xlsx file inside my_directory directory for the data of brand1 brand2 and brand3 between 10 and 20 pages.
