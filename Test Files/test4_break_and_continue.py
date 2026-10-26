def first_negative(xs):
    for x in xs:
        if x < 0:
            break
    else:
        return None
    return x
 
 
def count_down(start):
    count = start
    while count > 0:
        count -= 1
        if count == 3:
            continue
        print(count)
    return count
 
 
print(first_negative([2, 5, -3, 8]))
print(count_down(6))
 