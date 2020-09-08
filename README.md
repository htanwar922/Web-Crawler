# Web-Crawler

<info>
The WebCrawler downloads html files and continously crawls over extracted urls from the html files further. The downloaded files are stored in <code>&lt;path&gt;/&lt;filePath&gt;</code> defined in config.py file or in CLI arguments.<br>
After each level of extraction, it waits for 5 seconds.<br>
If the crawling is interrupted, there is an option to <code>&lt;continue\_left\_off&gt;</code> in the configuration.<br>
The crawler uses MongoDB database for handling of crawled information. The connection to MongoClient can be configured with <code>&lt;client&gt;</code> option.<br>
</info>

### Setup
Setup in linux can be done by sourcing setup.sh file:<br>
<code lang="bash">
source setup.sh
</code>
<br>
<p>It creates a python virtual environment in the repo directory itself, and runs main.py with config options defined in config.py file.</p>

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
<p>CLI arguments can also be provided which will override the config options in config.py file.</p>
