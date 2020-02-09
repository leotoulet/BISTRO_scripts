
import pandas as pd
import csv

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

vehicle_fleet_columns = ["agencyId", "routeId", "vehicleTypeId"]
frequency_adjustment_columns = ['route_id', 'start_time', 'end_time', 'headway_secs', 'exact_times']
mode_incentive_columns = ['mode', 'age', 'income', 'amount']
mass_fare_columns = ['agencyId', 'routeId', 'age', 'amount']
road_pricing_columns = ['linkId','toll','timeRange']


#Cordon fare limits
fareLimitX = None
fareLimitY = None
fareP = None


#Circle fare limits
centerx = None
centery = None
cradius = None
centry_toll = None
filepath_network = "/home/ubuntu/settingsFiles/network.csv"

points_x = {"p1_x":None, "p2_x":None, "p3_x":None, "p4_x":None }
points_y = {"p1_y":None, "p2_y":None, "p3_y":None, "p4_y":None }
polygon = []

def convert_to_input(sample, input_dir):
    vehicle_fleet = []
    frequency_adjustment = []
    mode_incentive = []
    mass_fare = []
    road_pricing = []

    for key in sample:
        value = sample[key]
        
        if key.startswith('v'):
            if processV(key, value):
                vehicle_fleet.append(processV(key, value))

        elif key.startswith('r'):
            if processR(key, value):
                frequency_adjustment.append(processR(key, value))

        elif key.startswith('f'):
            road_pricing = road_pricing + processF(key, value)

        elif key.startswith('a'):
            mass_fare.append(processA(key, value))

        #Circle toll
        elif key.startswith('c'):
            road_pricing = road_pricing + processC(key, value)

        #Polygon cordon
        elif key.startswith('p'):
            processP(key, value)

        elif 'income' in key:
            mode_incentive.append(processM(key, value))


    #Once we have all points in polygon, process it
    #polygon = Polygon(polygon)
    #road_pricing += processPolygon()

    vehicle_fleet_d = pd.DataFrame(vehicle_fleet, columns=vehicle_fleet_columns)
    frequency_adjustment_d = pd.DataFrame(frequency_adjustment, columns=frequency_adjustment_columns)
    mode_incentive_d = pd.DataFrame(mode_incentive, columns=mode_incentive_columns)
    mass_fare_d = pd.DataFrame(mass_fare, columns=mass_fare_columns)
    road_pricing_d = pd.DataFrame(road_pricing, columns=road_pricing_columns)

    road_pricing_d.to_csv(input_dir + '/RoadPricing.csv', sep=',', index=False)
    vehicle_fleet_d.to_csv(input_dir+'/VehicleFleetMix.csv', sep=',', index=False)
    frequency_adjustment_d.to_csv(input_dir + '/FrequencyAdjustment.csv', sep=',', index=False)
    mode_incentive_d.to_csv(input_dir + '/ModeIncentives.csv', sep=',', index=False)
    mass_fare_d.to_csv(input_dir + '/MassTransitFares.csv', sep=',', index=False)
    


def processP(key, value):
    #Key format pn_x = val
    if key[3]=="x":
        points_x[key] = value
    else:
        points_y[key] = value


def processPolygon():
    timeRange = '[7:10,16:20]'
    
    global polygon

    for x,y in zip(points_x.values(), points_y.values()):
        if x!= None and y!=None:
            polygon.append((x,y))

    polygon = Polygon(sorted(polygon))

    #Save parameters
    file = open("polygon_params.txt","a")
    for point in polygon.exterior.coords:
        file.write(str(point) + ";")
    file.close()

    changes = []
    i = 0
    for row in load_network():
        if row[0].isdigit():
            i+=1
            linkId,linkLength,fromLocationX,fromLocationY,toLocationX,toLocationY = row[0],row[1],row[-4],row[-3],row[-2],row[-1]
            p1 = Point(float(fromLocationX), float(fromLocationY))
            p2 = Point(float(toLocationX), float(toLocationY))
            if (polygon.contains(p2) and not polygon.contains(p1)):
                changes.append([linkId,3.0,timeRange])
            if (polygon.contains(p1) and not polygon.contains(p2)):
                changes.append([linkId,3.0,timeRange])

            if i%1000  == 0:
                print("Nb links analized : ", i)

    return changes


def processF(key, value):
    timeRange = '[:]'

    global fareLimitX, fareLimitY, fareP

    if key=='fareLimitX':
        fareLimitX = value
    if key=='fareLimitY':
        fareLimitY = value
    if key=='farePriceP':
        fareP = value

    if fareLimitX == None or fareLimitY == None or fareP == None:
        return []

    else:
        print("Parameters for this run: \nFareX: " + str(fareLimitX) + "\nFareY: " + str(fareLimitY) + "\nPrice: " + str(fareP))
        return get_cordon_links(fareLimitX, fareLimitY, fareP, timeRange)


