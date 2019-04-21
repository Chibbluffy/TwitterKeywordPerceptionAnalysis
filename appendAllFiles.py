import sys

thisfile = sys.argv[0]
outfilename = sys.argv[1]
lines_seen = set()
output = open(outfilename, 'w')

for filename in sys.argv:
    if filename != outfilename and filename != thisfile:
        for line in open(filename, 'r'):
            if line not in lines_seen:
                output.write(line)
                lines_seen.add(line)

output.close()