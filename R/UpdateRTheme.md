# Using `ggplot` Themes: theme_update() vs. theme_replace()

> This recipe shows the difference between ggplot's theme_replace() and theme_update() methods.

Libraries required:
- `ggplot2`

Themes are used in `ggplot()` to control how plots look and can also be used to create a consistent look to all plots.

We load the required library and grab some data to use to generate plots.
```R
library(ggplot2)
data <- mtcars
```

We'll capture one of ggplot's basic themes in a variable. This will let us explore how `theme_replace()` and `theme_update()` change a theme in different ways. We'll generate a plot and confirm what it looks like

```R
my.theme <- theme_set(theme_bw())
```

Make changes and reupload.