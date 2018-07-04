# Web Data View -- A Chrome Extension Letting Users to Query the Webpage

## To run server, run python chat.py In if statement at the bottom, the first two lines are for eventlet localhost and 2 lines below are for Kite server.

## Problem Definition
Web data is ubiquitous and is an abundant source of information. Users typically spend a few hours every day to extract information from the web for activities like online shopping, searching for good restaurants based on customer reviews, sorting through  news articles to gather opinions etc. Typically, data from a webpage is view-only for the end-user. To enable an end-user to perform any kind of data analysis to get additional useful information, it is required that the data entities and values in the webpage are accessible as individual objects. However, performing web data extraction is non-trivial due to unstructured or semi-structured nature of data.    


Previous work in information extraction from unstructured web data fall into two categories.
<ul><li>Machine learning approaches [1] [2] [3]</li>
<li>Rule based approaches [4] [5] [6]</li></ul>  

Machine learning based mathematical models require large amount of annotated data sets and complex model generation. Despite being trained and tuned for best performance, such models are not easily transferable across various categories of domains and data formats. Rule based methods, like web crawlers, require the webpage to be static and rely on proficiency of user's scripting skills. Such scripts could not be readily reused across similar websites and are not robust for changes within the same webpage. Additionally, it also hinders general non-programming community to extract useful information due to gap in skills required for the task.



## Insights and Proposed Solutions

It is evident that existing information extraction approaches are neither user-friendly nor easily transferrable across multiple types of webpages. We addressed this  limitation by proposing, and building a prototype of query language based web data extraction tool called Web Data View.  The acute challenges associated with rule-based approaches and our proposed solution insights of Web Data View are listed here 
* Users have to write wrapper rules outside of the browser, whereas we developed a chrome extension that allows in-browser queries, through a user friendly GUI. Additionally, the browser extension helps the user to visualize query results, and export it to Excel or CSV for further data analysis
* The wrapper rules usually apply only to individual pages and they are sensitive to small changes within HTML . We defined a visual-based query language that is not only robust to small changes but could also be reused across similar websites 
* Writing all the logic including query parsing/execution in Javascript is difficult,  so we created a python Flask server to make the process easier 

## System Architecture

Our approach for developing a query language-based data extraction is fundamentally based on the Document Object Model (DOM) tree of web documents. The system architecture comprises of a front-end chrome extension and a back-end python flask server. We followed a two-step approach for our system development. The Phase 1 system architecture is shown in Figure 1. 

<figure><center> <img src="https://i.imgur.com/9GHei96.png" alt=".." /> 
<figcaption> Figure 1: Phase 1 System Architecture </center></figcaption>
</figure>



The javascript based chrome browser extension is an interface through which users can specify what needs to extracted from a webpage in the form of a query language. The user query and URL of the current webpage are provided to python flask server for query parsing and query execution. For query execution, the webpage is re-rendered with Selenium webdriver and resultant DOM structure is parsed using a lxml parser to extract matching web elements. A list of xpaths of matching web elements are provided to the front-end chrome extension for display. The fundamental disadvantage of Phase 1 is that the page re-rendered by backend could be different w.r.t size, location, and properties of various web elements from the front-end version seen by the user. Additionally, the front end does not have a built-in visualization and export of query results to external format for further data analysis. 

To address the limitations of Phase 1 system, we re-architectured, and a new system as shown in Figure 2 was developed. The details of Phase 2 system is provided below.


<figure><center> <img src="https://i.imgur.com/BELVQIh.png" alt=".." /> 
<figcaption> Figure 2: Phase 2 System Architecture</center></figcaption>
</figure>


<b><li>Chrome browser extension </li></b>

A user specifies what needs to be extracted using a simple GUI as shown in Figure 3. The front-end serializes the DOM structure of the current webpage. During serialization process, every node in the DOM tree gets a unique ID. Serialized DOM is a dictionary with key as unique ID and value as dictionary of relevant property-value pairs of DOM nodes. Some examples of properties associated with the DOM node are tagname, classname, text, x location, y location etc. Thus, the front-end provides the user query and serialized DOM objects to the back-end python flask server. A query template for user query is shown in Figure 4. 



