# TwitterKeywordPerceptionAnalysis
1. install requirements
`pip install -r requirements.txt`
2. run tweets.py
	[Optional]: Run multiple times on multiple terms, just change terms in code and output file name
`python tweets.py`
3. run helper files on tweets if desired, and convert them to json format
`python removeDupeLines.py <inputfile> <outputfile>`
`python appendAllFiles.py <outputfile> <inputfile1> <inputfile2> <inputfilex>`
4. run analyzer
`python analyzer.py <inputfile>`
	[Optional]: Change analyzer.py to print out categorization predictions if desired.
