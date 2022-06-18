# CoinSmartTrade
It's a trading strategy which intends to capture sudden price movements in both directions by sending you the notification on desktop for the pairs which has these sudden price movements.
Working : It takes the volume data for every 5 min interval and compare it with a threshold value which itself is calculated by looking into the distribution of volume data. I found it to be fairly normally distributed and so took threshold value as below:
 Threshold value = mean + 2*std.
 Since there is a very strong correlation between volume and price movements, I used the volume as an indicator to enter into the market.
 I had created two verions, one for 5 minute interval and one for 15 minute interval, one can create for 1 minute as well.
