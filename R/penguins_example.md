---
---
  
```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## Introduction

This document is to go through some useful data wrangling functions in R and provide patrons some useful online materials related to fitting statistics models based on different specific goals. One very powerful package in R, while doing data manipulation, is the **dplyr**. Here we would use two penguin data, in R-packages called **palmerpenguins** and **ggResidpanel**, to demonstrate how and when some functions are used while working on data.

## Data manipulation

First things first, we would need to install the packages we need.
```{r, message=FALSE}
if (!require('dplyr')) install.packages('dplyr')
library('dplyr')
if (!require('palmerpenguins')) install.packages('palmerpenguins')
library('palmerpenguins')
if (!require('ggpubr')) install.packages('ggpubr')
library('ggpubr')
if (!require('ggResidpanel')) install.packages('ggResidpanel')
library('ggResidpanel')
if (!require('lme4')) install.packages('lme4')
library('lme4')
```
The penguin data mainly consist of two different types of variables. First, is the continuous repose variables $y$, including the flipper length, body mass, bill dimensions of each penguin. Second, the discrete variables $x$, including the species and the island in Palmer Archipelago of each penguin. Take a look at a subset of the penguin data that we are going to work on.

```{r}
head(palmerpenguins::penguins)
```

We observed that there are missing data by looking at the subset of penguin data. For further statistical analysis purposes, we omit the missing data by using the `filter` statement. The `filter` statement is to retain rows that satisfy certain conditions. To have rows without missing values, we could use the `filter` statement with the `complete.cases` function. The new penguin data with no missing values are saved as new data named `new_penguins`. 
```{r}
new_penguins<-palmerpenguins::penguins%>%filter(complete.cases(.))
```

Then we can use the `select` statement to select specific columns; here we select species, island and sex.
```{r}
head(new_penguins %>% 
       select(species,island,sex))
```
Want to create a grouped report of your data ? Use `summarize` followed by a `group_by` statement. Here we are creating a report that has the number of observations of different penguins species on different island.
```{r}
total_count=new_penguins %>% 
  group_by(species,island) %>% 
  summarize(n())
```
To filter the rows based on some conditions, use the `filter` statement. Here we are only looking at the count, mean and standard deviation of flipper length of male penguins.
```{r}
group_count=new_penguins %>% 
  group_by(species,island,sex) %>% 
  summarize(n(),mean(flipper_length_mm),sd(flipper_length_mm))%>% filter(sex=='male')
```
How to extract the information the we got from the summary table? Use the dollar sign.
```{r}
group_count$`n()`/total_count$`n()`
```
Save the table that we created for future use.
```{r}
write.csv(group_count, file = "penguins_groupby.csv")
```

## Statistical modeling

The first goal of the statistical analysis on the Palmer penguin data is to find out whether the response variables $y$, e.g., the flipper length, body mass or bill dimensions of each penguin exist differences among groups, e.g., species or island in Palmer Archipelago.

### ANOVA models
Reasonable statistics models one might consider are one-way ANOVA, two-way ANOVA with or without interaction. Here we would not go into details about the ANOVA models, just provide a general strategy for statistical analysis using ANOVA models. Suppose that we consider fitting a two-way ANOVA model
$$
y_{ijk}=\mu+\alpha_{i}+\beta_{j}+(\alpha\beta)_{ij}+\epsilon_{ijk},
$$
where $\mu$ is the overall mean of the response $y$, $\alpha_{i}$ and $\beta_{j}$ are the additive main effect of level $i$ and $j$ from the first and second group variables (species and island in Palmer Archipelago). The main assumption being made on the ANOVA models is that the error, $\epsilon$, are assumed to be independent and normally distributed with mean zero and constant variance $\sigma^2$. While fitting a two-way ANOVA model, we would need to investigate the interaction effect. This could be done by plotting the mean of the response variables for each group variable. Some useful code for plotting the mean plot of the observed data could be found through the following link

<http://www.sthda.com/english/wiki/two-way-anova-test-in-r>.

If the lines cross in the mean plot, then this might indicate there exist an interaction effect across the two groups. This somehow provides evidence that we should consider a two-way ANOVA model with interaction. We could use the `lm()` or `aov()` functions in R to fit the ANOVA model. For more details and examples; see

<https://bookdown.org/steve_midway/DAR/understanding-anova-in-r.html>

### Generalized linear model

The aforementioned ANOVA model had a Normal assumption on the error terms. But, in practice, the error terms might not follow a Normal distribution. To check this, we could plot the density of the response of each group and see whether placing a Normal distribution on the observed data is reasonable. Here we use the body mass as the response variable and plot the density of each species. 

```{r}
ggplot(new_penguins, aes(x = body_mass_g)) +
  geom_density() +
  facet_wrap(~species, ncol = 3)
