import time
import pandas as pd
import numpy as np
import calendar
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    city = get_user_input_city()
    # Get user input for month (all, january, february, ... , june).
    month = get_user_input_month()
    # Get user input for day of week (all, monday, tuesday, ... sunday).
    day = get_user_input_weekdays()

    print('-'*40)
    return city, month, day

def get_user_input_city():
    """
    - Get the user's input city name to analyze
    Returns: 
        - city: The city name string
    """
    city_names = ["chicago", "new york city", "washington"] 
    while True:
        city = input("Please input the city name you want to analyze (chicago, new york city, washington): ").strip().lower()
        # City name validation
        if city in city_names:
            return city
        else:
            print("You input wrong city!")

def get_user_input_month():
    """
    - Ask user to input the month to filter:
        + yes: User can input the month string to filter data
        + no: User don't wanna filter data by month
    Returns:
        - month: The month string to filter ("all" for none filter)
    """
    months_validation = list(map(lambda month: month.lower(), calendar.month_name[1:7]))
#     print(months_validation)
    should_filter_month = None
    # Do a loop to get user input month
    while True:
        if should_filter_month:
            if should_filter_month == "yes":
                month = input("Please input the month you want to analyze (all, january, february, ... , june): ").strip().lower()
                if (month in months_validation) or (month == "all"):
                    return month
                else:
                    print("You input wrong month!")
                    
            elif should_filter_month == "no":
                return "all"
            
            else:
                should_filter_month = None
                print("You input wrong answer!")
                
        else:
            should_filter_month = input("Would you like to filter city data by month? (yes/no): ").strip().lower()
    
def get_user_input_weekdays():
    """
    - Ask user to input the weekday to filter:
        + yes: User can input the weekday string to filter data
        + no: User don't wanna filter data by weekday
    Returns:
        - month: The weekday string to filter ("all" for none filter)
    """
    weekdays = list(map(lambda day: day.lower(), calendar.day_name))
#     print(weekdays)
    should_filter_weekday = None
    # Do a loop to get user input week day
    while True:
        if should_filter_weekday:
            if should_filter_weekday == "yes":
                day = input("Please input the day of week you want to analyze (all, monday, tuesday, ... sunday): ").strip().lower()
                if day in weekdays or day == "all":
                    return day
                else:
                    print("You input wrong day!")
                    
            elif should_filter_weekday == "no":
                return "all"
            
            else:
                should_filter_weekday = None
                print("You input wrong answer!")
                
        else:
            should_filter_weekday = input("Would you like to filter city data by week day? (yes/no): ").strip().lower()
        

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
    
    # Load the city dataframe from csv file by city name
    try:
        city_file_name = CITY_DATA.get(city)
        city_dataframe = pd.read_csv(city_file_name)
    except:
        print("There is error while reading file or file not found.")
#     print(city_dataframe)
    city_dataframe['Start Time'] = pd.to_datetime(city_dataframe['Start Time'])
    df = city_dataframe
#     print(f"data to analyze: {city} - month: {month} - day: {day}")
    # Filter the dataframe by month if any
    if month != "all":
        month_number = dt.datetime.strptime(month, "%B").month
        df = city_dataframe[city_dataframe['Start Time'].dt.month == month_number]
#         print("DF after filter month", df)
    # Filter the dataframe by week day if any.
    if day != "all":
        df = city_dataframe[city_dataframe['Start Time'].dt.strftime('%A') == day.title()]
    return df


def display_raw_data(df):
    """Ask user to display the 5 rows of raw-data"""
    start_index = 0
    while start_index < len(df):
        # Check the start index to ask user wanna see '5 lines' or 'next 5 lines' data
        if start_index == 0:
            should_display_data = input('\nWould you like to see 5 lines of raw data? Enter "yes" to continue or "no" to exit: ').lower()
        else:
            should_display_data = input('\nWould you like to see next 5 lines of raw data? Enter "yes" to continue or "no" to exit: ').lower()
            
        if should_display_data == 'yes':
            print(df.iloc[start_index:start_index + 5])
            start_index += 5
        elif should_display_data == 'no':
            print("\nExiting program.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
        

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Extract month and day of week from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.strftime('%A')
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common month.
    months = df['month'].value_counts().idxmax()
    print("The most common month is: {}".format(months))

    # Display the most common day of week.
    days_of_week = df['day'].value_counts().idxmax()
    print("The most common day is: {}".format(days_of_week))

    # Display the most common start hour.
    hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is: {}".format(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    start_station = df['Start Station'].value_counts().index.tolist()
#     print("Start station: ", start_station)
    popular_start_station = start_station[0]
    print("The most popular start station is: ", popular_start_station)

    # Display most commonly used end station.
    end_station = df['End Station'].value_counts().index.tolist()
#     print("End station: ", end_station)
    popular_end_station = end_station[0]
    print("The most popular end station is: ", popular_end_station)

    # Display most frequent combination of start station and end station trip.
    # Group the DataFrame by 'Start Station' and 'End Station', and count the occurrences.
    station_combinations = df.groupby(['Start Station', 'End Station']).size()
    most_frequent_combination = station_combinations.idxmax()
    print("The most frequent combination of start and end stations is: ", most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    # Calculate the travel time (trip duration = end time - start time).
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip duration'] = df['End Time'] - df['Start Time']
    # Calculate the total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: {}".format(total_travel_time))

    # Display mean travel time.
    # Calculate the mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: {}".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_type_counts = df['User Type'].value_counts()
    print("The counts of user types:")
    print(user_type_counts)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("The counts of gender:")
        print(gender_counts)
    except KeyError:
        print("Gender stats cannot be calculated because Gender does not appear in the dataframe")
    except:
        print("Gender stats cannot be calculated because some errors occurred")

    # Display earliest, most recent, and most common year of birth.
    user_stats_birth_year(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats_birth_year(df):
    try:
        # Get earliest birth year.
        earliest_birth_year = int(df['Birth Year'].min())
        # Get the most recent of birth year.
        most_recent_birth_year = int(df['Birth Year'].max())
        # Get the most common birth year.
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("The earliest year of birth is: {}, the most recent year of birth is: {}, the most common year of birth is: {}".format(earliest_birth_year, most_recent_birth_year, most_common_birth_year))
    except KeyError:
        print("Year of birth stats cannot be calculated because Birth Year does not appear in the dataframe")
    except:
        print("Year of birth stats cannot be calculated because some errors occurred")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Display raw data
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
