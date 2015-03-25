#!/usr/bin/env python
# encoding: utf-8
# Chisel by David Zhou, github.com/dz
# Fork and mod by Chyetanya Kunte, github.com/ckunte

try:
    import sys, os, re, time, jinja2, markdown, gzip
except ImportError as error:
    print 'ImportError:', str(error)
    exit(1)

# SETTINGS
#BASEURL = "http://ckunte.dev/log/" #trailing slash
SOURCE = os.environ["HOME"] + "/Sites/posts/" #trailing slash
DESTINATION = os.environ["HOME"] + "/Sites/yoursite.net/log/" #trailing slah
TEMPLATE_PATH = os.environ["HOME"] + "/Sites/chisel/templates/" #trailing slash
HOME_SHOW = 3 # number of entries to show on homepage
URLEXT = ".html" # for clean urls, this be "", and exclude .html in template links.
TEMPLATE_OPTIONS = {}
# Date formats
TIME_FORMAT = "%B %-d, %Y" # shown on post entries
STIME_FORMAT = "%b %d" # shown on the archive page
RSSDATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
ENTRY_TIME_FORMAT = "%m/%d/%Y" # to be input on the second line of post in markdown
# The block below is until Markdown 2.4.1.
#FORMAT = lambda text: markdown.markdown(text, ['smartypants','footnotes'])
# ---
# The commented block below is for Markdown 2.5 onward.
FORMAT = lambda text: markdown.markdown(text, \
    extensions=['markdown.extensions.smarty','markdown.extensions.footnotes'])
#
if URLEXT == ".html":
    PATHEXT = ""
    pass
if URLEXT == "":
    PATHEXT = ".html"
    pass

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print "Starting " + func.__name__ + "...",
        func(*args, **kwargs)
        print "Done."
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            if not re.match(r'^.+\.(md|mdown|markdown)$', name): continue
            path = os.path.join(root, name)
            with open(path, "rU") as f:
                title = f.readline().decode('UTF-8')[:-1].strip('\n\t')
                date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
                year, month, day = date[:3]
                content = FORMAT(''.join(f.readlines()[1:]).decode('UTF-8'))
                url = '/'.join([str(year), os.path.splitext(name)[0] + URLEXT])
                files.append({
                    'title': title,
                    'epoch': time.mktime(date),
                    'content': content,
                    'url': url,
                    'pretty_date': time.strftime(TIME_FORMAT, date),
                    'sdate': time.strftime(STIME_FORMAT, date),
                    'rssdate': time.strftime(RSSDATE_FORMAT, date),
                    'date': date,
                    'year': year,
                    'month': month,
                    'day': day,
                    'filename': name})
    return files

def write_file(url, data):
    path = DESTINATION + url + PATHEXT
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs): os.makedirs(dirs)
    with open(path, "w") as file:
        file.write(data.encode('UTF-8'))

def write_feed(url, data):
    path = DESTINATION + url
    with open(path, "w") as file:
        file.write(data.encode('UTF-8'))

def write_sitemap(url, data):
    path = DESTINATION + url
    with gzip.open(path, "wb") as file:
        file.write(data.encode('UTF-8'))

@step
def gen_home(f, e):
    write_file('index' + URLEXT, e.get_template('home.html').render(entries=f[:HOME_SHOW]))

@step
def gen_detailpages(f, e):
    for file in f:
        write_file(file['url'], e.get_template('detail.html').render(entry=file))    

@step
def gen_archive(f, e):
    write_file('archive' + URLEXT, e.get_template('archive.html').render(entries=f))

@step
def gen_colophon(f, e):
    write_file('about' + URLEXT, e.get_template('about.html').render(entry=file))

@step
def gen_rss(f, e):
    write_feed('rss.xml', e.get_template('feed.html').render(entries=f[:HOME_SHOW]))
 
@step
def gen_sitemap(f, e):
    write_sitemap('sitemap.xml.gz', e.get_template('sitemap.html').render(entries=f))

def main():
    print "Chiseling..."
    print "\tReading files...",
    files = sorted(get_tree(SOURCE), key=lambda entry: entry['epoch'], reverse=True)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), extensions=['jinja2_markdown.MarkdownExtension'], **TEMPLATE_OPTIONS)
    print "Done."
    print "\tRunning steps..."
    for step in STEPS:
        print "\t\t",
        step(files, env)
    print "\tDone."
    print "Done."

if __name__ == "__main__":
    sys.exit(main())