```

We observed that the density of response seems to have heavy tails. This happens in real-data analysis. The response variable does not guarantee to be normally distributed in the observed data. A generalized linear model provides some flexibility in modeling. For example, a binary regression for the discrete response, Poisson regression for count response, or a Gamma regression for continuous and skewed response with all values greater than zero. There are others regression models for different types of response variables, e.g., negative binomial or Beta regression model. The generalized linear model is a general class of linear model, an ANOVA model is a special case of it. Some useful code for fitting a generalized linear model could be found through the following link

<https://tysonbarrett.com/Rstats/chapter-5-generalized-linear-models.html>.

For more detail about how to interpret the result of different generalized linear models and some examples; see

<https://stats.oarc.ucla.edu/r/seminars/generalized_linear_regression/>

### Linear mixed effect model
 
So far we only consider the fixed-effect model, now we would like to discuss when to consider a random or fixed effect on a linear mixed effect model. The penguin data in **ggResidpanel** R-package would be a great example to demonstrate the idea behind the linear mixed effect model.

Before getting into the model fitting, we should mention what is a fixed or random effect, and how it impacts the interpretation of the model. There are no firm rules for defining a fixed or random effect, but in general, the guidelines are as follow

* Random effect: 
  + The group variable is a subset of the population. As we randomly selected the groups from a larger population, we would need to treat the group variable as a random effect. For example, if we randomly select schools within a district and the response is the student score. The school might be a random effect as we need to consider variations between schools.
  + Nested data structure and would like to control potential dependent of the hierarchical structure. For example, in educational research, it is common to have repeated observations for each student. The observations in this example are nested within each student. For each student, the observed values are likely to be dependent. Another example might be the visit of each patient.
* Fixed effect: the group variable represents the entire population, e.g., gender, treatment assignment.

The penguin data in **ggResidpanel** package is measuring the heart rate of 9 different emperor penguins  based on the depth (in meters) and duration (in minutes) they dive. Through data visualization, we could find some evidence of why we should consider using a linear mixed effect model on this emperor penguins.
```{r}
new_penguins2<-ggResidpanel::penguins
new_penguins2<-new_penguins2%>%mutate(bird=paste('Penguin',new_penguins2$bird,sep=' '))
ggplot(new_penguins2, aes(x = depth,y=heartrate)) +
    geom_point() +
    facet_wrap(~bird, ncol = 3)
```

The plot shows that each penguin has a different curve on depth with respect to heart rate. There might exist variation among the penguins, which leads us to consider setting the penguin as a random effect. In R, we fit a linear mixed effect model using the **lme4** package. 

```{r}
penguins_mixed = lme4::lmer(heartrate ~ depth + duration + (1 | bird),data=new_penguins2)
# create a summary results
summary_output=summary(penguins_mixed)
# Total variance of the random effects attributed to model
round(53.7/(53.7+144.8),3)
# extract fixed effect  estimates
fixef(penguins_mixed)
# the confidence interval of the random and fixed effects
confint(penguins_mixed)
# prediction
yhat <- fitted(penguins_mixed)

```


* The random effect provides 27.1\% of the total variance in the model. If the explained variance from the random effect is small, then we might consider removing the random effect and applying generalized linear modeling instead. 
* To extract fixed effect estimates, we could use the `fixef` function, and the interpretation is the same as linear regression. For example, increasing one unit (meter) of depth would increase 0.06 units (beats per minute) of the heart rate of penguin, and increasing on a unit (minute) of duration would decrease 5.72 units (beats per minute) of the heart rate of penguin. 
* The significance of the fixed and random effect could be found using the `confint` function. In the results, the 95\% confidence interval of the coefficients of fixed effect, including the intercept, depth, and duration, does not contain the value zero. We could conclude that all the fixed effects are significant in the linear mixed effect model. The confidence interval of the variance of the random effect does not include zero as well, thus, using a random effect makes sense on this penguin data.
* The prediction of heart rate could be done using the `fitted` function

Need more details about the linear mixed effect model and how to interpret the result?

* Some applications of linear mixed effect model; see
<https://m-clark.github.io/mixed-models-with-R/random_slopes.html>
* How to interpret a linear mixed effect model; see
<https://it.unt.edu/sites/default/files/linearmixedmodels_jds_dec2010.pdf>
* Understanding mixed-model formulas in **lme4** package; see <https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf>

