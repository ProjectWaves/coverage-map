import os, csv, sys
import matplotlib.pyplot as plt
import shapefile

def save_csv(data, path):
    if len(data) == 0:
        raise ValueError('Data we are saving has no elements, aborting...')
    if not isinstance(data[0], dict):
        raise ValueError('Data rows are not saved as dicts, aborting...')
    header = list(data[0])
    with open(path, 'w') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# valid is a function, reader is a csv_reader, save_path is a path
def filter(path, valid, save_path, save=True):
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if valid(row):
                data.append(row)
    if save:
        save_csv(data, save_path)
    return data

def draw_water():
    sf = shapefile.Reader('tl_2020_24510/tl_2020_24510_areawater.shp')
    for shape in sf.shapes():
        plt.fill(*zip(*shape.points), "blue")

def clean_comcast_data():
    is_comcast = lambda row: 'Comcast' in row.get('Holding Company Final', '')
    data = filter('baltimore_data.csv', is_comcast, None, False)
    speeds = {} # by block
    for row in data:
        code = row['Census Block FIPS Code']
        speed = int(row['Max Advertised Downstream Speed (mbps)'])
        speeds[code] = speed
    print(set(speeds.values()))
    return speeds

def draw_blocks():
    comcast_data = clean_comcast_data()

    sf = shapefile.Reader('tl_2020_24510/tl_2020_24510_tabblock10.shp')
    for data in sf.shapeRecords():
        shape = data.shape
        # GEOID10 maps to Census Block FIPS Code for some reason
        fips_code = data.record.as_dict()['GEOID10']
        plt.fill(*zip(*shape.points), color=get_color(fips_code, comcast_data))

def get_color(fips_code, data):
    cmap = plt.cm.get_cmap('Greens')
    return cmap(255 * data.get(fips_code, 0) / max(data.values()))

# this converts our data in two steps
# first to Maryland, then to Baltimore City
# this is because I didn't know how FIPS codes worked
# it could be done in one step (just by looking for the 24510 FIPS code start)
# but I didn't redo it, because the FCC data is really large and took a while
if __name__ == '__main__':
    # this full data set is downloaded from the FCC
    full_data_path = 'Fixed_Broadband_Deployment_Data__December_2019.csv'
    md_data_path = 'md_data.csv'
    baltimore_data_path = 'baltimore_data.csv'

    # the dataset is _huge_
    # this runs a one time computation to filter out any non MD data
    if not os.path.exists(md_data_path):
        row_in_md = lambda row: 'State' in row and row['State'] == 'MD'
        filter(full_data_path, row_in_md, md_data_path)

    # it's still pretty large.
    # this filters out any non-Baltimore data
    if not os.path.exists(baltimore_data_path):
        fips_str = 'Census Block FIPS Code'
        row_in_balt = lambda row: fips_str in row and row[fips_str].startswith('24510')
        filter(md_data_path, row_in_balt, baltimore_data_path)

    # at this point, we just have Baltimore city data
    # it's relatively small and easy to work with

    # Notice the Census Block FIPS Code column
    # we can cross reference the FCC data with census blocks
    # this gives us a coverage map

    # the census "shapefiles" are used in GIS settings
    # lets just do a simple matplotlib graph and color them by speed

    # files found at this link:
    # https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

    # the shapefiles are in tl_2020_24_all
    # remove everything without a 24510 to get Baltimore data

    draw_blocks()
    draw_water()

    plt.show()
