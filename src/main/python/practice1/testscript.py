def count_letters(word_list):
    """ See question description """

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    letter_count = {}
    for word in word_list:
        for letter in word:
            letter_count[letter] = letter_count.get(letter, 0) + 1

    max_count = max(letter_count.values())

    for letter, count in sorted(letter_count.items()):  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if count == max_count:
            return letter


print(count_letters(["hello", "world"]))

monty_quote = "listen strange women lying in ponds distributing swords is no basis for a system of government supreme executive power derives from a mandate from the masses not from some farcical aquatic ceremony"

monty_words = monty_quote.split(" ")

print(count_letters(monty_words))
