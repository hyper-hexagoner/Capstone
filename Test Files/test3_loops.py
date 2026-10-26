def sum_positive(numbers):
    total = 0
    for n in numbers:
        if n > 0:
            total += n
    return total
 
 
result = sum_positive([3, -1, 4, -1, 5])
print(result)
 