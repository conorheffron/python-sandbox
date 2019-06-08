import isp_diff_template as idp


FILES_PATH = "isp_diff_files/"

# res1 = idp.singleline_diff("testing1", "test")
# print(res1)
# res2 = idp.singleline_diff("testing1", "testing1")
# print(res2)
#
# res3 = idp.singleline_diff('aba', 'abb')
# print(res3)
#
# res4 = idp.singleline_diff_format('aba', 'abb', res3)
# print(res4)
#
# res5 = idp.singleline_diff_format('', 'a', 0)
# print(res5)
#
# res6 = idp.singleline_diff_format('a', 'ab', 1)
# print(res6)
#
# res7 = idp.singleline_diff_format('abcd', 'abcd', -1)
# print(res7)
#
# res8 = idp.singleline_diff_format('abcdefg', 'abc', 5)
# print(res8)
#
# res9 = idp.singleline_diff_format('abc', 'abcdefg', 5)
# print(res9)
#
# res10 = idp.multiline_diff(['line1', 'line2'], ['line1', 'line2', 'line3'])
# print(res10)
#
# res11 = idp.get_file_lines(FILES_PATH+'file1.txt',)
# print(res11)
#
# res12 = idp.file_diff_format(FILES_PATH+'file1.txt', FILES_PATH+'file2.txt')
# print(res12)

res13 = idp.file_diff_format(FILES_PATH+'file1.txt', FILES_PATH+'file2.txt')
print(res13)

res14 = idp.multiline_diff(['line1', 'line2'], ['line1', 'line2', 'line3'])
print(res14)
