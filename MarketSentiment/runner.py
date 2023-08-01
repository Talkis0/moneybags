from dateutil import rrule
from datetime import datetime
from datetime import timedelta
import sys
begin_date = sys.argv[1]
end_date = sys.argv[2] 
dates = [ dt for dt in rrule.rrule( rrule.YEARLY, dtstart=datetime.strptime(begin_date, '%Y%m%d'), until=datetime.strptime(end_date, '%Y%m%d') ) ]
for idx in range( len(dates) - 1 ):
    a = dates[idx].strftime('%Y%m%d')
    b = dates[idx+1].strftime('%Y%m%d')
    print( 'python ./MarketSentiment/stocks_singleTicker.py {} {}'.format( a, b ) )
    print( 'sleep 12' )