batting_statistics = read_csv_as_list_dict(baseballdatainfo["battingfile"], baseballdatainfo["separator"],
                                           baseballdatainfo["quote"])
print(len(batting_statistics))
master_statistics = read_csv_as_list_dict(baseballdatainfo["masterfile"], baseballdatainfo["separator"],
                                          baseballdatainfo["quote"])
filter_test = filter_by_year(batting_statistics, 1871, baseballdatainfo["yearid"])
print(len(filter_test))
print(filter_test)

top_player_ids_test = top_player_ids(baseballdatainfo, batting_statistics,
                                     lambda info, stats: batting_average(info, stats), 5)
print(top_player_ids_test)

player_names_test = lookup_player_names(baseballdatainfo, top_player_ids_test)
print(player_names_test)

aggs_test = aggregate_by_player_id(batting_statistics, baseballdatainfo["playerid"],
                                   baseballdatainfo["battingfields"])
print(aggs_test.get("nonnere01"))