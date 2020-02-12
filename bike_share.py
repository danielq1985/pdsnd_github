import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('\nChoose a city: chicago, new york city or washington:  ').lower()

    while city not in ('chicago', 'new york city', 'washington'):
        print('\nPlease enter a valid input.')
        city = input('\nChoose a city: chicago, new york city or washington.').lower()

    # get user input for month (all, january, february, ... , june)
    month = input(
        '\nChoose a month, as an integer. (Example: All, january = 1, february = 2, march = 3, april = 4, may= 5, '
        'june = 6):  ').lower()

    while month not in ('all',  '1', '2', '3', '4', '5', '6'):
        print('\nPlease enter a valid input:  ')
        month = input(
            '\nChoose a month, as an integer. (Example: All, january = 1, february = 2, march = 3, april = 4, may= 5, '
            'june = 6):  ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nChoose a day of the week (All, Sunday, Monday, etc.):  ').lower()

    while day not in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
        print('\nPlease enter a valid input:  ')
        day = input('\nChoose a day of the week (all, Sunday, Monday, etc.):  ').lower()

    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[(df['month'] == int(month))]

    if day != 'all':
        df = df[(df['day_of_week'] == day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_week = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('\n The most popular month: {} \n The most popular day of the week: {} \n The most popular start hour: {} \n' \
          .format(popular_month, popular_week, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    print('\nMost commonly used start station: ', start)
    # display most commonly used end station
    end = df['End Station'].mode()[0]
    print('\nMost commonly used end station: ', end)
    # display most frequent combination of start station and end station trip
    combi = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n Most common Start and End Station combination with count: \n', combi.to_string(header=False))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: ', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time: ', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].reset_index().groupby('User Type').count()
    print('Counts of user types: \n', user_counts)
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].reset_index().groupby('Gender').count()
        print('\nGender counts: \n', gender_counts)
    else:
        print('There is not a Gender column for this data frame.')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_age = df['Birth Year'].min()
        max_age = df['Birth Year'].max()
        avg_age = df['Birth Year'].mean()
        print(
            'Oldest passenger age : {}\nYoungest passenger age : {}\nAverage passenger age: {}'.format(min_age, max_age,
                                                                                                       avg_age))
    else:
        print('There is not a Birth Year column for this data frame.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data_view(df):

    inp = input('If you would like to view raw data, 5 lines at a time, enter yes or no: ').lower()
    while inp not in ('yes', 'no'):
        print('\nPlease enter a valid input.')
        inp = input('If you would like to view raw data, 5 lines at a time, enter yes or no: ').lower()

    if inp == 'yes':
        i = 0
        while True:
            print(df.iloc[i:i + 5].to_string())
            i += 5
            cont = input('Enter Yes to continue. Any other input will terminate scroll.').lower()
            if cont not in 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
