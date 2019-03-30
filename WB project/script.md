> - For a past week, I had been able to look into valuable data accumulated by AB Inbev, Wiess Beerger and came up with a couple of insight that could be of value to your team and business. Today I would like to share a few findings with you.

> - For this project, I was given two objectives.
> - The main purpose was to prove whether Soju category is cannibalizing beer consumption or not, given dataset.
> - The second, find opportunities to gain category share and increase beer incidents.
> - For both purposes, I focused my studies on demand of beer and features influencing, in particular, Soju.

> - Let me jump into the conclusion first.
> - After a week of analysis over the data given, I was unable to find good evidence that Soju is cannibalizing demand for beer.
> - And I also found out that the demand for food has something to do with the demand for beer, in a positive way.
> - Now, lets find out how I ended up with such a conclusion.

> - The dataset, which I have acquired look like the table you see.
> - It has 16 thousand rows, and each row has 22 traits, which summarizes daily transactions.
> - They are from 147 bars, 6-month period in 2017.
> - With this data, I was able to:
>   1. understand basic information about daily transactions (which bar, when...)
>   2. track sales volume of beverage by category (not item)
>   3. approximate price given revenue and units sold
> - But I am unable to:
>   1. track record of items sold
>   2. track composition of items in a single order
>   3. figure out how items are categorized into (for instance, soju falls into spirits category, but what else might there be in this category? I donno)
> - So I've got this data, and the hypothesis to study cannibalization... two machine leaning models came across my mind.

> - First, I thought I could build a robust linear regression model, and the coefficient can tell how one affects the other.
> - Second, I could use classification and regression tree model to test feature importance, and how important one variable is in determining the other.
> - For both model, Beer Units could work as dependent variable, Soju Units could work as one of the independent variables.

> - Having that in mind, followed Explanatory Data Analysis.
> - The first thing I looked for, was linear trend of beer, soju, and spirits units sold over the period.
> - As you can see, beer demand seems to be in downward trend.
> - What I also noted was though, "the variance of observations."
> -  The variance in the early stage of observation seemed extraordinary. and I had to look into this in more detail to confirm that beer sales is decreasing.

> - So next, I checked how evenly observations are distributed by bars, and by date.
> - As you can see, observations were not evenly distributed, data was not complete by bars and date.
> - Not a day had full record of 147 bars, and 25 days in the early stage had less than 30 observations, which I reckon that high variance might have been cause by small size of samples.
> - By bars, there were 2 bars with full records over the period, but the stores did not seem to sell soju to compare relationship with beer, what a shame.

> - Looking at correlation matrix among the variables, you can easily witness strong correlation between certain variables.
> - It is obvious as variables like volume, order, unit, revenue for same category are observations from pretty much same event. So upon finding explanation using models, it is advised to avoid the use of duplicated variables.
> - Looking at figure on the right, I also ran correlation analysis on beer and soju units by month. Interestingly, the correlation coefficient increased from -0.11 to 0.13 weakening evidence of substitute goods, cannibalizing.

> - ok, the last bit of EDA
> - It is very typical to find right-skewed distribution in commercial outlets where most sales are made below average, and few exceptional sales triggered by externalities.
> - And it seems the data also shares similar characteristics of right-skewed distribution
> - Nothing bad about it, I will just need to  transforme variables to follow gaussian/normal distribution before I run into building models for analysis for a better explanation. (PAUSE)

> - Now, to begin with data preprocessing, I started with zero values.
> -  In data, there are two types of zero values. One, zero values indicating Not Available. Two, zero values indicating items not being sold.
> - The former, zero values indicating "we don't sell soju" are to be omitted for the analysis testing relationship between beer and soju, as they will distort the effect.
> - I have defined zero values to be omitted, as zero values from bars which aggregate sales unit of soju equals to zero. 
> - There were 15 bars not selling soju.

> - I have also removed observations impossible to explain.
> - Negative figures in daily summary data is one of them. Per item, it can have negative values indicating canceled or refunded order. For data aggregated on a daily bases, however, negative values are nearly impossible to explain without relevant features.
> - Also there are outliers. Observation at the far end of the distribution may have its own reasons for being there. But in most case, those outliers damage integrity of characteristics of dataset. I have created and used derivative variables, price,  which follows normal distribution, and removed observations that are outside of 99.7% credential interval level. There were 593 observations.