def processC(key, value):

    global centerx, centery, centry_toll, cradius

    if key=='centerx':
        centerx = value
    if key=='centery':
        centery = value
    if key=='cradius':
        cradius = value
    if key=='centry_toll':
        centry_toll = value

    if centerx == None or centery == None or centry_toll == None or cradius == None:
        return []

    else:
        print("Parameters for this run: \nCenterX: " + str(centerx) + "\nCenterY: " + str(centery) + "\nPrice: " + str(centry_toll) + "\nRadius: " + str(cradius))
        links = get_circle_links(centerx, centery, cradius, centry_toll)
        return links


def processV(key, value):
    # 'vehicleType_r1347': 'BUS-SMALL-HD'
    route = key.split('_')[1][1:]
    if value == 'BUS-DEFAULT':
        return None
    return [217, route, value]

def processR(key, value):
    #'r1351_72654_92669': 90,
    values = key.split('_')
    route = values[0][1:]
    start = values[1]
    end = values[2]
    if value:
        head_room = value * 60
        if head_room == 180:
            head_room = head_room + 1
        if head_room == 7200:
            head_room = head_room - 1
    else:
        return None
    return [route, start, end, head_room, 1]

def processA(key, value):
    # 'age1:15': 4.5,
    age = '['+key[3:]+']'
    return [217, '', age, value]


def processM(key, value):
    # 'WALK_TRANSIT_age60:120_income1': 6.5,
    values = key.split('_age')
    mode = values[0]
    age_income = values[1].split('_')
    age = '[' + age_income[0] + ']'
    income_s = age_income[1]
    income = 0
    if income_s == 'income0':
        income = '[0:19999]'
    elif income_s == 'income1':
        income = '[20000:49999]'
    elif income_s == 'income2':
        income = '[50000:99999]'
    elif income_s == 'income3':
        income = '[100000:150000]'
    return [mode, age, income, value]


def load_network():
    with open(filepath_network, "rt") as csvfile:
        datareader = csv.reader(csvfile)
        yield next(datareader)
        for row in datareader:
            yield row
        return


def get_cordon_links(x, y, p, timeRange):
    changes = []
    for row in load_network():
        if row[0].isdigit():
            linkId,linkLength,fromLocationX,fromLocationY,toLocationX,toLocationY = row[0],row[1],row[-4],row[-3],row[-2],row[-1]
            if float(toLocationX) <= x and float(toLocationY) <= y:
                price = 3 #If link enters the cordon, flat fare of 3 dollars
                if float(fromLocationX) <= x and float(fromLocationY) <= y:
                    price = str(round(float(linkLength)*float(p), 2))
                changes.append([linkId,price,timeRange])
    return changes


def get_circle_links(x, y, r, p):
    timeRange = '[:]'
    #timeRange2 = '[57600:72000]'

    #Save parameters
    file = open("circle_params.txt","w")
    file.write("x:" + str(x) + ",y:" + str(y) + ",r:"+str(r) + ",p:" + str(p))
    file.close()

    changes = []
    for row in load_network():
        if row[0].isdigit():
            linkId,linkLength,fromLocationX,fromLocationY,toLocationX,toLocationY = row[0],row[1],row[-4],row[-3],row[-2],row[-1]
            fromLocationX = float(fromLocationX)
            toLocationX = float(toLocationX)
            fromLocationY = float(fromLocationY)
            toLocationY = float(toLocationY)
            dfrom = ((x - fromLocationX)**2 + (y - fromLocationY)**2)**0.5
            dto = ((x - toLocationX)**2 + (y - toLocationY)**2)**0.5
            price = str(round(float(linkLength)*float(p)/1600, 2))

            #if (dfrom > r and dto < r): 
            #    changes.append([linkId,p,timeRange])
            #if (dfrom < r and dto > r):
            #    changes.append([linkId,p,timeRange])
            
            if dfrom < r or dto < r: 
                changes.append([linkId,price,timeRange])

    return changes




