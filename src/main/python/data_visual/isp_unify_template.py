"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    not_found_countries = set()
    plot_countries_result = dict()
    for plot_country_code in plot_countries:
        country = plot_countries.get(plot_country_code)
        gdp_country = gdp_countries.get(country, None)
        if gdp_country is None:
            not_found_countries.add(plot_country_code)
        else:
            plot_countries_result[plot_country_code] = gdp_country.get('Country Name')
    return plot_countries_result, not_found_countries


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    not_found_countries = set()
    plot_countries_result = set()
    gdp_values = dict()
    for country_code in plot_countries:
        gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                          gdpinfo["separator"], gdpinfo["quote"])
        country = plot_countries.get(country_code, None)
        country_data = gdpdata.get(country, None)
        if country_data is not None:
            gdp = country_data.get(str(year), '0')
        else:
            gdp = '0'

        if country_data is None:
            not_found_countries.add(country_code)
        elif country_data is not None and gdp is None or gdp == "":
            plot_countries_result.add(country_code)
        else:
            gdp_values[country_code] = math.log10(float(gdp))

    return gdp_values, not_found_countries, plot_countries_result


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for " + year \
                           + " (log scale), unified by common country NAME"
    plot_values = build_map_dict_by_name(gdpinfo, plot_countries, year)
    gdp_ata = plot_values[0]
    missing = plot_values[1]
    no_data = plot_values[2]
    worldmap_chart.add("GDP for " + year, gdp_ata)
    worldmap_chart.add("Missing from World Bank Data", missing)
    worldmap_chart.add("No GDP Data", no_data)
    worldmap_chart.render_to_file(map_file)


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csv_reader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES
    print(pygal_countries)

    gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                      gdpinfo["separator"], gdpinfo["quote"])
    print(gdpdata)

    res1 = reconcile_countries_by_name(pygal_countries, gdpdata)
    print(res1)

    res2 = build_map_dict_by_name(gdpinfo, pygal_countries, 1960)
    print(len(res2[0]))
    print(len(res2[1]))
    print(len(res2[2]))

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
