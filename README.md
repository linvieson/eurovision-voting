# Eurovision voting

## Aim of the project

Voting systems are extremely sensitive to different factors, and thus are easy to manipulate, implicitly or explicitly. The Eurovision Song Contest (ESC) is an example of such voting ambiguousness. It is upon people to decide which artists will win, but the results of the contest do not depend only on their opinions. The locations of main diasporas, national minorities’ distribution, and political presumptions are the main factors that might affect the authenticity of the results. For instance, being in solidarity with Ukraine, neighbouring countries may give it more points, and vice versa. Likewise, countries with large diasporas of ukrainians will more likely vote for their native country.

The aim of this project is to identify whether peoples’ votes are correlated with political and demographic situations in the countries, based on the previous Eurovision contest results, data about ethnicities’ distribution over participant countries, and geopolitical and cultural factors.


## Implementation

Two OLS models were implemented. The dependent variable is the number of points to country A from country B in the particular year.

- In the first model, the dependent variables are defined as a number of migrants in country A from country B in all previous years, inclluding the predicting one.
- In the second model, the dependent variables are votes, given to country A from country B in the previous years, not including the predicted one.

In both models, there are two more parameters specified: the presense of physical border between countries A and B, and the language variable = 1 if country A performs a song in a language, that is native to country B, 0 otherwise.

## Data description

Primary data used in the research comes from three datasets: Eurovision data 1957-2021, Eurovision data 2021, and Population division dataset. All data sets were cleared and brought to a convenient view. Moreover, special functions to get information about the specific country were implemented.

All the necessary datasets can be found in the [data](https://github.com/linvieson/eurovision-voting/tree/main/data) folder, and the data processing functions are located in the [process_data.py](https://github.com/linvieson/eurovision-voting/blob/main/process_data.py) module.


## Results

The results of the project are important to identify the relevance of the contest voting systems, in particular the ESC one. The precise analysis also gave insights into the possibility of anticipating contest results long before the voting polls are even open.
 
As a result of the work, an analysis of exploring the ESC voting results was done. After analysing different geopolitical, ethnical, and cultural features, the authors were able to explain these factors’ influence on the overall ESC voting results and competitors’ victories throughout the years, starting from 1990.
 
It turned out that the model, based on the migration data, has a very low R-squared score of 13.7%, meaning it is not reliable in predicting the voting results. On the contrary, the model, which takes into consideration voting results from the previous years, is  more credible, showing the R-squared score of 93%. The p-values to the variables in the migration-based model are not low, thus the null-hypothesis of those variables being significant is rejected. Regarding the borders and language variables, they tend to influence the overall voting results at some point.

The reports can be found in the [reports](https://github.com/linvieson/eurovision-voting/tree/main/reports) folder.

## Contributors

- [Alina Voronina](https://github.com/linvieson)
- [Anastasiia Havryliv](https://github.com/be-unkind)


## Lisence

[MIT](https://github.com/linvieson/eurovision-voting/blob/main/LICENSE)