input = {'OnDemand_ride_age16:60_income0': 48.5,
 'OnDemand_ride_age16:60_income1': 48.0,
 'OnDemand_ride_age16:60_income2': 20.0,
 'OnDemand_ride_age16:60_income3': 34.0,
 'OnDemand_ride_age1:15_income0': 39.0,
 'OnDemand_ride_age1:15_income1': 20.0,
 'OnDemand_ride_age1:15_income2': 1.5,
 'OnDemand_ride_age1:15_income3': 47.5,
 'OnDemand_ride_age60:120_income0': 41.0,
 'OnDemand_ride_age60:120_income1': 14.5,
 'OnDemand_ride_age60:120_income2': 39.5,
 'OnDemand_ride_age60:120_income3': 2.5,
 'WALK_TRANSIT_age16:60_income0': 17.0,
 'WALK_TRANSIT_age16:60_income1': 8.0,
 'WALK_TRANSIT_age16:60_income2': 21.0,
 'WALK_TRANSIT_age16:60_income3': 47.0,
 'WALK_TRANSIT_age1:15_income0': 44.5,
 'WALK_TRANSIT_age1:15_income1': 41.5,
 'WALK_TRANSIT_age1:15_income2': 41.5,
 'WALK_TRANSIT_age1:15_income3': 26.5,
 'WALK_TRANSIT_age60:120_income0': 35.5,
 'WALK_TRANSIT_age60:120_income1': 6.5,
 'WALK_TRANSIT_age60:120_income2': 25.5,
 'WALK_TRANSIT_age60:120_income3': 49.5,
 'age16:60': 4.0,
 'age1:15': 4.5,
 'age61:120': 1.5,
 'drive_transit_age16:60_income0': 18.0,
 'drive_transit_age16:60_income1': 44.0,
 'drive_transit_age16:60_income2': 24.0,
 'drive_transit_age16:60_income3': 22.5,
 'drive_transit_age1:15_income0': 9.5,
 'drive_transit_age1:15_income1': 18.0,
 'drive_transit_age1:15_income2': 26.0,
 'drive_transit_age1:15_income3': 34.0,
 'drive_transit_age60:120_income0': 26.0,
 'drive_transit_age60:120_income1': 44.5,
 'drive_transit_age60:120_income2': 2.5,
 'drive_transit_age60:120_income3': 10.5,
 'r1340_0_27956': 60,
 'r1340_27956_37625': 90,
 'r1340_37625_59312': 45,
 'r1340_59312_72654': None,
 'r1340_72654_92669': 30,
 'r1341_0_27956': None,
 'r1341_27956_37625': 75,
 'r1341_37625_59312': 5,
 'r1341_59312_72654': 90,
 'r1341_72654_92669': 10,
 'r1342_0_27956': 75,
 'r1342_27956_37625': 30,
 'r1342_37625_59312': 60,
 'r1342_59312_72654': 5,
 'r1342_72654_92669': 30,
 'r1343_0_27956': 90,
 'r1343_27956_37625': 3,
 'r1343_37625_59312': 3,
 'r1343_59312_72654': 75,
 'r1343_72654_92669': 5,
 'r1344_0_27956': 90,
 'r1344_27956_37625': None,
 'r1344_37625_59312': 45,
 'r1344_59312_72654': 90,
 'r1344_72654_92669': 60,
 'r1345_0_27956': 45,
 'r1345_27956_37625': 60,
 'r1345_37625_59312': 10,
 'r1345_59312_72654': 60,
 'r1345_72654_92669': 10,
 'r1346_0_27956': None,
 'r1346_27956_37625': 60,
 'r1346_37625_59312': 120,
 'r1346_59312_72654': 75,
 'r1346_72654_92669': None,
 'r1347_0_27956': 15,
 'r1347_27956_37625': None,
 'r1347_37625_59312': None,
 'r1347_59312_72654': 75,
 'r1347_72654_92669': 75,
 'r1348_0_27956': 60,
 'r1348_27956_37625': 75,
 'r1348_37625_59312': 90,
 'r1348_59312_72654': 5,
 'r1348_72654_92669': 45,
 'r1349_0_27956': 75,
 'r1349_27956_37625': 5,
 'r1349_37625_59312': 10,
 'r1349_59312_72654': 45,
 'r1349_72654_92669': 3,
 'r1350_0_27956': 90,
 'r1350_27956_37625': 3,
 'r1350_37625_59312': 5,
 'r1350_59312_72654': 60,
 'r1350_72654_92669': None,
 'r1351_0_27956': 45,
 'r1351_27956_37625': None,
 'r1351_37625_59312': 3,
 'r1351_59312_72654': 15,
 'r1351_72654_92669': 90,
 'vehicleType_r1340': 'BUS-SMALL-HD',
 'vehicleType_r1341': 'BUS-STD-HD',
 'vehicleType_r1342': 'BUS-STD-ART',
 'vehicleType_r1343': 'BUS-SMALL-HD',
 'vehicleType_r1344': 'BUS-SMALL-HD',
 'vehicleType_r1345': 'BUS-STD-HD',
 'vehicleType_r1346': 'BUS-STD-ART',
 'vehicleType_r1347': 'BUS-SMALL-HD',
 'vehicleType_r1348': 'BUS-DEFAULT',
 'vehicleType_r1349': 'BUS-SMALL-HD',
 'vehicleType_r1350': 'BUS-STD-HD',
 'vehicleType_r1351': 'BUS-SMALL-HD'}

