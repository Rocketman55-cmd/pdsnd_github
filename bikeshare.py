import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    # Pick a city until the input equals washington, new york city, or chicago
    city = input("Pick a city: ")
    while (city.lower() != 'washington' and city.lower() != 'new york city' and city.lower() != 'chicago'):
        city = input("Pick a city: ")

    # Pick a month until the input equals all or any month from january to june
    month = input("Pick a month: ")
    while (month.lower() != 'all' and month.lower() != 'january' and month.lower() != 'february' and month.lower() != 'march' and month.lower() != 'april' and month.lower() != 'may' and month.lower() != 'june'):
        month = input("Pick a month: ")

    # Pick a day until the input equals all or any day of the week    
    day = input("Pick a day: ")
    while (day.lower() != 'all' and day.lower() != 'sunday' and day.lower() != 'monday' and day.lower() != 'tuesday' and day.lower() != 'wednesday' and day.lower() != 'thursday' and day.lower() != 'friday' and day.lower() != 'saturday'):
        day = input("Pick a day: ")
    city = city.lower()
    month = month.lower()
    day = day.lower()
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df): 
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # find the most common month
    popular_month = df['month'].mode()[0]
    # find the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour
    popular_hour = df['hour'].mode()[0]
    
    print('\nMost Common Month:', popular_month)
    print('\nMost Common Day of Week:', popular_day)
    print('\nMost Common Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_Start = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_End = df['End Station'].mode()[0]

    # Combine start and end station into one column: total trip station 
    df['Total Trip Station'] = df['Start Station'] + '-' + df['End Station']
    
    # display most frequent combination of start station and end station trip
    frequent = df['Total Trip Station'].mode()[0]
    
    print('\nMost Common Start Station:', popular_Start)
    print('\nMost Common End Station:', popular_End)
    print('\nMost Common Start and End Station Combination:', frequent)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    
    print('\nThe total travel time:', total_time)
    print('\nThe mean travel time:', mean_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        popular_user = df['User Type'].dropna().mode()[0]
        print('\nMost Common User Type:', popular_user)
    # Display counts of gender
    if 'Gender' in df:
        popular_gender = df['Gender'].dropna().mode()[0]
        print('\nMost Common Gender:', popular_gender)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        popular_birth = df['Birth Year'].dropna().mode()[0]
        print('\nMost Common Birth Year:', popular_birth)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays five lines of data until users says no."""
    # raw is set to yes
    raw = 'yes'
    run = 0
    # while loop continues until user says no
    while raw == 'yes':
        for index, row in df.iterrows():
            if raw.lower() == 'no':
                break
            # if yes, print five lines of raw data
            if raw.lower() == 'yes':
                print(row) 
                run += 1 
            # if user wants to see more data, run has to reset for five more lines
            if run == 5:
                raw = input('\nWould you like to see some more data? Enter yes or no.\n')
                run = 0
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
                  
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # prompts user if they want to see some raw data
        raw = input('\nWould you like to see some data? Enter yes or no.\n')
        # if yes, then go to the raw_data function 
        if raw.lower() == 'yes':
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
