Description:
The package is built using Python, HTML and Javascript. The project code presented in 'CODE' folder is divided into three major parts. Namely DataCollection, UI and Algorithm.
The DataCollection and Algorithm is built using python. The UI components are built using HTML and Javascript. 
Data files are present in the submission, these were extracted using the code present in DataCollection folder.

Installation:
Requires Python 3.6 along with following Package requirements:
 1. numpy
 2. scipy
 3. pandas
 4. json
 5. flask 
The above python packages must be installed if not present. Python PIP install can be used for this.

Execution:
	1. Extract and copy the Code folder in any desired location. 
	2. Run the index.py file using command : python index.py. This will start hosting a web API in the localhost:5000 port. ( This address will be displayed)
	3  Browse for the http://localhost:5000/ui using GoogleChrom or FireFox browser.
	4. Once the page is loaded, start typing the desired movie name in the text box and click on "Get Recommendation" button.
	5. This will create a visualization of Movies, tropes and recommended movies.
    6. Change the sliders to tune the recommendations
	
Note: 
1. An API key is needed to connect to TMDB website. We kept our key as default value. 
2. All the data files needed are present in the package and should be with the expected name.


