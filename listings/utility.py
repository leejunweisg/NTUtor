import requests
from .models import Module

# populate module model
def fetch_modules():
    url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1'
    params = {'r_search_type': 'F',
            'boption': 'Search',
            'acadsem': '2020;2',
            'r_subj_code': '',
            'staff_access': 'false'}

    try:
        x = requests.post(url, data = params)
        with open('response.html', 'w') as f:
            f.write(x.text)
    except:
        print("Something went wrong...")
        return False

    return True

def populate_modules():
    # parse html file of course details into dictionary
    try:
        with open('response.html') as f:
            contents = f.readlines()
    except:
        print("Something went wrong opening 'response.html")
        return False

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
            temp = temp.replace('#', '')
            temp = temp.replace('^', '')
            names.append(temp)

    # add to model
    created = 0
    not_created = 0
    for i in range(len(codes)):
        result = Module.objects.get_or_create(moduleCode=codes[i], moduleName=names[i])[1]
        if result:
            created += 1
        else:
            not_created += 1
        
    print(f"Created: {created}, not created: {not_created}")
    return True