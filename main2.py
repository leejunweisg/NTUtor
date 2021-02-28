# parse html file of course details into dictionary
with open('response.html') as f:
    contents = f.readlines()

# extract course codes and course names
codes = []
names = []
for line in contents:
    if line.startswith('<TD WIDTH="100"><B><FONT COLOR=#0000FF>'):
        codes.append(line[39:39+6])
    elif line.startswith('<TD WIDTH="500"><B><FONT COLOR=#0000FF>'):
        temp = line
        temp = temp.replace('<TD WIDTH="500"><B><FONT COLOR=#0000FF>','')
        temp = temp.replace('</FONT></B></TD>','')
        temp = temp.replace('*', '')
        names.append(temp)


print(len(codes))
print(len(names))

