from datetime import datetime

current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

fish_id_lookup_url = 'http://maps2.dnr.state.mn.us/lakefinder/lib/lakefinder.js'
county_id_lookup_url = 'http://maps1.dnr.state.mn.us/cgi-bin/gazetteer2.cgi?type=county&_=1517509749935'
lake_id_lookup_url = 'http://maps2.dnr.state.mn.us/cgi-bin/lakefinder_json.cgi?context=desktop&name=&county='
lake_info_url = 'http://maps2.dnr.state.mn.us/cgi-bin/lakefinder/detail.cgi?type=lake_survey&id='

number_of_threads = 50

csv_output_directory = '/output'
output_filename = (f'mn_dnr_fish_counts_{current_timestamp}.csv')
