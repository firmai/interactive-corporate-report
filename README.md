# 4D Report
For a sampled version of the report (webapp) see [**FirmAI Report**](http://report.firmai.org).

This report endeavours to provide ratings of four corporate dimensions: employees, customers, shareholders and management, as benchmarked against competitors. It also shows the change in ratings over time. The competitors are automatically identified from the data using statistical distance metrics.

This report consists of Programmatic Competitor Analysis, NLP Sentiment Analysis, NLP Summarisation, ML Time Series and Cross-Section Prediction (Valuation, Closures, Geographic Opportunity), Employee Growth and Qualifications Measures, Location Ratings, Rating Growth, Social Media Analytics, Compensation Satisfaction Analysis, Interview Analysis, Product Analysis and Financial PCA. It is my hope that this report, analysis, generated data and scraping scripts (in functionality folder), will benefit smaller firms who do not necessarily have access to this technology stack.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_CE83DB4FA505DA9E22D78608D2D9724ABB207FCF67EC0D449DDCF275FD745057_1530937036816_file.png)

## Description

The report is built out of a [Dash](https://plot.ly/products/dash/) example. It is fully automated and updates on a monthly basis. It allows companies to study multiple competitors and company locations without strenuous user input. It is the first interactive report of its kind. It is in PDF style, making it easily digestible and also easy to print for meetings.

All information is extracted from the public domain using modern programming tools. This report uses state of the art machine learning and natural language processing techniques for deep sentiment analysis and prediction tasks. The report looks analysis a company’s from four dimensions, being the employees, customers, shareholders (owners) and management. Information is gathered from numerous online sources, the majority of which do not sit behind pay-walls. This report serves the following functions.


- Identify the overall sentiment of your firm on the before-mentioned dimensions.
- Identify the extent to which your firm is currently under or overvalued as per qualitative and quantitative metrics using machine learning.
- Compare the valuation of your firm against that of close competitors, and programatically identify close competitors.
- Get an overview as to which locations are the most and least at risk of closing using inbuilt machine learning tools.
- Get to understand the different attributes leading to higher customer satisfaction.
- Get an indication as to how well the company has done by following various metrics over time.
- Gain a deeper insight into how your employee and management cohort compares against industry benchmarks.
- Isolate competitor firms using five different algorithmic benchmarks.
- Identify the relationship between firm value and three machine learning satisfaction ratings (employee, customer and manager satisfaction).
- Identify the top employment regions historically and more recently by analysing open job locations.
- Look at different positive and negative sentiment summaries from employees and customers as identified with natural language processing tools.
- Get to know the composition of employees such as their level of qualifications, skill and their hierarchical position across different benchmarks.
- Identify the level of employee growth among competitors.
- Understand employee's level of satisfaction with their compensation packages.
- Survey the surroundings to understand the geographic competitiveness.
- Explore the difference in ratings across states and counties.
- Get an understanding of the sentiment as it relates to different categories.
- Identify some of the key financial metrics and patterns leading to company success.
- Compare competitor's website and social media stats.
- Get an understanding of each firm's online footprint and how it changes over time.
- Get an overall rating of the firm at present and historically to gauge possible future rating changes.
- Gain a better understanding of customers both locally and nationally.
- Obtain a better understanding of the interview process and other details.
- Identify competitor's top products and categorical prices.


## Report

The report will grow dynamically over time and eventually become more prescriptive in nature.

- In the future the report would attempt to predict prospective revenue and identify the portion of revenue generated from each location.
- Furthermore, the different level of overall firm financial health would be estimated using machine learning techniques.
- A further procedure would include the analysis of firm financial filings and financial statement readability along with anomaly detection.
- A further 30 novel databases are to be compiled to estimate the level of corporate social responsibility of each firm.
- Finally, the creation of an improved valuation model for firms that are not publicly traded and the addition of causal analysis.
- Any additional forms of analysis as requested by the client. It is likely that for a more granular exploration would require internal data.

**Running Your Own**

- Download Repository
- Run scrapers with setup.py (only if you want to generate new data)
- Install dependencies in requirements.txt
- Run main.py
- Note, this repository is big (4GB), it already contains data

