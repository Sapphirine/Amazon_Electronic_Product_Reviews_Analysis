def grade_count_time(productID,amazon):
    import json
    from datetime import datetime
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    amazon1=amazon.filter(amazon.asin==productID)
    amazon1=amazon1.orderBy("unixReviewTime",ascending=0)
    amazon1_panda = amazon1.toPandas()
    amazon1_panda['datetime'] = pd.to_datetime(amazon1_panda["unixReviewTime"], unit='s')
    amazon1_panda['month']=[str(x)[:7] for x in amazon1_panda['datetime']]
    amazon1_panda_table = pd.pivot_table(amazon1_panda, values='overall', index='month', aggfunc=[np.mean,np.size])
    rtime=pd.date_range(amazon1_panda['datetime'].min(),amazon1_panda['datetime'].max(),freq=pd.tseries.offsets.DateOffset(months=1))
    rating_time=pd.DataFrame()
    rating_time['time']=rtime
    rating_time['month']=[str(x)[:7] for x in rating_time['time']]
    #merge
    amazon1_panda_table = rating_time.join(amazon1_panda_table,how='left', on = ['month'])
    amazon1_panda_table.fillna(0)
    amazon1_panda_table['m_sum']=amazon1_panda_table['size']*amazon1_panda_table['mean']
    avg=list()
    for x in range(len(amazon1_panda_table)):
        t=amazon1_panda_table[:(x+1)]['m_sum'].sum()
        c=amazon1_panda_table[:(x+1)]['size'].sum()
        avg.append(float(t)/c)
    amazon1_panda_table['cum_avg'] = avg    
    amazon1=amazon1_panda_table.reset_index()
    fig,ax1 = plt.subplots()
    ax1.plot(amazon1['time'], amazon1['size'], 'b-',marker = '*', label = 'number of reviews')
    ax1.set_xlabel('time')
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('number of reviews', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ##

    ax1.legend(loc=0)    
    ax2 = ax1.twinx()
    ax2.plot(amazon1.time, amazon1.cum_avg, 'r--', marker = 'o', label = 'scores')
    ax2.set_ylabel('scores', color='r')
    ax2.legend(loc=0)
    ax1.grid()
    for tl in ax2.get_yticklabels():
        tl.set_color('r')


    plt.show()