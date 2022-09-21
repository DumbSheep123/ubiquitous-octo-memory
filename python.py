import requests
import time
import termcolor
import tqdm
import pyttsx3
import playsound



engine = pyttsx3.Engine()

engine.setProperty('rate', 150)

#// exit()

COLOR_MAPPING = {
    'RD':termcolor.colored('● RD', 'red'),
    'YL':termcolor.colored('● YL', 'yellow'),
    'GR':termcolor.colored('● GR', 'green'),
    'OR':termcolor.colored('● OR', 'yellow'),
    'BL':termcolor.colored('● BL', 'blue'),
    'SV':'● SV'
}

COLOR_NAMES_MAP = {
    'RD':'red',
    'YL':'yellow',
    'GR':'green',
    'OR':'yellow',
    'BL':'blue',
    'SV':'silver'
}

station_code_mapping = {
    "Addison Road-Seat Pleasant": "G03",
    "Anacostia": "F06",
    "Archives-Navy Memorial-Penn Quarter": "F02",
    "Arlington Cemetery": "C06",
    "Ballston-MU": "K04",
    "Benning Road": "G01",
    "Bethesda": "A09",
    "Braddock Road": "C12",
    "Branch Ave": "F11",
    "Brookland-CUA": "B05",
    "Capitol Heights": "G02",
    "Capitol South": "D05",
    "Cheverly": "D11",
    "Clarendon": "K02",
    "Cleveland Park": "A05",
    "College Park-U of Md": "E09",
    "Columbia Heights": "E04",
    "Congress Heights": "F07",
    "Court House": "K01",
    "Crystal City": "C09",
    "Deanwood": "D10",
    "Dunn Loring-Merrifield": "K07",
    "Dupont Circle": "A03",
    "East Falls Church": "K05",
    "Eastern Market": "D06",
    "Eisenhower Avenue": "C14",
    "Farragut North": "A02",
    "Farragut West": "C03",
    "Federal Center SW": "D04",
    "Federal Triangle": "D01",
    "Foggy Bottom-GWU": "C04",
    "Forest Glen": "B09",
    "Fort Totten": "B06,E06",
    "Franconia-Springfield": "J03",
    "Friendship Heights": "A08",
    "Gallery Pl-Chinatown": "B01,F01",
    "Georgia Ave-Petworth": "E05",
    "Glenmont": "B11",
    "Greenbelt": "E10",
    "Greensboro": "N03",
    "Grosvenor-Strathmore": "A11",
    "Huntington": "C15",
    "Judiciary Square": "B02",
    "King St-Old Town": "C13",
    "L'Enfant Plaza": "D03,F03",
    "Landover": "D12",
    "Largo Town Center": "G05",
    "McLean": "N01",
    "McPherson Square": "C02",
    "Medical Center": "A10",
    "Metro Center": "A01,C01",
    "Minnesota Ave": "D09",
    "Morgan Boulevard": "G04",
    "Mt Vernon Sq 7th St-Convention Center": "E01",
    "Navy Yard-Ballpark": "F05",
    "Naylor Road": "F09",
    "New Carrollton": "D13",
    "NoMa-Gallaudet U": "B35",
    "Pentagon": "C07",
    "Pentagon City": "C08",
    "Potomac Ave": "D07",
    "Prince George's Plaza": "E08",
    "Rhode Island Ave-Brentwood": "B04",
    "Rockville": "A14",
    "Ronald Reagan Washington National Airport": "C10",
    "Rosslyn": "C05",
    "Shady Grove": "A15",
    "Shaw-Howard U": "E02",
    "Silver Spring": "B08",
    "Silver Spring Transit Center": "T81",
    "Smithsonian": "D02",
    "Southern Avenue": "F08",
    "Spring Hill": "N04",
    "Stadium-Armory": "D08",
    "Suitland": "F10",
    "Takoma": "B07",
    "Tenleytown-AU": "A07",
    "Twinbrook": "A13",
    "Tysons Corner": "N02",
    "U Street/African-Amer Civil War Memorial/Cardozo": "E03",
    "Union Station": "B03",
    "Van Dorn Street": "J02",
    "Van Ness-UDC": "A06",
    "Vienna/Fairfax-GMU": "K08",
    "Virginia Square-GMU": "K03",
    "Waterfront": "F04",
    "West Falls Church-VT/UVA": "K06",
    "West Hyattsville": "E07",
    "Wheaton": "B10",
    "White Flint": "A12",
    "Wiehle-Reston East": "N06",
    "Woodley Park-Zoo/Adams Morgan": "A04"
}

print("Line - No. Cars - Dest. - ETA (min.)\n")

iters = 1

for i in range(iters):
    for station_name in station_code_mapping:

        if station_name != "Friendship Heights":
            continue

        time_now = int(time.time())
        station_code = station_code_mapping[station_name]

        response = requests.get(f'https://www.wmata.com/components/stations.cfc?method=getNextTrains&StationCode={station_code}&returnFormat=JSON&_={time_now}')

        print(station_name+':')
        data = response.json()['TRAINS']

        try:
            for line in data[:3]:
                print(COLOR_MAPPING[line['Line']], str(line['Car'])+' cars to', line['Destination'], 'in '+str(line['Min'])+' min.' if line['Min'] not in ['BRD', 'ARR', 'DLY'] else termcolor.colored(f'[{line["Min"]}]', 'green'))
        except KeyError:
            termcolor.cprint('NO DATA!', 'red')
        finally:
            print('\n'*2)


    is_min_no = True
    allow_humor = True
    do_bell = True


    time.sleep(.5)

    try:
        temp = int(data[0]['Min'])
        del temp
    except:
        is_min_no = False

    if is_min_no and allow_humor:
        engine.say(f"There is a, {COLOR_NAMES_MAP[data[0]['Line']]}, line train to, {data[0]['Destination']}, approaching the station in {data[0]['Min']*60000} milliseconds. Please stand back and allow customers to exit. When boarding, please move the the center of the car. Thank you for riding with Washington metropolitan area transit authority.")
    elif is_min_no:
        engine.say(f"There is a, {COLOR_NAMES_MAP[data[0]['Line']]}, line train to, {data[0]['Destination']}, approaching the station in {data[0]['Min']} minutes. Please stand back and allow customers to exit. When boarding, please move the the center of the car. Thank you for riding with Washington metropolitan area transit authority.")
    else:
        engine.say(f"There is a, {COLOR_NAMES_MAP[data[0]['Line']]}, line train to, {data[0]['Destination']}, approaching the station. Please stand back and allow customers to exit. When boarding, please move to the center of the car. Thank you for riding with W M A T A.")
    #engine.say(f"There is a red line train to, shady grove, 4, minutes away. please stand back from the platform edge.")

    engine.runAndWait()
    
    time_delay = 7.5
    tq_str = " " * 100
    
    if i+1 < iters:
        for tq_chr in tqdm.tqdm(tq_str, desc='Next Query'):
            time.sleep(time_delay/len(tq_str))