<figure><center> <img src="https://i.imgur.com/lS0e4Xw.png" alt=".." /> 
<figcaption> Figure 3: In-browser User Interface</center></figcaption>
</figure>


<figure><center> <img src="https://i.imgur.com/yIShmmS.png" alt=".." /> 
<figcaption>Figure 4: Sample Query Template</center></figcaption>
</figure>



The python flask server performs query parsing and query execution, and returns a list of unique ID’s of nodes that satisfy the match criteria in the user query. The unique ID's are used to identify DOM nodes in the front-end for visualization and export of query results. 

<b><li> Python Flask Server </li></b> 

The user query has information on what needs to be extracted (Ex: laptop title and price from a given webpage) and query details are obtained by the query parser. The query execution engine iterates through serialized DOM nodes to get a list of nodes that match the user provided criteria.

<b><li> Query Language </li></b>

The json query format is designed to extract multiple fields from a web document. The "*extract*" specifies what needs to be extracted and "*Field_id*" is the user defined unique identifier for each object type.  For example, for extracting laptop title and price from an e-commerce website, there needs to be 2 field-ids. Within each field id, user specifies various "*match*" conditions. These match conditions correspond to various primitives that the user defines for extraction.  For instance, lets say a user needs to extract title of laptops from bestbuy website. The title text is identified either by text length (range) or tagname or combination of the above conditions. The text length and tagname are examples of primitives in the above query.

<b><li> Supported Language Primitives </li></b>

A set of different categories of language primitives supported in our framework are shown below.

| Type  | Functions 
| -------- | -------- 
| Generic     | isdate, isprice, islink, isnumeric
| String | len, startswith, endswith, contains, regex
|Image | size, location
|Position | align (left,right,top,bottom,vertical,horizontal), bounding box
|Web | classname, tagname
|Visual | location (top, bottom,left,right,middle)

The fundamental reasons to support different types of primitives are 1) completeness of operators (similar to SQL) and 2) expressives (i.e how much a user could potentially describe using the primitives). Each class of primitives is briefly explained below with a simple illustration.

Generic functions enable extraction of string in a specific format like date or price. For example, price, available date of a books, URL of book description from an online bookstore could be obtained using generic primitives. String functions provide a variety of ways to extract text information from a webpage. Typically, title text in e-commerce websites are longest strings. Users could use this insight in "len" primitive to extract titles. Users could specify substring-based extraction with startswith and endswith functions for additional filtering. Regular expressions are powerful constructs that enable users to reuse queries across multiple webpages with a generic pattern. Image extraction is enabled through bounded box location and image size (height and weight) functions. 

The fundamental advantage of our method is enabling the user to extract information based on visual layout of the webpage. The position and visual primitives enable the user to extract web elements based on "*what user sees*" principle. "Align" position primitive extracts a set of web elements that satisfy user's align criteria. For instance, the news article headings in BBC homepage are top-aligned i.e their X position varies and Y position remains the same. Users could use this insight to extract news headlines. Visual primitives enable users to extract information based on their relative location in the webpage.  We divide the layout of the webpage into three parts vertically and horizontally. "Top" represents top 30% of the page, bottom represents bottom 30% of the page. Similar definitions are used for left,right and middle. For instance, the BBC news headlines could be extracted by specifying the location criteria as "top".

<b><li> Output files </li></b>

User could the highlight results in the browser after query execution, and click the output icon to generate the grid view of the results, and eventually download the results in various formats.

