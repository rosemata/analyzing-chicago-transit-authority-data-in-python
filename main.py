#######################################################
# Project : Analyzing CTA data in Python
# Owner : Roselle Mata
# Overview : console-based Python program that inputs commands from the user and outputs data from the CTA2 L daily ridership database
#######################################################
import sqlite3
import matplotlib.pyplot as figure

###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    # prints total number of stations
    dbCursor.execute("Select count(*) From Stations;")
    total_stations = dbCursor.fetchone();
    print("  # of stations:", f"{total_stations[0]:,}")

    # prints total number of stops
    dbCursor.execute("Select count(*) From Stops;")
    total_stops = dbCursor.fetchone();
    print("  # of stops:", f"{total_stops[0]:,}")

    # prints total number of ride entries
    dbCursor.execute("Select count(*) From Ridership;")
    total_ride_entries = dbCursor.fetchone();
    print("  # of ride entries:", f"{total_ride_entries[0]:,}")

    # prints the start date and latest date of database
    dbCursor.execute("Select date(Ride_Date) From Ridership")
    start_date = dbCursor.fetchone();
    dbCursor.execute("Select date(Ride_Date) From Ridership Order by Ride_Date desc")
    latest_date = dbCursor.fetchone();
    print(f"  date range: {start_date[0]} - {latest_date[0]}");

    # prints total ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    total_ridership = dbCursor.fetchone();
    print("  Total ridership:", f"{total_ridership[0]:,}")

    # prints weekly ridership and it's percentage
    dbCursor.execute("select sum(Num_Riders) From Ridership Where Type_of_Day = 'W'")
    row = dbCursor.fetchone();
    print("  Weekday ridership:", f"{row[0]:,}", f"({row[0]/total_ridership[0]*100:.2f}%)") 

    # prints saturday ridership and it's percentage
    dbCursor.execute("select sum(Num_Riders) From Ridership Where Type_of_Day = 'A'")
    row = dbCursor.fetchone();
    print("  Saturday ridership:", f"{row[0]:,}", f"({row[0]/total_ridership[0]*100:.2f}%)") 

    # # prints holiday/sunday ridership and it's percentage
    dbCursor.execute("select sum(Num_Riders) From Ridership Where Type_of_Day = 'U'")
    row = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({row[0]/total_ridership[0]*100:.2f}%)") 
    print()
    
###########################################################  
#
# func_one
#
# User will input station name using %, _, or full name
# SQL queries will output Station Name/s that are like the user's input
#
def func_one(dbConn):
  print()
  dbCursor = dbConn.cursor()
  variable = input("Enter partial station name (wildcards _ and %): ")
  sql = f"""select Station_ID, Station_Name From Stations Where Station_Name like '{variable}' Order by Station_Name asc"""
  dbCursor.execute(sql);
  station_name = dbCursor.fetchall();

  if len(station_name) == 0:
    print("**No stations found...")
    return;

  for each in station_name:
    print(f"{each[0]} : {each[1]}")

