"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    lines = [line1, line2]

    len1 = len(line1)
    len2 = len(line2)

    shortest = 0
    longer = 1
    if len2 > len1:
        shortest = 1
        longer = 0
    else:
        pass

    for idx, char in enumerate(lines[shortest]):
        if char in lines[longer] and char == lines[longer][idx]:
            pass
        else:
            return idx

    return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    if "\n" in line1 or "\n" in line2 or "\r" in line1 or "\r" in line2:
        return ""

    if (line1 == line2) and idx == IDENTICAL:
        return ""

    if idx > len(line2) or idx > len(line1):
        return ""

    if len(line1) >= len(line2):
        len_line1 = len(line1)
        if len_line1 == 0:
            flag = "^"
        else:
            flag = '=' * len(line1)
            flags = list(flag)
            flags[idx] = '^'
            flag = "".join(flags)
            flag = flag[0:flag.index("^")+1]
    else:
        len_line2 = len(line2)
        if len_line2 == 0:
            flag = "^"
        else:
            flag = '=' * len(line2)
            flags = list(flag)
            flags[idx] = '^'
            flag = "".join(flags)
            flag = flag[0:flag.index("^") + 1]

    return line1 + "\n" + flag + "\n" + line2 + "\n"


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    load = [lines1, lines2]
    len1 = len(lines1)
    len2 = len(lines2)

    shortest = 0
    longer = 1
    if len2 < len1:
        shortest = 1
        longer = 0
    else:
        pass

    for ctr, line1 in enumerate(load[shortest]):
        diff = singleline_diff(line1, load[longer][ctr])
        if diff != IDENTICAL:
            return ctr, diff

    if len(lines1) > len(lines2):
        return len(lines2), 0
    if len(lines2) > len(lines1):
        return len(lines1), 0

    return IDENTICAL, IDENTICAL


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file = open(filename, 'rt')
    lines = file.readlines()
    file.close()

    result = []
    for line in lines:
        line = " ".join(line.split())
        result.append(line)
    return result


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)

    result = multiline_diff(lines1, lines2)

    line = result[0]
    idx = result[1]

    if line == IDENTICAL & idx == IDENTICAL & len(lines1) < len(lines2):
        return "Line " + str(line) + ":\n" + singleline_diff_format("", lines2[line], idx)
    if line == IDENTICAL & idx == IDENTICAL & len(lines2) < len(lines1):
        return "Line " + str(line) + ":\n" + singleline_diff_format(lines1[line], "", idx)
    if line == IDENTICAL & idx == IDENTICAL:
        return "No differences\n"

    return "Line " + str(line) + ":\n" + singleline_diff_format(lines1[line], lines2[line], idx)