![](https://i.imgur.com/PXWe7cf.png)


## Quantitative Evaluation of Query Results

We performed several experiments to test the robustness of the system and correctness of the query result. 
In the result chart below, precision means how many highlighted element are correct, and recall means how many expected highlighted elements are indeed highlighted.


<b><li>Text query for multiple websites</li></b>

This Query selects all the price, title and the corresponding records of computer from shopping websites.
![](https://i.imgur.com/IFjJgZY.png)

| Website  | Highlighted elements | Expected Highlighted elements | Precision(%) | Recall(%) 
| -------- | -------- | ------- | ------- | -----
| Amazon  | 23 | 24 | 100.0 | 95.8
| Bestbuy | 24 | 24 | 100.0 | 100.0
| eBay |   49 |50 | 100.0 | 98.0
| Walmart |20 |20 | 100.0 | 100.0

<b><li>Text query for the same website across time</li></b>

This query is the same as Q1, but runs on Amazon's current webpage and history pages. We got the history pages from https://web.archive.org

| Year  | Highlighted elements | Expected Highlighted elements | Precision(%) | Recall(%) 
| -------- | -------- | ------- | ------- |-
| 2005  | 5 | 5 | 100 | 100
| 2008 | 5 | 5 | 100 | 100
| 2012 |   17 |24 | 100 | 70.8
| 2015 |20 |24 | 100 | 83.3
| 2018 |23|24| 100 | 95.8

<b><li> Text queries for websites in different domains</li></b>

This query tests the string matching functionality as well as the capability to deal with different kinds of websites.
In Amazon, Reddit, Quora, we first search iPhone, and then let the language to highlight all the titles containing "iPhone X"

![](https://i.imgur.com/pFKT9Bp.png)


| Website  | Highlighted elements | Expected Highlighted elements | Precision(%) | Recall(%)
| -------- | -------- | ------- | ------- | ---
| Amazon  | 1 | 1 | 100 | 100
| Reddit | 2 | 2 | 100 | 100
| Quora |   7 |9 | 85.7 | 66.7

<b> Image queries across various websites </b>


The following query illusrates refrigerator image extraction from multiple websites using image size primitive. Amazon, bestbuy, ebay have images vertically aligned, but walmart has the images horizontally aligned.  Irrespective of their differences, a single query collects images from multiple webpages.
![](https://i.imgur.com/O8pylcr.png)


| Website  | Highlighted elements | Expected Highlighted elements | Precision(%) | Recall(%)  
| -------- | -------- | ------- | -------|-------|
| Amazon  | 27 | 20 | 75.07 | 100
| Bestbuy | 22 | 24 | 100 | 91.67
| eBay |   16 |25 | 100 | 64
| Walmart |47 |40 | 85.11 | 100

<b>Image query across different timeframes of same webpage</b>

The query is same as above, tested against amazon website across timeframes. The webpage structure evolved and we were able to execute the same query.

| Year  | Highlighted elements | Expected Highlighted elements | Precision | Recall 
| -------- | -------- | ------- | ------- |-
| 2008 | 38 | 24 | 63.16 | 100
| 2012 |   18 |16 | 88.89 | 100
| 2015 |15 |15 | 100 | 100
| 2018 |27|20|75.07 | 100


<b> Image extraction using alignment</b>
This query highlights how difffernt images could be extracted with alignment property of images

![](https://i.imgur.com/1psABeM.png)


| Website  | Highlighted elements | Expected Highlighted elements | Precision(%) | Recall(%)  
| -------- | -------- | ------- | -------|-------|
| Amazon  | 20 | 20 | 100 | 100
| Bestbuy | 12 | 24 | 100 | 50
| eBay |   12 |24 | 100 | 50
| Walmart |0 |0 | NA | NA



##  Lessons Learned
<li><b>Importance of user friendly application</b></li>

A major novelty of our system is that we packed all the functionality and made it an application in the form of Chrome browser extension. We could have accomplished similar  functionality using python scripts only. The latter approach would not have been friendly for non-programmers as the users might need to execute a script for DOM serialization, query parsing and execution. Additionally, re-use of scripts across similar websites would need the user to specify URL everytime. The in-browser extension works on current page alleviating these drawbacks.  A good application should be relatively straightforward to be used by people with different skill-sets and our platform accomplishes this goal.

<li><b>Considerations when processing dynamic data</b></li>

Web data is dynamic, and the visual appearance and DOM object properties of webpage could be different across various rendering methods. Initially, we used Selenium webdriver to render the webpage using the URL passed from the front-end. The re-rendered webpage is slightly different from the webpage seen by the user at front-end. As a result, some of the resultant xpaths from backend were invalid. So we changed our approach to serialize the DOM tree obtained in the front-end and pass the same to back-end for query execution. Thus, we learnt that when dealing with real-time or dynamic data, it's important to access data directly, instead of creating backups or in-directly obtaining data through backdoor approaches.


<li><b>Design considerations for query language</b></li>

A major portion of our work was to design a query language to let user query the web. We tried to achieve two fundamental goals. They are 1. Make the language structured and 2. Make the language expressive. To achieve the first goal, we have tried to name our primitives to have an implicit meaning (as in SQL) and impose document-like structure (as in  mongodb). For instance, "TextLength" : {"lt":5,"gt":1}," as match condition for Strings would query for texts that meet the given length criteria. This language structure gave us flexbility to add and control primitives seamlessly. For our second goal, we continued to add primitives to let our query language support a wide variety of match strategies (e.g. match by alignment, size, location, etc.). 

We found that it is challenging to define a query language  over unstructured data. To make our data as structured as possible, we serialized the DOM tree of a webpage. Serialized DOM tree contains key-value pairs of subset of properties of every DOM node. Although comprehensive experiments have been performed on our system, there may be limitations due to partial information of DOM nodes in the serialized data structure. Thus, through this project, we have learnt how to design a query language and how to structure data to get extract useful information.


##  Proposed Future Research
<li><b>Further extension of language capabilities</b></li>

Data extraction and manipulation are fundamental capabilities of a query language. Currently, our query language supports data extraction. A potential extension would be to include data manipulation features like aggregation.The aggregation framework could be useful in many cases, for example, to generate text clusters in which font colors are the same, one could use *groupby* framework. To find the cheapest macbook with the rating greater than some threshold, *min* function could be useful.

Currently, we serialized the DOM tree in a custom format with fixed key-value pairs for every DOM node. The query executes on serialized DOM objects. As a future work, one could potentially try to use query on hierarchical DOM tree directly. Since HTML structure is similar to document object model in Mongodb, we could potentially use "unwind" like feature for serialization. This would remove the limitation of having fixed key-value pairs for every DOM node, and enhances flexibility and robustness to include many different web properties. One could also use "project" like operation to limit the properties of DOM nodes as per requirements of query.


<li><b>Improvements on user interface</b></li>

Our language supports many primitives, and as we continue adding primitives, it could become less user-friendly as users might not be able to remember every primitive and their valid usage. In future, one could improve our frontend by making a form to let users to fill in values against match criteria. Additionally, the in-browser query window could be enhanced to have syntax highlighting helping the user to formulate correct syntax.


Furthermore, every user might not be familiar with the webpage properties. When looking at the webpage, the user might be totally oblivious about exact font-color of text,  classnames and tagnames associated with elements etc,. We could implement a mouse hover, whenever the user moves the mouse to an element, a graphical box is shown to let users know some useful properties of the element. Such properties would aid in query formulation.

## 7.References
References:
1)Jun Zhu, Zaiqing Nie, Bo Zhang, and Ji-Rong Wen. 2007. Dynamic hierarchical Markov random fields and their application to web data extraction. In Proceedings of the 24th international conference on Machine learning (ICML '07), Zoubin Ghahramani (Ed.). ACM, New York, NY, USA, 1175-1182. 
2)Jun Zhu , Zaiqing Nie , Ji-Rong Wen , Bo Zhang , Wei-Ying Ma, 2D Conditional Random Fields for Web information extraction, Proceedings of the 22nd international conference on Machine learning, p.1044-1051, August 07-11, 2005, Bonn, Germany
3)Lu Jiang, Zhaohui Wu, Qinghua Zheng, and Jun Liu. 2009. Learning Deep Web Crawling with Diverse Features. In Proceedings of the 2009 IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology - Volume 01 (WI-IAT '09), Vol. 1. IEEE Computer Society, Washington, DC, USA, 572-575. 
4)Maeda F. Hanafi, Azza Abouzied, Laura Chiticariu, and Yunyao Li. 2017. SEER: Auto-Generating Information Extraction Rules from User-Specified Examples. In Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems (CHI '17). ACM, New York, NY, USA, 6672-6682. 
5)Yanan Hao and Yanchun Zhang. 2006. A two-phase rule generation and optimization approach for wrapper generation. In Proceedings of the 17th Australasian Database Conference - Volume 49 (ADC '06), Gillian Dobbie and James Bailey (Eds.), Vol. 49. Australian Computer Society, Inc., Darlinghurst, Australia, Australia, 39-48.
6)Alberto H. F. Laender, Berthier A. Ribeiro-Neto, Altigran S. da Silva, and Juliana S. Teixeira. 2002. A brief survey of web data extraction tools. SIGMOD Rec. 31, 2 (June 2002), 84-93. 
