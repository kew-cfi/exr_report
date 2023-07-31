# exr_report
Automate process of reporting other currencies to European exchange rate, by scraping data from ECB API

### To Run:
1. Use the <code>main</code> function in src/analysis/scraper.py.
2. It will generate the dataframe that contains the exchange rate based on the start and end period defined.
3. Output is generated in data/preprocess under the name <b>ecb_exchange_rate_{end_period}.csv</b>

### Key Parameters to Get the Desired Reports:
1. Change the 'start_period', 'end_period' and 'country' in <code>main</code> function.
2. If 'start_period' is stated None, the period defined in 'end_period' will be used to extract the data.

### Remarks
- Export file path can be controlled in config.py.
- Variables to be displayed can be controlled by <code>VARS</code> in config.py, by setting the 'predictive' True or False.  