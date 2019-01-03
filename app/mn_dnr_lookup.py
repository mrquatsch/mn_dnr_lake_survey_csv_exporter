import mn_dnr
import properties

def main():
    '''
    Gather a list of lakes from the MN DNR site
    Use this list to gather species catch by length counts
    '''
    output_filename = properties.output_filename

    print('Running script...')
    lake_list = mn_dnr.compile_lake_list()
    print(f'Will create {output_filename} file with {len(lake_list)} results')
    print_output(lake_list)
    print('Done!')

def print_output(lake_list):
    '''
    Prints out the data is a CSV style format
    '''
    csv_output_directory = properties.csv_output_directory
    output_filename = properties.output_filename
    output_filename = (f'{csv_output_directory}/{output_filename}')

    csv_file = open(output_filename, 'w')
    fish_catch_length_ranges = ['0-5','6-7','8-9','10-11','12-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-300']
    fish_catch_length_range_header = ''
    for fish_catch_length_range in fish_catch_length_ranges:
        fish_catch_length_range_header = fish_catch_length_range_header + '","' + fish_catch_length_range + ' in'
    csv_file.write('"Lake Name","Lake ID","County Name","Nearest Town","Survey Date","Species","Total Count' + fish_catch_length_range_header + '"\n')

    for lake in lake_list:
        lake = lake[0]
        try:
            lake_name = lake['lake_name']
            lake_id = lake['lake_id']
            county_name = lake['county_name']
            nearest_town = lake['nearest_town']
            survey_date = lake['survey_date']
            for species in lake['species']:
                fish_catch_length_ranges_dictionary = {}
                species_name = species['species_name']
                total_catch_count = species['total_catch_count']
                for catches in species['catches']:
                    for fish_catch_length_range in fish_catch_length_ranges:
                        min_length = int(fish_catch_length_range.split('-')[0])
                        max_length = int(fish_catch_length_range.split('-')[1])
                        fish_catch_length = int(catches['fish_length'])
                        fish_catch_count = int(catches['fish_count'])
                        if fish_catch_length in range(min_length, max_length + 1):
                            if fish_catch_length_range in fish_catch_length_ranges_dictionary:
                                fish_catch_length_ranges_dictionary[fish_catch_length_range] += fish_catch_count
                            else:
                                fish_catch_length_ranges_dictionary[fish_catch_length_range] = fish_catch_count

                fish_catch_length_range_row = ''
                for fish_catch_length_range in fish_catch_length_ranges:
                    if not fish_catch_length_range in fish_catch_length_ranges_dictionary:
                        fish_catch_length_ranges_dictionary[fish_catch_length_range] = 0
                    fish_catch_length_range_row = fish_catch_length_range_row + ',' + str(fish_catch_length_ranges_dictionary[fish_catch_length_range])
                csv_file.write('"' + lake_name + '",' + str(lake_id) + ',"' + county_name + '","' + nearest_town + '","' + survey_date + '","' + species_name + '",' + str(total_catch_count) + fish_catch_length_range_row + '\n')
        except:
            pass
    csv_file.close()

if __name__ == '__main__':
    main()