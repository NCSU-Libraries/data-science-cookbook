# How to Create a Bar Chart over a Map in Tableau

> Credit: This tutorial was developed by [Kiara Richardson](https://github.com/kmricha4), Data Science Consultant in the [Data & Visualization Services department](https://www.lib.ncsu.edu/department/data-visualization-services) at NC State University Libraries in 2021. This tutorial uses calculated fields to generate bars as described by Jeffrey A. Shaffer on the [Data Plus Science, LLC blog](https://www.dataplusscience.com/BarChartMaps.html).   

> Note that this code is currently missing the referenced "Dogs Vs. Cats" spreadsheet and image URLs have not yet been added.

## Part 1: Uploading the Data
 We are going to be using a **fictitious** dataset for this tutorial. The dataset includes a survey of how many households in different cities that have a dog or a cat as a pet.
1. Open Tableau and under ‘Connect’ - ‘To a file’ , click on 'Microsoft Excel'  
2. Find the excel file titled "Dogs Vs. Cats" and click open
3. In your Data Source view, Choose the sheet in which your working data is and drag that sheet to where it says “Drag Sheets here”.   
Click Here for how your dashboard should look: [Insert Image 1 here.]   
4. Make sure Tableau is interpreting your Data Types correctly. (e.g., the Location column may need to be changed from a simple string to being assigned the Geographic Role of City)   
5. Click on the icon at the top of a column to change the data type:
6. Make sure all dimensions match a location, data type, number value, etc. Please see example below [Insert Image 2]   

## Part 2: Creating Bar Chart Calculations

You will have to create a few new fields before creating your graphic.   

1. In the Data Source tab on the bottom left.
2. Hover over Dogs and click on the small drop down arrow or right click on the column.
3. Click on create calculated field.
4. Enter the copy and paste the below statement.   
 LEFT ("██████████",ROUND([Dogs]/([Cats]+[Dogs])*10))
    - This statement will tell Tableau to create a left bar that depicts the proportion of many Dogs against the total household pet population. We also scaled the bar up 10 times up so that we can see more of the smaller bars proportions for depiction.
5. Click Apply, then Ok.
6. Repeat the above and create the same calculated field for Cats.  
 LEFT ("██████████",ROUND([Dogs]/([Cats]+[Dogs])*10))

Click here for example [Insert Image 3]  


## Optional: Create a Regions Column

You will also need to group data together to create a Regions Column  

1. Right Click on the “State” column and click on “Create Group”  
2. In “Field Name” write what you would like the column to be named (e.g., Regions)  
3. Hold down Ctl- (Windows) or Cmd- (Mac) and click to highlight the states you would like to group, (e.g NC,FL,VA,AL,MS, & GA for Southern region). Click “Group”   
4. After creating a group, rename it with the appropriate region, (e.g. South).  
5. Repeat to group the rest of the states. Click Apply, then ok.  Click Here for an Example: Insert Image 4    

**_At the end of these steps you should have 3 new columns. Two new columns for the bar graphics and one for the group._**


## Part 3: Creating the Map
1. Go to your first Sheet    
2. Under Dimensions - double click on State. This should generate a map with data points.  Refer to this example [Insert Image 5]  
3. Under “Measures”, Drag Latitude (generated) to Rows at the top of sheet.  
4. Click the drop down from the second Latitude (generated) and click “Dual Axis”  
5. Under ‘Marks’, Click on the second Latitude (generated) and change the drop down to “Text”  
6. Under “Measures”, Drag the all the newly calculated fields for the bars (e.g Asian Bar) directly over the Text box.   
7. Click on the Text box, and click on the Alignment drop down menu and select these options:   
    - For Horizontal, click Left   
    - For Vertical, click Bottom   
    - For Direction, click Up  
8. Click on the ellipsis (…) next to ‘Text’  
9. To change color of a bar graphic, highlight each AGG value and use the dropdown color picker to change the text color   
10. Click apply and ok  
   See Example [Insert Image 6]
11. Don't forget to name your map at the top!


## Part 4: Tips and Tricks

### Adjust the Size of the Bars
1. Click on the Size box and drag bar to left for smaller bars and right for larger bars.  

 ### Highlighting Regions  

1. Under Marks, for the first Latitude (generated), change the drop down menu to Map      
2. Drag the column in which you created the group of maps (ex. State(group)) to the map and each region should turn a separate color.

### To Change Colors of the Regions

1. To the right of the pane you should see the color Legend. Click on the arrow and “Edit Colors”
2. Select Color Palette “Seattle Grays” then Assign Palette.
3. Click Apply then Ok.  

   See Example: Insert Image 7   

### Edit Map

1. At the top, click on “Map” then “Map Layers”.
2. Edit Map to include/exclude borders, state/city names, black out states without data, etc.  
See Example: [Insert Image 8]

### Creating a Legend

How to create a legend for the 3 samples:

1. Identify an area on the map in which you would like to place the legend.   
2. Right click on the area > Click on Annotate > Click on Area
in the box   
3. Copy and paste the below:   

        █ Dog Bar  
        █ Cat Bar  

3. To change the color of the boxes:   
    - Highlight the black box with your cursor   
    - Choose the same designated color that you have in the bar chart for each sample.   
4. Click Apply then Ok.  
5. You can also choose to give the legend a title by adding one above the boxes.  

Click Here for an example *Colors may Differ*:   [Insert Image 9], [Insert Image 10]
