"""
    This module is for the CSV practice project.
    - Includes tests and solutions for all problem sets
"""
import csv


def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=separator, quotechar=quote)
        return reader.fieldnames


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=separator, quotechar=quote)
        result_list = []
        for row in reader:
            result_list.append(row)
        return result_list


def read_csv_as_nested_dict(filename, key_field, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=separator, quotechar=quote)
        result_dict = dict()
        for row in reader:
            result_dict[row.get(key_field)] = row
        return result_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    """
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, quotechar=quote, quoting=csv.QUOTE_NONNUMERIC,
                                fieldnames=fieldnames, delimiter=separator)
        writer.writeheader()
        for row in table:
            writer.writerow(row)
