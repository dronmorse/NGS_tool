# NGS TOOL - PIPELINES FOR GENETIC SEQUENCE ANALYSIS
#### Video Demo:  <URL HERE>
#### Description:

The following project's purpose is to provide a user-friendly interface for bioinformaticians to **process, analyse and generate** reports  by creating pipelines that guide the user through the steps required to analyse their input file.

The project is written as a Web-based application written in Flask and utilizing sqlite3 database to store and access data. The database is also used for storing user data and the passwords are hashed so that they cannot be retrieved easily by a user with malicious intents. The webpages written in HTML use a bootstrap library to enhance the user experience and provide the pages with an easy to read pathway for each pipeline.

Users have to create their own accounts to access the Tools provided by the application. Normally, a scientist will perform multiple analyses at a time, creating a long list of files processed. To overcome this problem, each account only has access to data uploaded using this account.

Currently there are two pipelines available:

- **What does your DNA encode?**
    
    This pipeline allows the scientist to harness the power of the Blast algorithm provided by the ***National Center for Biotechnology Information (NCBI)*** to find sequences similar to what they have in their input file in NCBI's database by using the local alignment tool. The file can be uploaded from the user's disk or retrieved from the database if it was analysed before. Files in a different format than .fasta  will be rejected and files that contain data inside that do not correspond to .fasta format rules will also be rejected. The analysis supports cases where a FASTA input file contains more than one sequence - in such a case, the user will be asked to choose only one for further analysis.
    As the last step, the application asks for a e-mail address for NCBI to contact the user if something goes wrong with their query. By default, the analysis is done over the core_nt database and return top 50 results - choice made to ensure the best experience of the user. Returning only 50 still answers the initial question and limits the time required to make the search. The final report is a modified HTML output file, which only shows what is most interesting to the user - the local alignment with all accuracy parameters and names of matched sequences. The user will be able to download the report file or finish the pipeline. Each subsequent analysis will overrun the previous report and clear all data from the previous analysis.

- **Perform a quick analysis of a FASTQ file**

    This pipeline performs a Quality Control assessment of the input FASTQ file using ***fastQC software***. Similarly to previous pipeline, this one also accepts new FASTQ files or allows the user to use input files from previous analyses. All rules from the previous pipeline apply, as they use the same functions that behave differently when accepting input from separate pipelines. Files in .fasta format will be rejected in this pipeline, while the previous pipeline will reject the .fastq files. As .fastq files oftne consists of several sections called "reads", all of them are returned in the Preview section of the pipeline. All reads have to be accepted before proceeding with analysis - as .fastq file can be very long, the output is initially hidden, but it can be viewed by expanding the input file section. The final fastQC analysis returns an HTML report in an unaltered form that can be downloaded to the local disk that contains all metrics necessary to assess the quality of the input data.

The application is designed to be easily expandable in the future - all fuctions can be reused in the next pipeline that can be added to the application on the later stages of the project.

It is also possible to remove entries from the database simply by going to the "Manage database" menu. Each user can only remove the entries they have uploaded not to the work of others.

Once the user is done they can simply logout and close the session. If the user does not logout but simply closes the browser, the session is terminated automatically.

Citations to the 3rd party software used in this project:
1. **NCBI BLAST:** ***Camacho, C., Coulouris, G., Avagyan, V., Ma, N., Papadopoulos, J., Bealer, K., and Madden, T.L. 2009. BLAST+: architecture and applications. BMC Bioinformatics, 10, 421.***

2. **fastQC:** ***Citation: Andrews, S. (2010). FastQC:  A Quality Control Tool for High Throughput Sequence Data [Online]. Available online at: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/***

3. **Biopython library for biological data retrieval and analysis:** ***Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423***

Explanation of all relevant files:

- **app.py**

    This file is the heart of the project - it starts the Flask session and navigates through all of the user's input. All of the functions prepared are created keeping in mind the idea of code reusability - each function can be reused later for different pipelines if necessary by providing different parameters through HMTL forms or button inputs. All of the functions try hard to handle the edge cases and return a "Sorry!" page if something goes wrong or is unexpected.
    The biggest hurdle here was to integrate the external tools into the Python code, which was not as straightforward as it seemed initially. Programatically, the most interesting part is the processing of FASTA/FASTQ files together using only a **single function** and returning the output to the HTML Preview page, which can recognise the input and process it using Jinja. Such approach is actually common to most of the pages here, but this one shows the elegance of Jinja conditional and loops in tandem with Bootstrap accordion component - speaking of which, proved perfect for displaying contents of .fasta and .fastq files; each header can be used as an Accordion header and content can be collapsed. The page can get quite slow if all the data is loaded and displayed at once - FASTA and FASTQ files can be pretty large, so initially the application froze just because of a sheer amount of data needed to be displayed. Dynamically generated accordion files completely mitigated this issue, thankfully.

- **helper.py**

    This page has a few useful functions for the application - it allows the **app.py** to easily render apology pages, force login, save the sequences to the database and build the input file out of the data stored in the database. As 3rd party tools require actual files as input, the files can be created but they also have to be removed - such a function also exists there.

- **data.db**

    The sqlite3 database is a vital part of the project - it stores data that concern the user login and all the .fasta and .fastq data uploaded by all the users. Thanks to that it is possible to access the data uploaded before without worrying about the input file. It consists of two tables named users and seq - they are related by the users 'id' parameter, that serves as a Primary_Key and allows the application to distinguish between the data uploaded by a single user.

- **templates directory**

    The templates directory includes all the html pages required to run the application. The idea here was to use a single, central *layout.html* page and extend it with additional HTMLs using Jinja - this preserves uniformity and enhances user-experience. One feature used the most among the templates are Jinja loops - they proved really useful when generating content sequentially. 

- **static directory**

    This directory contains a small amount of files - an externall CSS file for additional page formatting outside of Bootstrap, an apology picture and the logo of the application.

- **temp directory**

    Initially empty, this directory is vital to the application proper function - as the external programs require proper files as input, all the operational files are created modified and finally removed here. A challange itself is accesing the files stored here for display - as it came out during the project, Flask struggles with referring to actual Paths; it was necessary to write additional Flask functions to redirect the traffic from HTML (e.g. from iframe) to a certain Flask function and only there render the template, finally accessing the HTML file. Also, Flask can only access HTML files in the templates directory - this creates and additional problem of copying the HTML output to the *templates* folder and removing it afterwards. Thanks to the *temp* folder however everythin can be kept clean.





