import tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import PySimpleGUI as sg


class SentimentAnalysis:
	

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        consumerKey = 'xxxxxxxxxx'
        consumerSecret = 'xxxxxxxxxxxx'
        accessToken = 'xxxxxxxxxx'
        accessTokenSecret = 'xxxxxxxxxxxx'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        sg.theme('SystemDefaultForReal')	
        
        layout = [  [sg.Text('Please keep an eye on the command line for the result')],
                    [sg.Text('Enter hashtag value'), sg.InputText()],
                    [sg.Button('Ok'), sg.Button('Cancel')] ]
        
        # Create the Window
        
        # Event Loop to process "events" and get the "values" of the inputs
        window = sg.Window('***SENTIMETER***', layout)    

        event, values = window.read()    
        window.close()
        
        searchTerm = values[0]
        NoOfTerms = 100

        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

       
        csvFile = open('result.csv', 'a')

        
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)
        result=""
        # finding average reaction
        polarity = polarity / NoOfTerms
        if (polarity == 0):
            result="Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            result="Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            result="Positive"
        elif (polarity > 0.6 and polarity <= 1):
            result="Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            result="Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            result="Negative"
        elif (polarity > -1 and polarity <= -0.6):
            result="Strongly Negative"
        # printing out data
        sa.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
        sa.posttweet(searchTerm,NoOfTerms,polarity,positive, wpositive, spositive, negative, wnegative, snegative, neutral,result)

    def posttweet(self,searchTerm,NoOfTerms,polarity,positive, wpositive, spositive, negative, wnegative, snegative, neutral,result):
        sg.theme('SystemDefaultForReal')
        layout = [[sg.Text("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")],              
                [sg.Text("General Report: \n"+result)],
                
                   [sg.Text('Detailed Report: ')],
                [sg.Text(str(positive) + "% people thought it was positive")],
                [sg.Text(str(wpositive) + "% people thought it was weakly positive")],
                [sg.Text(str(spositive) + "% people thought it was strongly positive")],
                [sg.Text(str(negative) + "% people thought it was negative")],
                [sg.Text(str(wnegative) + "% people thought it was weakly negative")],
                [sg.Text(str(snegative) + "% people thought it was strongly negative")],
                [sg.Text(str(neutral) + "% people thought it was neutral")],
                
                [sg.Button('Ok')] ]
        window = sg.Window('***SENTIMETER_Result***', layout)    
        event, values = window.read()
        window.close()
       
        
        window.close()
    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        #plt.tight_layout()
        plt.savefig("Figure1.png")
        plt.show()


if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
    
