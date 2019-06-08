"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


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


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    plot_code_data = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["plot_codes"],
                                             codeinfo["separator"], codeinfo["quote"])
    result = dict()
    for plot_code in plot_code_data:
        world_bank_data = plot_code_data.get(plot_code)
        world_bank_country_code = world_bank_data.get(codeinfo["data_codes"])
        result[plot_code] = world_bank_country_code
    return result


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    not_found_countries = set()
    found_countries = dict()

    country_codes_map = build_country_code_converter(codeinfo)

    for plot_country_code in plot_countries:
        plot_country_code_upper = plot_country_code.upper()
        world_bank_code = country_codes_map.get(plot_country_code_upper)
        gdp_country = gdp_countries.get(world_bank_code, None)
        if gdp_country is None:
            not_found_countries.add(plot_country_code)
        else:
            found_countries[plot_country_code] = world_bank_code
    return found_countries, not_found_countries


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

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
    found_plot_countries = set()
    gdp_values = dict()

    codes_map = {k.upper(): v.upper() for k, v in build_country_code_converter(codeinfo).items()}
    gdp_data = {k.upper(): v for k, v in
                          read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"],
                                                  gdpinfo["separator"], gdpinfo["quote"]).items()}

    for country_code in plot_countries:
        world_bank_code = codes_map.get(country_code.upper())
        country_data = gdp_data.get(world_bank_code)
        if country_data is not None:
            gdp = country_data.get(year, '0')

        if country_data is None:
            not_found_countries.add(country_code)
        elif country_data is not None and gdp is None or gdp == "":
            found_plot_countries.add(country_code)
        else:
            gdp_values[country_code] = math.log10(float(gdp))

    return gdp_values, not_found_countries, found_plot_countries


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for " + year \
                           + " (log scale), unified by common country NAME"
    plot_values = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    gdp_ata = plot_values[0]
    missing = plot_values[1]
    no_data = plot_values[2]
    worldmap_chart.add("GDP for " + year, gdp_ata)
    worldmap_chart.add("Missing from World Bank Data", missing)
    worldmap_chart.add("No GDP Data", no_data)
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"],
                                      gdpinfo["separator"], gdpinfo["quote"])
    print(gdp_data)

    plot_code_data = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["plot_codes"],
                                      codeinfo["separator"], codeinfo["quote"])
    print(plot_code_data)

    data_code_data = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["data_codes"],
                                        codeinfo["separator"], codeinfo["quote"])
    print(data_code_data)

    converted_codes = build_country_code_converter(codeinfo)
    print(converted_codes)
    res1 = reconcile_countries_by_code(codeinfo, pygal_countries, gdp_data)
    print(res1)

    res2 = build_map_dict_by_code(gdpinfo, codeinfo, pygal_countries, "1960")
    print(res2)

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
