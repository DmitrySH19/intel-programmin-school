def all_eq(lst) -> list:
    new_arr = []
    longest_str = len(max(lst, key=len))
    for string in lst:
        diff = longest_str - len(string)
        print(diff)
        if diff != 0:
            string += '_' * diff
            print(string)
        new_arr.append(string)
    return new_arr

array = ['1234', 's', '','asd']
print(all_eq(array))