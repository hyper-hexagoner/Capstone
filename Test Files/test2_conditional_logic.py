score = 72
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
 
if grade != "F":
    passed = True
else:
    passed = False
 
print(grade, passed)
 