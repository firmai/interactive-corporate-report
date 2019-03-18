import pandas as pd
import os
import dash_core_components as dcc


##p = "BJRI"

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_pickle = os.path.join(my_path, "../data//")

"""
df_final_filt = pd.read_csv("comp_f_df.csv")
df_final_one = pd.read_csv("comp_o_df.csv")

df_final = pd.read_csv("comp_df.csv")
df_tick = pd.read_csv("tick_df.csv")
"""

exec = "FirmAI's restaurant report connects up to multiple datasets to provide automated analytics. Among other things, machine learning (AI) tools are " \
       "used to identify the extent to which certain restaurant locations are at risk of closing, to predict the closest competitors and to identify " \
       "a firm's fair valuation. This report makes use of the latest research to identify the sentiment of employees, customers, shareholders and management. " \
       "More than 300 metrics are weighted according to how well they translate into value creation and survivability. This monthly interactive update seeks to provide an exploratory environment " \
       "for some of those metrics. Some of the terms and heading have additional descriptions when you hover over them. "


trends = "All meassures are above six sigma statistical significance. The variables most correlated with firm value" \
         " is employee culture and compensation at the lower ranks of employment. Perceived Upper management competence is not as important as " \
         "lower rank management competence, furthermore, overall customer satisfcation and employee work life balance are also not as " \
         "strongly associated with firm value as the before-mentioned. Customer satisfaction is however an important parameter to " \
         " consider for reasons related to survivability. Customer satisfaction is highly correlated with lower-level " \
         " employee culture and values as well as employees' perception of career opportunities and upward mobility. The chart below is an attempt to" \
         " understand the relationship and variation in measures over time." \
         " Measures are pegged to the management sentiment rating and therefore don't have any absolute meaning. Some values in the chart have further been callibrated to accentuate the trends. " \
         "The search time series is still experimental; it is an attempt to" \
         " gauge the association between firm value and targeted search terms on Google over time. "


social = "The first two tables to the left shows some of the more important social data points gathered to gauge the quality and reception" \
         " of the firm's online public footprint. The last table explores a number of the metrics that can be estimated from the" \
         " before-mentioned data points. Some of the metrics have been normalised for presentation purposes. These metrics and their" \
         " variants account for 7.5% of the final rating.  "

#exec = "BJ's was founded in 1978 and first opened in Orange County, California. By 1996, seven restaurants had opened between San Diego and Los Angeles. Originally known as Chicago Pizza, the company went public about 1996, raising $9.4 million.[1] The company then bought 26 Pietro's Pizza restaurants in March 1996 in a $2.8 million deal in cash and assumed debt, but then sold off seven of the locations with plans to convert the remaining Pietro's to what was then BJ's Pizza.[1] Between 2010 and 2011, the National Retail Federation named it as one of the 10 fastest growing restaurants in the U.S. based on year-over-year sales.[2] BJ’s Restaurants, Inc. owns and operates 192 restaurants of April 2017,[3] located in 24 states of Alabama, Arizona, Arkansas, California, Colorado, F, Nevada, New Jersey, New Mexico."

#

drop_steun = dcc.Markdown('''

#
```
This report updates on a monthly basis to allow the reader to stay up to date with the current issues facing the organisation.
The report is close to fully automated which may lead to potential errors when left unreported. This report loosely serves the
following function:
```

*	Identify the overall sentiment of your firm on multiple dimensions.
*	Identify the extent to which your firm is currently under or overvalued as per qualitative metrics using machine learning techniques.
*	Compare the valuation of your firm against that of close competitors.
*	Get an overview as to which locations are the most as well as the least at risk of closing.
*	Get to understand the different attributes leading to higher customer satisfaction.
*	Get an indication as to how well the company has done for various metrics over time.
*	Gain a deeper insight into how your employee and management cohort compares against industry benchmarks. 
*	Isolate competitor firms using five different algorithmic benchmarks. 
*	Identify the relationship between firm value and employee, customer and manager satisfaction.
*	Identify the top employment regions historically and more recently by analysing open job locations. 
*	Look at different positive and negative sentiment summaries from employees and customers.
*	Get to know the composition of employees such as their level of qualifications, skill and their hierarchical position across different benchmarks. 
*	Identify the level of employee growth among competitors.
*	Understand employee's level of satisfaction with their compensation packages.
*	Survey the surroundings to understand the geographic competitiveness. 
*	Explore the difference in ratings across states and counties.
*	Get an understanding of the sentiment as it relates to different categories.
*	Identify some of the key financial metrics and patterns. 
*	Look at competitor's website and social media stats.
*	Get an understanding of each firm's online footprint and how it changes over time.
*	Get an overall rating of the firm at present and historically to gauge possible future trajectories.
*	Better understand the level of convenience both locally and nationally. 
*	Obtain a better understanding of the interview process and other details.
*	Gauge an understanding of competitor's top products and categorical prices.    


```
The report will grow dynamically over time and eventually become prescriptive.   
```

*	In the future the report would attempt to predict prospective revenue and identify the portion of revenue produced by each competitive location. 
*	Furthermore, the different level of overall firm financial health would be estimated using machine learning techniques. 
*	A further procedure would include the analysis of firm financial filings and financial statement readability along with anomaly detection. 
*	A further 30 novel databases are to be compiled to estimate the level of corporate social responsibility of each firm. 
*	Finally, the creation of an improved valuation model for firms that are not publicly traded and the addition of causal analysis.
*	Any additional forms of analysis as requested by the client. It is likely that for a more granular exploration would require internal data.   


''')