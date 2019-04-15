import sys

filename = sys.argv[1]
if len(sys.argv) == 3:
    outfilename = sys.argv[2]
else:
    outfilename = sys.argv[1]
# filename = "Companies.txt"
# outfilename = "CompanyList.txt"

lines_seen = set()
output = open(outfilename, 'w')
for line in open(filename, 'r'):
    if line not in lines_seen:
        output.write(line)
        lines_seen.add(line)
output.close()