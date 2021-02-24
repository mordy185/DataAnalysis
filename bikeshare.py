import time
import pandas as pd


CITY_DATA = { 'Chicago': 'chicago.csv',
              'NewYorkCity': 'new_york_city.csv',
              'Washington': 'washington.csv' }
'''
in this section we load three Dictionaries for CITY, MONTH , DAY 
from a configuration file in CSV format  using df.to_dict()
'''
LOOKUP_DATA =  'lookup.csv'
df_lookup = pd.read_csv(LOOKUP_DATA, index_col='Lookup_type')
temp = df_lookup[['lookup_id', 'lookup_value']].loc['CITY'].to_dict('split')
dicCITY = dict(temp['data'])
temp = df_lookup[['lookup_id', 'lookup_value']].loc['MONTH'].to_dict('split')
dicMONTH = dict(temp['data'])
temp = df_lookup[['lookup_id', 'lookup_value']].loc['DAY'].to_dict('split')
dicDAY = dict(temp['data'])
#print(dicMONTH)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (Chicago, NewYorkCity, Washington). HINT: Use a while loop to handle invalid inputs
    city, month, day = ['','','']
    while True:
        if not city :
            print('Select the CITY by typing one of the following options: ')
            for item in dicCITY:
                print('{} for {}.'.format(item,dicCITY[item] ))
            cc= input()
            try:
                assert int(cc) in dicCITY
                city = dicCITY[int(cc)]
            except (AssertionError,ValueError) :
                print("YOU SUCK  ")

    # get user input for month (all, january, february, ... , june)
        if  city and not month :
            print('Select the MONTH by typing one of the following options: ')
            for item in dicMONTH:
                print('{} for {}.'.format(item,dicMONTH[item] ))
            mm= input()
            try:
                assert int(mm) in dicMONTH
                month = dicMONTH[int(mm)]
            except (AssertionError,ValueError) :
                print("Invalid Input !!  ")


    # get user input for day of week (all, monday, tuesday, ... sunday)
        if city and month and not day:
            print('Select the DAY by typing one of the following options: ')
            for item in dicDAY:
                print('{} for {}.'.format(item, dicDAY[item]))
            dd = input()
            try:
                assert int(dd) in dicDAY
                day = dicDAY[int(dd)]
            except (AssertionError, ValueError):
                print("Invalid Input !! ")
        if city and month and day :
            break
    #print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print ('-'* 20 +'Loading Data'+ '-'*20)
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])
    df = df.rename(columns={'Start Time': 'StartTime', 'End Time': 'EndTime',
                            'Trip Duration': 'TripDuration', 'Start Station': 'StartStation',
                            'End Station': 'EndStation', 'User Type': 'UserType', 'user_gender':'Gender'})
    # Add Month and Day to the dataframe
    df['DayOfWeek'] = df['StartTime'].dt.day_name()
    df['Month'] = df['StartTime'].dt.month_name()
    df['Hour'] = df['StartTime'].dt.hour
    df.set_index(['Month', 'DayOfWeek','Hour'])
      # data cleansing for Start Station , End Station , Month , Day if All is included
    df[['StartStation','EndStation']].dropna()
    if month == 'All' or  month == '' :
        df['Month'].dropna()
    else:
        df = df.loc[(df['Month'] == month)]
    if day == 'All' or day == '':
        df['DayOfWeek'].dropna()
    else:
        df = df.loc[(df['DayOfWeek'] == day ) ]
    print (str(df.count()[0])+ ' Records Found' )
    print('-'*52)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df[['DayOfWeek', 'Month']].dropna()
    top_month = top_month.groupby(['Month']).size().sort_values(ascending=False)
    maxVal = top_month.iloc[0]
    maxVal = str(top_month[top_month == maxVal].index[0])
    print("the most common Month is: " + maxVal)
    # display the most common day of week
    top_day = df[['DayOfWeek', 'Month']].dropna()
    top_day= top_day.groupby(['DayOfWeek']).size().sort_values(ascending=False)
    maxVal = top_day.iloc[0]
    maxVal = str(top_day[top_day == maxVal].index[0])
    print("the most common day of week is: " + maxVal)

    # display the most common start hour
    top_hour = df[['Hour', 'Month']].dropna()
    top_hour = top_hour.groupby(['Hour']).size().sort_values(ascending=False)
    maxVal = top_hour.iloc[0]
    maxVal = str(top_hour[top_hour == maxVal].index[0]) +":00"
    print("the most common start hour is : " + maxVal)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start = df[['StartStation', 'Month']].dropna()
    # this is another way of doing it using count()
    top_start = top_start.groupby(['StartStation']).count().sort_values(['Month'], ascending=False)
    maxVal = top_start.index[0]
    print("the most common Start Station is : " + maxVal)

    # display most commonly used end station
    top_end = df[['EndStation', 'Month']].dropna()
    # this is another way of doing it using count()
    top_end = top_end.groupby(['EndStation']).count().sort_values(['Month'], ascending=False)
    maxVal = top_end.index[0]
    print("the most common End Station is : " + maxVal)

    # display most frequent combination of start station and end station trip
    top_start_end = df[['StartStation', 'EndStation', 'Month']].dropna()
    # this is another way of doing it using count()
    top_start_end = top_start_end.groupby(['StartStation', 'EndStation']).count().sort_values(['Month'],ascending=False)
    print('Frequent trip from: {} ---to---> {}'.format(top_start_end.index[0][0], top_start_end.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    tot_trips = df[['TripDuration']]
    totVal = tot_trips['TripDuration'].sum()
    print("Total Travel time is : {} Seconds".format(int(totVal)))

    # display mean travel time

    tot_trips = df[['TripDuration']]
    totVal = tot_trips['TripDuration'].mean()
    print("Mean Travel time is : {} Seconds".format(int(totVal)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'UserType' not in df.columns:
        print ("No data Existintg")
    else:
        # Display counts of user types
        user_types = df[['UserType', 'Month']].dropna()
        user_types = user_types.groupby(['UserType']).size().sort_values(ascending=False)
        print(user_types.to_string()+"\n")
        #maxVal = str(top_end[top_end == maxVal].index[0])
        #print("the most common End Station is : " + maxVal)

        # Display counts of gender

        if 'Gender' not in df.columns:
            print("No data Existintg")
        else:
            user_gender = df[['Gender', 'Month']].dropna()
            user_gender = user_gender.groupby(['Gender']).size().sort_values(ascending=False)
            print(user_gender.to_string())

    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    '''city, month, day = get_filters()
    df = load_data(city, month, day)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
'''
          #
          #
          #
          ######
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
