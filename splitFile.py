import sys

thisfile = sys.argv[0]
totalfile = sys.argv[1]
outfilename1 = sys.argv[2]
outfilename2 = sys.argv[3]
lines_seen = set()
output1 = open(outfilename1, 'w')
output2 = open(outfilename2, 'w')
count = 0

for line in open(totalfile, 'r'):
    if count % 10 == 0:
        output1.write(line)
    else:
        output2.write(line)
    count += 1;
output1.close()
output2.close()