###########################################################  
#
# func_two
#
# SQL queries will output ridership at each station, in ascending order by station namme
# SQL queries will output the percentage which represents across the total L ridership
#
def func_two(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **")

  dbCursor.execute("select sum(Num_Riders) from Ridership;")
  total_riders = dbCursor.fetchone();

  dbCursor.execute("select Station_Name, sum(Num_Riders) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID group by Station_Name order by Station_Name ASC;")

  rows = dbCursor.fetchall();
  for each in rows:
    print(f"{each[0]} : {each[1]:,}", f"({each[1]/total_riders[0]*100:.2f}%)") 

###########################################################  
#
# func_three
#
# SQL queries will output top-10 busiest stations in descending order
# 
#
def func_three(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **")

  dbCursor.execute("select sum(Num_Riders) from Ridership;")
  total_riders = dbCursor.fetchone();

  dbCursor.execute("select Station_Name, sum(Num_Riders) From Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Group by Station_Name Order by sum(Num_Riders) desc Limit 10;")

  rows = dbCursor.fetchall();
  for each in rows:
    print(f"{each[0]} : {each[1]:,}", f"({each[1]/total_riders[0]*100:.2f}%)")

###########################################################  
#
# func_four
#
# SQL queries will output top-10 least busiest stations in ascending order
# 
#
def func_four(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **")


  dbCursor.execute("select sum(Num_Riders) from Ridership;")
  total_riders = dbCursor.fetchone();

  dbCursor.execute("select Station_Name, sum(Num_Riders) From Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Group by Station_Name Order by sum(Num_Riders) asc Limit 10;")

  rows = dbCursor.fetchall();
  for each in rows:
    print(f"{each[0]} : {each[1]:,}", f"({each[1]/total_riders[0]*100:.2f}%)")
    

###########################################################  
#
# func_five
#
# User will input color of the station
# SQL queries will output all stop names that are part of the linex
# will output direction, and wether it's accesible or not
#
def func_five(dbConn):
  print()
  dbCursor = dbConn.cursor()
  variable = input('Enter a line color (e.g. Red or Yellow): ')

  variable = variable.title()

  sql = f"""select Stop_Name, Direction, ADA from Lines join StopDetails on Lines.Line_ID = StopDetails.Line_ID join Stops on StopDetails.Stop_ID = Stops.Stop_ID where Color = '{variable}' Order by Stop_Name asc"""
  
  dbCursor.execute(sql);
  station_name = dbCursor.fetchall();

  if len(station_name) == 0:
    print("**No such line...")

  else:
    for each in station_name:
      if (each[2] == 1):
        var2 = 'yes'
      else:
        var2 = 'no';

      print(f"{each[0]} : direction = {each[1]} (accessible? {var2})")

###########################################################  
#
# func_six
#
# SQL queries will output total ridership by month, ascending order
# User will input y (plot the data) or n (not to plot the data)
#
# 
def func_six(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by month **")

  sql = f"""SELECT strftime('%m', Ride_Date), sum(Num_Riders) FROM Ridership GROUP BY strftime('%m', Ride_Date) ORDER BY strftime('%m', Ride_Date) ASC """

  dbCursor.execute(sql)
  results = dbCursor.fetchall()

  # Display results
  for result in results:
      print(f"{result[0]} : {result[1]:,}")
  print()

  command = input("Plot? (y/n) ")

  if (command == "y"):
    x = []
    y = []

    for result in results:
      x.append(result[0])
      y.append(result[1])
    
    figure.xlabel("x")
    figure.ylabel("number of riders(x * 10^8)")
    figure.title("monthly ridership")

    figure.plot(x,y)
    figure.show()
    figure.close()


###########################################################  
#
# func_seven
#
# SQL queries will output total ridership by year, ascending order
# User will input y (plot the data) or n (not to plot the data)
#
# 
def func_seven(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by year **")

  sql = f"""SELECT strftime('%Y', Ride_Date), sum(Num_Riders) FROM Ridership GROUP BY strftime('%Y', Ride_Date) ORDER BY strftime('%Y', Ride_Date) ASC """

  dbCursor.execute(sql)
  results = dbCursor.fetchall()

  # Display results
  for result in results:
      print(f"{result[0]} : {result[1]:,}")
  print()

  command = input("Plot? (y/n) ")

  if (command == "y"):
    x = []
    y = []

    for result in results:
      x.append(result[0])
      y.append(result[1])
    
    figure.xlabel("x")
    figure.ylabel("number of riders(x * 10^8)")
    figure.title("yearly ridership")

    figure.plot(x,y)
    figure.show()
    figure.close()
###########################################################  
#
# func_eight
#
# SQL queries will output total ridership by year, ascending order
# User will input y (plot the data) or n (not to plot the data)
#
# 
def func_eight(dbConn):
  print()
  dbCursor = dbConn.cursor()

  year = input("Year to compare against? ")
  print()
  station1 = input("Enter station 1 (wildcards _ and %): ")
  # Station1
  sql = "select Station_ID, Station_Name From Stations Where Station_Name like ?"
  dbCursor.execute(sql, [station1]);
  total_station1 = dbCursor.fetchall();

  if len(total_station1) > 1:
    print("**Multiple stations found...")
    return;

  if len(total_station1) == 0:
    print("**No station found...")
    return;
  print()
  station2 = input("Enter station 2 (wildcards _ and %): ")
  # Station2
  sql = "select Station_ID, Station_Name From Stations Where Station_Name like ?"
  dbCursor.execute(sql, [station2]);
  total_station2 = dbCursor.fetchall();

  if len(total_station2) > 1:
    print("**Multiple stations found...")
    return;

  if len(total_station2) == 0:
    print("**No station found...")
    return;
    
  # Station1
  sql = "select Station_ID, Station_Name From Stations Where Station_Name like ?"
  dbCursor.execute(sql, [station1]);
  total_station1 = dbCursor.fetchone();

  print(f"Station 1: {total_station1[0]} {total_station1[1]}")

  var = total_station1[0]

  sql = f"""select date(Ride_Date), Num_Riders from Ridership where strftime('%Y', Ride_Date) = '{year}' and Station_ID = '{var}' group by Ride_Date order by Ride_Date asc"""
  dbCursor.execute(sql);
  daily_ridership = dbCursor.fetchall();

  # First 5 results
  for i in range(0,5):
    print(f"{daily_ridership[i][0]} {daily_ridership[i][1]}")
  
  # Last 5 results
  for i in range(len(daily_ridership)-5, len(daily_ridership)):
    print(f"{daily_ridership[i][0]} {daily_ridership[i][1]}")

  # Station2
  sql = "select Station_ID, Station_Name From Stations Where Station_Name like ?"
  dbCursor.execute(sql, [station2]);
  total_station2 = dbCursor.fetchone();

  print(f"Station 2: {total_station2[0]} {total_station2[1]}")

  var = total_station2[0]

  sql = f"""select date(Ride_Date), Num_Riders from Ridership where strftime('%Y', Ride_Date) = '{year}' and Station_ID = '{var}' group by Ride_Date order by Ride_Date asc"""
  dbCursor.execute(sql);
  daily_ridership2 = dbCursor.fetchall();

  # First 5 results
  for i in range(0,5):
    print(f"{daily_ridership2[i][0]} {daily_ridership2[i][1]}")
  
  # Last 5 results
  for i in range(len(daily_ridership2)-5, len(daily_ridership2)):
    print(f"{daily_ridership2[i][0]} {daily_ridership2[i][1]}")
  print()
  command = input("Plot? (y/n) ")

  if (command == "y"):
    x = []
    y = []

    x2 = []
    y2 = []

    for result in daily_ridership:
      x.append(result[0])
      y.append(result[1])

    for result in daily_ridership2:
      x2.append(result[0])
      y2.append(result[1])

    figure.xlabel("day")
    figure.ylabel("number of riders")
    figure.title("riders each day of 2020")

    figure.plot(x,y)
    figure.plot(x2,y2)
    figure.show()
  

###########################################################  
#
# func_nine
# 
# User will input line color
# SQL queries will output distinct(Station_Name), Latitude, Longitude 
# User will have the option to plot (y) or not plot (n)
#
def func_nine(dbConn):
  print()
  dbCursor = dbConn.cursor()
  color = input("Enter a line color (e.g. Red or Yellow): ");
  color = color.title();

  sql = f"""select distinct(Station_Name), Latitude, Longitude from Stations join Stops on Stations.Station_ID = Stops.Station_ID join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID join Lines on StopDetails.Line_ID = Lines.Line_ID where Color = '{color}' group by Station_Name order by Station_Name asc""";

  dbCursor.execute(sql);
  results = dbCursor.fetchall();

  if len(results) == 0:
    print("**No such line...")
    return

  for result in results:
      print(f"{result[0]} : ({result[1]}, {result[2]})")

  print()
  command = input("Plot? (y/n) ")

  if (command == "y"):

    x = []
    y = []

    for result in results:
      y.append(result[1])
      x.append(result[2])

    image = figure.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)

    # -- Orange
    # -- Pink
    # -- Purple
    # -- Purple-Express
    # -- Red
    # -- Yellow

    figure.title(color+ " line")
    if (color.lower() == "yellow"):
      color = "Yellow"
    if (color.lower() == "purple-express"):
      color = "Purple"
    if (color.lower() == "blue"):
      color = "Blue"
    if (color.lower() == "brown"):
      color = "Brown"
    if (color.lower() == "green"):
      color = "Green"
    if (color.lower() == "orange"):
      color = "Orange"
    if (color.lower() == "pink"):
      color = "Pink"
    if (color.lower() == "red"):
      color = "Red"
    if (color.lower() == "purple"):
      color = "Purple"

    figure.plot(x, y, "o", c=color)
    for each in results:
      figure.annotate(each[0], {each[2], each[1]})
    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])
    figure.show()
###########################################################  
#
# main
# user interface
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
a = 1
variable = ' '
while variable != 'x':
  variable = input('Please enter a command (1-9, x to exit): ')
  if variable == "1":
    func_one(dbConn)
  elif variable == "2":
    func_two(dbConn)
  elif variable == "3":
    func_three(dbConn)
  elif variable == "4":
    func_four(dbConn)
  elif variable == "5":
    func_five(dbConn)
  elif variable == "6":
    func_six(dbConn)
  elif variable == "7":
    func_seven(dbConn)
  elif variable == "8":
    func_eight(dbConn)
  elif variable == "9":
    func_nine(dbConn)
  elif variable == "x":
    break
  else:
    print('**Error, unknown command, try again...')
  print()
