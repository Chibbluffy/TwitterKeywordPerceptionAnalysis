filename = "Companies.txt"
outfilename = "CompanyList.txt"
lines_seen = set()
output = open(outfilename, 'w')
for line in open(filename, 'r'):
    if line not in lines_seen:
        output.write(line)
        lines_seen.add(line)
output.close()