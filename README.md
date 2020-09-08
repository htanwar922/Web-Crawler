# Web-Crawler

<info>
The WebCrawler downloads html files and continously crawls over extracted urls from the html files further. The downloaded files are stored in <code>&lt;path&gt;/&lt;filePath&gt;</code> defined in config.py file or in CLI arguments.<br>
After each level of extraction, it waits for 5 seconds.<br>
If the crawling is interrupted, there is an option to <code>&lt;continue_left_off&gt;</code> in the configuration.<br>
The crawler uses MongoDB database for handling of crawled information. The connection to MongoClient can be configured with <code>&lt;client&gt;</code> option.<br>
</info>

### Setup
Setup in linux can be done by sourcing setup.sh file:<br>
<code lang="bash">
source setup.sh
</code>
<br>
<p>It creates a python virtual environment in the repo directory itself, and runs <code>main.py</code> with <code>config</code> options defined in <code>config.py</code> file.</p>

For Windows, run from PS:
<code>
bash -c "source setup.sh"
</code>

### Run
Either run through above setup or run directly by:<br>
<code>
python3 main.py
</code>
<br>
<p>CLI arguments can also be provided which will override the config options in <code>config.py</code> file.</p>

### Get html file
The path for html file corresponding to any successfully crawled link can be accessed by running the <code>get_html_doc.py</code> file and entering the desired link on prompt.<br>
The process asks whether to open the file in a browser, to which a ```yes``` input will do it.
