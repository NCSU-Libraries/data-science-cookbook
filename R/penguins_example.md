---
title: "Data manipulation and statistical modeling"
output:
  html_document:
    df_print: paged
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## R Markdown

This document is to go through some useful data wrangling functions in R and provide patrons some useful online materials related to fitting and explaining linear mixed-effect model. One very powerful package in R, while doing data manipulation, is the **dplyr**. Here we would use the penguins data, in a R-package called **palmerpenguins**, to demonstrate how and when some functions are used while working on a data.

## Data manipulation

First things first, we would need to install the packages we need, **dplyr** and **palmerpenguins**.
```{r}
require("dplyr")
require("palmerpenguins")
```
Take a look of a subset of the penguins data that we are going to work on
```{r}
head(penguins)
```
Use the `select` statement to select specific columns; here we select species, island and sex.
```{r}
head(penguins %>% 
       select(species,island,sex))
```
Want to create a grouped report of your data ? Use `summarize` followed by a `group_by` statement. Here we are creating a report that has the number of observations of different penguins species on different island.
```{r}
total_count=penguins %>% 
  group_by(species,island) %>% 
  summarize(n())
```
To filter the rows based on some conditions, use the `filter` statement. Here we are only looking at the count, mean and standard deviation of flipper length of male penguins.
```{r}
group_count=penguins %>% 
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
Let's try to fit a linear mixed effect model using the **lme4** package. To extract the model output, there are several functions that we could use, including `summary`,`fixef`,`confint`,`ranef`.
```{r}
require(lme4)
penguins_mixed = lme4::lmer(body_mass_g ~  (1 | island), REML = F, data=penguins)
# create a summary results
summary(penguins_mixed)
# extract fixed effect estimates
fixef(penguins_mixed)
# extract fixed effect confidence interval
confint(penguins_mixed)
# extract random effect
ranef(penguins_mixed)
```
Need more details about linear mixed effect model and how to interpret the result?

* Generalized linear model detail; see <https://stats.idre.ucla.edu/other/mult-pkg/introduction-to-generalized-linear-mixed-models/>
* Some applications of linear mixed effect model; see
<https://m-clark.github.io/mixed-models-with-R/random_slopes.html>
* How to interpret a linear mixed effect model; see
<https://it.unt.edu/sites/default/files/linearmixedmodels_jds_dec2010.pdf>
* Understanding mixed-model formulas in **lme4** package; see <https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf>


