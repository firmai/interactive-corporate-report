
import dash_core_components as dcc
import dash_html_components as html
import _pickle as pickle
import os
import pandas as pd

#### NB the requirement for snapshot_layout is app_processing.py it should not be called
## upon by the dictionary as it is not that involved in user interaction.

def social_dic(coy, bench):


    ## This one is indeed going to require a dictionary for the mere reason that it
    ## has some involved huma interaction.

    fb_measures = ["","All hitstorical FB likes the firm has received in thousands.",
                   "All historical checkins from FB in thousands",
    "All photos posted by users on the FB page, indicative of true customer support and experience. ",
    "The number of posts the firm posted within the last quarter.",
    "The number of quarterly reactions to firms posts.",
    "The number of comments on the firm's quarterly posts.",
    "The number of quarterly shares to firms posts.",
    "The proportion of posts dedicated to photos in the last quarter.",
    "The proportion of posts dedicated to videos in the last quarter.",
    "The proportion of posts dedicated to events in the last quarter.",
    "The proportion of posts dedicated to text statuses in the last quarter."]


    other_media = ["","The number of twitter followers no related to like and following velocity.",
    "The number of ratings used to calculate food quality measures.",
    "The number of employees with Linkedin accounts.",
    "The number of Glassdoor datapoints/reviews available for analysis. ",
    "The number of Yelp reviews available across all firms.",
    "The number of Instagram posts by the firm.",
    "The number of instagram followers.",
    "The number of tweets made by the firm.",
    "The number of people followed by the firm.",
    "The number of followers the firm have.",
    "The number of likes given by the firm."]


    ratio_rating = ["","This is a combination of Glassdoor and Linkedin information to estimate how active employees are online. How willing they are to express their opinion online. This is a simple ratio.",
    "This measure identifies a rough estimate of how many customers to the number of employees. This is a measure out of five.",
    "This measure identifies the quality of posts by identifying the ratio of comments and shares to the number of reactions.",
    "Marketing effectiveness is an important measure that seeks to idnetify the association between all social media marketing attempts and the amount of customers obtained through the checkins measure.",
    "Photo Worthiness identifies a ratio related to the likelihood of a customer taking a photo inside your restaurant and sharing it, this can be indicative of good food a good brand, or good internal presentation. ",
    "Photo Effect measures the effectiveness of photo ads and media to attract customer interaction. ",
    "Video Effect measures the effectiveness of video ads and media to attract customer interaction. ",
    "Event Effect measures the effectiveness of event ads and media to attract customer interaction. ",
    "Status Effect measures the effectiveness of text ads and media to attract customer interaction. ",
    "Best post highlights the best post of the quarter and offers a link to that post. ",
    "Facebook focus is a percentage that identifies whether the firm is over or underweight in their social media strategy. Generally a number higher than 85% is indicative of a company focusing too much on FB as opposed to other social media channels."]





    def make_dash_table_metrics(df,descriptors):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        tol = -1
        for row, ad in zip(df.itertuples(index=True, name='Pandas'),descriptors):
            print(row)
            tol = tol + 1
            html_row = []
            for i in range(len(row)-1):
                i = i +1
                if len(str(row[i]))<40:
                    html_row.append(html.Td([row[i]]))
                else:
                    print(i)
                    bore = html.A("link",href=row[i],target="_blank")
                    html_row.append(html.Td([bore]))
            table.append(html.Tr(html_row,title=descriptors[tol]))

        return table



    #
    def make_dash_table_overall(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                if len(str(row[i]))<40:
                    html_row.append(html.Td([row[i]]))
                else:
                    row[i] = html.A("link",href=row[i],target="_blank")
                    html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/social_media/")

    #
    copli_first = pd.read_csv(path + "copli_first.csv").set_index("ticker")
    copli_second =pd.read_csv(path + "copli_second.csv").set_index("ticker")
    copli_third =pd.read_csv(path + "copli_third.csv").set_index("ticker")

    copli_first = copli_first.loc[[coy, bench,"Mean"],:].reset_index().T
    copli_first.columns = copli_first.iloc[0,:].values
    copli_first = copli_first.reset_index().replace("ticker","Measures")
    copli_first = copli_first.reset_index().replace("Mean","Bench").round(2)
    copli_first["index"].iloc[1:8] = [x +" (K)" for x in copli_first["index"].iloc[1:8]]
    copli_first = copli_first.iloc[:,1:].fillna("NA")

    copli_second = copli_second.loc[[coy, bench,"Mean"],:].reset_index().T
    copli_second.columns = copli_second.iloc[0,:].values
    copli_second = copli_second.reset_index().replace("ticker","Measures (K)")
    copli_second = copli_second.reset_index().replace("Mean","Bench").round(2)
    copli_second = copli_second.iloc[:,1:].fillna("NA")

    copli_third = copli_third.loc[[coy, bench,"Mean"],:].reset_index().T
    copli_third.columns = copli_third.iloc[0,:].values
    copli_third = copli_third.reset_index().replace("ticker","Measures")
    copli_third = copli_third.reset_index().replace("Mean","Bench").round(2)
    copli_third = copli_third.iloc[:,1:].fillna("NA")

    lt = html.Div([

        html.Div([
    html.H6('FB Measures',
            className="gs-header gs-text-header padded"),
    html.Table(make_dash_table_metrics(copli_first, fb_measures), id="som1"),
    #html.H5(str(fullar[fullar["ticker"]==coy]["Overall Rating"].round(2).iloc[-1]),title="Overall Rating",style={"font-size":"60px","color":"#65201F",'font-weight': 'bold',"text-align":"center","margin-bottom":"0.2cm","margin-top":"-1cm",'padding': "0px"})
                     ],style={'float':'left','width':'32%' }),

    html.Div([
    html.H6('Other Media',
            className="gs-header gs-text-header padded"),
    html.Table(make_dash_table_metrics(copli_second, other_media), id="som2")
                     ],style={'float':'left','width':'32%','margin-left':'2%'}),

    html.Div([
    html.H6('Ratios and Ratings',
            className="gs-header gs-text-header padded"),
    html.Table(make_dash_table_metrics(copli_third, ratio_rating), id="som3")
                     ],style={'float':'right','width':'32%' }),],style={'display':'inline-block','width':'100%'})

    return lt