> - Next is variable selection, and I will briefly go over the model I am thinking of at this point.
> - The model, which I am trying to build to test hypothesis should look like this. I would like to explain the demand for beer as the sum of demand for other products, characteristics of bar, and characteristics of dates. Especially, my interest is with Soju, which the coefficient should explain the relationship with beer.
> - In the data there are six product categories; soju and beer, spirits, wine, non-alcoholic and food. and each category consists of one to four correlated variables referring to demand. The four types of variables are unit, revenue, volume, and number of order. Of all, I chose unit as a primary variable to represent demands, and revenue the secondary. While I believe units sold is more linked to how much people desire for product, the revenue is combination of unit times price, which is more likely to have been affected by many other externalities like promotion.
> - Bar and date features have been extracted from original data and encoded as dummy variables.
> - Of course I can let machines do the work and select optimum variables that can explain beer trend the best, but since the object of this project is with measuring effect of variable not accuracy, I did select variables manually to some degree.

> - now that we have outlined what the model should look like, the final touch has been left.
> - As said earlier, the values in variables were in right-skewed distribution. I took log to each variables to normalize and convert the shape of data.

> - We have come a long way, and now at last, the analysis.
> - I have implemented linear regression model and CART for good explanation
> - For linear regression model, I have adopted bagged Ridge regression.
> - Based on linear regression that provides effects in coefficient, bagging or easily put, multiple sampling and averaging, and ridge that paneities weight, all together it generalizes model so that it can return more robust output.

> - The final model explains the effect of variables on demand of beer as follows.
> - and referring to the score, model itself has r-square score at 0.8395, and MSE at 0.1632 on full dataset, which I believe the model to be pretty trustworthy.
> - So, the model, it suggests that a percentage increase in soju units result in 0.003 percent decrease in beer units, and you can see how other variables affect beer units. Taking account of relatively small unit volume of soju compared to beer, 0.003 percent does not seem so meaningful.
> - On the other hand the regression coefficient of Food Revenue is noticeable that when food revenue increases by 1%, beer unit is likely to increase by 0.74%

> - Let's look at random forest model now.
> - Similarly, it uses ensemble model too and random forests uses CART prediction to model for beer demand.

> - straight to the result, putting aside of non-demand related variables, we can see that food revenue is considered determinant in forecasting beer demand.
> - Demand for soju on the other hand, is nowhere to be seen. it maked zero.

> - So in conclusion, I want to say that there is no evidence to argue that soju is cannibalizing the beer category.
> - On the left, I cannot agree that beer sales is going down. and to the right the relationship between soju and beer demand is very weak given data. In fact it is showing more of a traits as a complimentary goods rather than substitutes.
> - I would like to reject the hypothesis that soju is cannibalizing.

> - What surprised me in fact was noticeable relationship between beer and food.
> - Out of all the beer orders, 92.4% was with food.
> - I am not so certain that this ratio is relatively high compared to that of other zones, but to my domain understandings, the figure can explain  Koreans’ love for food and gatherings that they do not drink alcoholic beverage alone without foods, even after a full supper.
> - I maybe exaggerating, but from this finding I can relate that after high demand for food follows high food sales, which in turn it can be achievable by a large number of customer visits.
> - If so, in order to increase visit rate as bar owners, I would suggest to go for decent cuisine and food paring for beer, to attract customer, increase beer incidents.
> - For beverage distributors, I can think of promoting dinning out and gatherings to increase chance to beer consumption.

> - So after all this project, I see that there have been some limitations and a few points to be improved.
> - limitations, in short, the data is relatively small in size and is summarized to retrieve product level information and insights.
> - and for points to be improved, I kind of ignored certain variables for clustering, that might have meaningful information, and rather a weak action plan followed by the analysis.

> - ok, that is pretty much all that i have for you today
> - please, should you have anything suggest about the presentation, I am all ears.
> - And one more thing, please excuse me for short English.

