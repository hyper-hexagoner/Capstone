def read_numbers(path):
    numbers = []
    try:
        for line in open(path):
            line = line.strip()
            if line:
                numbers.append(int(line))
    except FileNotFoundError:
        print("missing file")
    return numbers
 
 
def average(values):
    total = 0
    for v in values:
        total += v
    if len(values) == 0:
        return 0
    return total / len(values)
 
 
def report(path):
    data = read_numbers(path)
    mean = average(data)
    print("count:", len(data))
    print("mean:", mean)
    return mean
 
 
if __name__ == "__main__":
    report("scores.txt")
    
 