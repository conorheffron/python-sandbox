"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
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


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    result = list()
    for year in range(gdpinfo["min_year"], gdpinfo["max_year"]+1, 1):
        gdp = gdpdata.get(str(year))
        if gdp != '' and gdp is not None:
            item = tuple((year, float(gdp)))
            result.append(item)
    return result


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                      gdpinfo["separator"], gdpinfo["quote"])
    result = dict()
    for country in country_list:
        country_val = gdpdata.get(country, None)
        if country_val is not None:
            item = build_plot_values(gdpinfo, country_val)
            result[country] = item
        else:
            result[country] = list()

    return result


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    xy_chart = pygal.XY(title="Plot of GDP for select countries spanning 1960 to 2015",
                        x_title="Year",
                        y_title="GDP in current US dollars")
    plot_values = build_plot_dict(gdpinfo, country_list)
    for country in plot_values:
        country_plots = plot_values[0]
        xy_chart.add(country, country_plots)

    xy_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1980,
        "max_year": 2014,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"],
                                      gdpinfo["separator"], gdpinfo["quote"])
    print(gdpdata)

    test_plot_values = build_plot_values(gdpinfo, gdpdata["ALB"])
    print(test_plot_values)

    country_list = list()
    for country_code in gdpdata:
        country = gdpdata.get(country_code)[gdpinfo["country_name"]]
        country_list.append(country)
    country_list.append("Country3")
    print(country_list)
    plot_dict = build_plot_dict(gdpinfo, country_list)
    print(plot_dict)

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()
