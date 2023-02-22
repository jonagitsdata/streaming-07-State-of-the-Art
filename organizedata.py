#Organize Twitter data into a spreadsheet
#ID | Tweet Created | Tweet ScreenName | Tweet Text | Tweet Status Source
require(twitteR)

tweet_func = function(hashtag,n){
  tweets = searchTwitter(hashtag,n)
  tweets_df = twListToDF(tweets)

  tweets_gTxt = sapply(tweets, function(x) x$getText())
  tweets_gSN = sapply(tweets, function(x) x$getScreenName())
  tweets_gID = sapply(tweets, function(x) x$getId())
  tweets_gCr = sapply(tweets, function(x) x$getCreated())
  tweets_gSS = sapply(tweets, function(x) x$getStatusSource())

  data_to_csv = cbind(tweets_gID,tweets_gCr,tweets_gSN,tweets_gTxt,tweets_gSS)
  write.table(data_to_csv,file = "/home/kartik/Desktop/R-Statistical-Computing/twitteR/twitter_to_CSV.csv",sep = ",",)
}

tweet_func("#gdg",10)