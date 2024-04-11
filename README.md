# merakiAirMarshalAudit
Get the AirMarshal configuration for all networks and export to CSV file

How to Use:
1. Clone repo with `git clone https://github.com/Francisco-1088/merakiAirMarshalAudit.git` 
2. Edit config.py as follows
   * `api_key` should be your API Key
   * `org_id` should contain your organization ID as an integer (you can find your organization ID by scrolling down to the bottom of any Dashboard window)
3. Install the libraries in `requirements.txt` by running `pip install -r requirements.txt`
4. Run the script with `python main.py`

The script will then iterate through all networks in your organization and produce a CSV file of name `{org_id}_air_marshal_audit.csv`.
