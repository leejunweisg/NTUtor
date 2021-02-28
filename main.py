import requests

url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1'
myobj = {'r_search_type': 'F',
        'boption': 'Search',
        'acadsem': '2020;2',
        'r_subj_code': '',
        'staff_access': 'false'
}

x = requests.post(url, data = myobj)

print('Response received, writing...')

with open('response.html', 'w') as f:
    f.write(x.text)
