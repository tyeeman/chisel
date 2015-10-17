# Chisel

[![Build Status](https://travis-ci.org/ckunte/chisel.svg?branch=master)](https://travis-ci.org/ckunte/chisel)

Written by [David Zhou][dz] in [python][py], forked and enhanced by [Chyetanya Kunte][c], [Chisel][ch] is an extremely lightweight (just 8kB) blog generating script. 

This fork includes the following additions and enhancements:

- Smartypants content parsing to emit typographically nicer quotes, proper em and en dashes, etc.
- A shorter (just year based) permalink structure.
- RSS feed for posts.
- Page support with markdown. (Use `{% markdown %}Markdown formatted content here.{% endmarkdown %}`)
- Support for Page titles in title tag for permalinks added in templates.
- Supports clean URLs.
- Works just fine with [MathJax][mj] for rendering using [LaTeX][tx] (math syntax). (Just remember to use `\newline` for multiple lines instead of `\n`. For mathjax support, see the section below.)
- Sitemap auto-generation for posts (gzipped).
- List number of posts using `{{ entries | length }}` in Jinja (archive.html) template.
- Time taken to read a post using `{{ entry.content | wordcount // 300 + 1 }} min read`, where 300 is the number of words a typical reader reads per minute. (Posts less than 1 minute long to read will approximate to 1 min.)

## What it does not do

Chisel keeps it simple and stupid. And so, there is

- No taxonomy support, i.e., no categories, and no tags.
- No built-in search. (A simple json based search script may easily be developed together with a gzipped flat file index for text query.)
- Multiple posts in a day, since the time stamp is simple without the time element. This does not mean multiple posts do not show up. They will just be ordered by title alphabetically.

## What it does best

- No loss of fidelity. All posts would be plain text, which kind of makes it timeless. Great for archiving. Burn on a CD, or save it on a USB stick.
- Regenerate the entire site again if one just has the native markdown draft posts, and Chisel + templates.
- It's incredibly lightweight -- less than 8kB! (Compare that with anything out there, and they all seem like they weigh a ton, not to mention the complexity of install, maintain, and backup.)
- Zero security issues. Generate site locally, and upload only the thus created html files out of markdown post drafts. 
- Pure static site. Pretty robust to network spikes, and heavy loads. No server-side scripting ensures no overload.
- Helps you blog offline, run your own private blog, information system, if you don't want to host it on the web, and still have a web like interface.
- Written in python: Simple to understand, simple to modify, but most of all, simpler to use. (Knowledge of python is not required, except for installation, which is explained in detail below.)

## How it works

1. Write the post in Markdown, save it as `post-title.md` or `posttitle.md` (or post_title.md) in a designated folder, say, `posts`. 

2. Run `python chisel.py` in a Terminal, and Chisel will parse all `.md`, `.markdown` or `.mdown` files in `posts` folder to another designated folder, say `www` in html -- ready to be served using a web server.

3. Sync [See Note] all files and folders from the local `www` folder to the root of your web host, and you've got a fully functioning web site.

(Note: There are a number of ways one can sync files, [git][], [rsync][], or plain vanilla (s)[ftp][]. The sync can be further automated using a (ana)cron job, or via the Automator.)

## Requirements

If you are using a Mac or Linux, then python comes pre-installed. In addition, you'll need just a few python packages for Chisel to function. They are as follow:

1. [Jinja2][ji] is a templating engine, developed by [Pocoo Team][pt].
2. [Markdown][md] is a text markup language, developed by [John Gruber][jg]. It's nearly plain text, i.e., zero learning curve, which is why it's awesome.
3. [jinja_markdown][jm] to render markdown in pages.

#### Install these on a [Mac OS X][m] via [pip][] -- python package installer:

    $ sudo easy_install pip
    Password:
    $ sudo pip install jinja2 markdown jinja2_markdown
    
#### On [Ubuntu][u] (Debian) linux:

    $ sudo apt-get install python-pip
    Password:
    $ sudo pip install jinja2 markdown jinja2_markdown

To update these packages, you may run the following:

    $ sudo pip install --upgrade jinja2 markdown jinja2_markdown

## Create a site structure on your computer (This is just an example)

    $ mkdir ~/site
    $ cd ~/site
    $ mkdir posts www chisel

Now download Chisel as a zip file or via git (`git clone git://github.com/ckunte/chisel.git`). Move the unzipped contents into `chisel` folder created above. The structure should look like this following:

    ~/site/
    ~/site/posts/
    ~/site/www/
    ~/site/chisel/
                 /README.md
                 /chisel.py
                 /templates/
                           /archive.html
                           /base.html
                           /detail.html
                           /home.html

While it is not required, keeping `chisel`, `posts`, and `www` separate is a good idea. It helps keep chisel folders clean (for future updates), aside from keeping the tool separated from the content you create using it (`posts`, and `www`).

Remember to open and edit templates, particularly `base.html` as it contains site name, description and other `meta` into in the `<head>` section hard-coded. In addition, you will need to update the settings below.

### Updating Settings to suit

Open `chisel.py` in a text editor and have a look at the section Settings. You may need to update the following:

    # Settings
    BASEURL = "http://mysite.net/" # Must end with a trailing slash.
    SOURCE = "../posts/"             # Must end with a trailing slash.
    DESTINATION = "../www/"          # Must end with a trailing slash.
    HOME_SHOW = 15                   # Number of entries to show on homepage.
    TEMPLATE_PATH = "./templates/"   # Path of Jinja2 template files.
    TIME_FORMAT = "%b %d, %Y"
    ENTRY_TIME_FORMAT = "%m/%d/%Y"
    FORMAT = lambda text: markdown.markdown(text, ['footnotes','smartypants',])

### Usage

    $ cd ~/Sites/chisel
    $ python chisel.py

### Sample Entry

`sample.markdown` (Note: Filenames shall not have spaces. Good examples: `hotel-california.md`, `i_love_cooking.md`, and so on):

    Title of the post
    3/14/1879

    Content in Markdown here onward.

    Next paragraph.

    Next paragraph.

The very simple post entry format, shown above, is as follows:

- Line 1: Enter a Title.
- Line 2: Enter date in m/d/Y format.
- Line 3: Blank line.
- Line 4: Content in Markdown here onward.

### Adding Steps

Use the @step decorator. The main loop passes in the master file list and jinja environment. Here's an example of a `@step` decorator added to `chisel.py` to generate a colophon page:

Add this below in `chisel.py` code:

    @step
    def gen_colophon(f, e):
        write_file('colophon' + URLEXT, e.get_template('colophon.html').render(entry=file))

### Clean URLs - Howto

GitHub (via nginx rewrite I think) recognizes post files ending with `.html` or feed URLs ending with `.xml`. So, generate the files with these extensions as usual, but tell chisel to skip the extensions in permalinks using settings. (Follow up by excluding .html extension in hard links in Jinja templates too.)

The default setting in chisel now -- assuming server recognizes `.html` extension but does not require its inclusion when referring to a URL -- is as follows:

    URLEXT = ""
    
This above is what I use. (Note that you should not set both to empty or `.html` strings in the above; this would lead to unintended results.)

The fallback option is as follows:

    URLEXT = ".html"

This above setting would be suitable if your server does not recognize `.html` files if they are referred to without `.html` extension in URLs.

#### Local server at home

Since I also run chisel on my home server, here's what I had to do to enable rewrite using nginx web server:

I edited the `default` file, which serves our local family site, in the following folder on my home server:

    cd /etc/nginx/sites-enabled

and added this following in it:

    location / {
        try_files $uri.html $uri/ =404;
        error_page 404 = /404.html;
    }

I now get clean URLs with these above settings.

### Can I use this to run a site locally, like offline?

Yes! Just navigate to `~/site/www` and run the following to start a simple HTTP server in Terminal:

    $ python -m SimpleHTTPServer

Then, point your browser to: `http://localhost:8000` and your site is live on your computer.

### I have a large number of posts in WordPress. How do I convert?

Have a look at Thomas Frössman's tool, [exitwp][ep]. While it's written primarily for Jekyll, it does a very good job of converting all WordPress posts to Markdown post -- one file per post. Each post thus converted shows some preformatted lines in the beginning. much of which you don't need in Chisel (You only require Title and Date in the format illustrated above.) You could either manually edit each markdown file, or you could fork Thomas's exitwp and change the following lines (between line 253 and 259) from

    yaml_header = {
          'title': i['title'],
          'date': i['date'],
          'slug': i['slug'],
          'status': i['status'],
          'wordpress_id': i['wp_id'],
        }

to

       yaml_header = {
          i['title'],
          i['date'],
        }

Further, the date would need a fix to read as m/d/Y. But at least for now, it reduces your edits to just changing dates. Or you could write a [shell script][ss] to chuck out needless information generated for Jekyll to suit Chisel.

## I miss pinging my site via Pingomatic. How do I?

Create and save a bookmarklet via [Pingomatic][p]. Alternatively, put the following script (hat-tip: [Ned Batchelder][nb] for this script) in a file, say `ping.py`, and run `python ping.py` (please do remember to change the title and URL in the script below):

    # encoding: utf-8
    #!/usr/bin/env python

    import xmlrpclib

    # Ping-o-matic the Pinging service:
    ps = "http://rpc.pingomatic.com/RPC2"

    # Your site's title, url and rss:
    title = "Site title"
    url = "http://mysite.net"
    rss = "http://mysite.net/log/rss"

    remoteServer = xmlrpclib.Server(ps)
    ret = remoteServer.weblogUpdates.ping(title, url, rss)
    print title, ret['message']

To map by pinging each and every post from an entire site, one may use a script like below using archive.html page as the sitemap:

    #!/usr/bin/env python
    # encoding: utf-8
    """
    mapsite.py
    2014-06-07: Created by ckunte.
    2014-08-28: Updated to urllib3, and beautifulsoup4.

    Requirements:
        1. beautifulsoup4 module. (pip install beautifulsoup4)
        2. A file named srvclst.txt with ping servers list.
        
    Usage:
    
        $ python mapsite.py

    """
    import bs4
    import urllib3
    import xmlrpclib

    #--- Start edit: site details ---------------------
    # For absolute links: SITEURL = ''
    # For relative links: SITEURL = 'http://mysite.com'
    SITEURL = 'http://mysite.com'
    SITETITLE = 'Site title'
    SITEMAP = 'http://mysite.com/log/archive.html'
    #--- End edit. ------------------------------------

    def main():
        servers = [line.strip() for line in open('srvclst.txt', 'r')]
        http = urllib3.PoolManager()
        html_page = http.urlopen('GET', SITEMAP, preload_content=False)
        soup = bs4.BeautifulSoup(html_page)
        for link in soup.find_all('a'):
            title = SITETITLE + ": " + link.contents[0]
            url = SITEURL + link.get('href')
            for ps in servers:
                remoteServer = xmlrpclib.Server(ps)
                push = remoteServer.weblogUpdates.ping(title, url)
                print title, push['message']
            pass
        pass

    if __name__ == '__main__':
        main()

In addition, all update services may be populated in a file called `srvclst.txt`, e.g.,

    http://rpc.pingomatic.com/RPC2
    http://blogsearch.google.com/ping/RPC2
    http://rpc.weblogs.com/RPC2

Stepping through the code above, here's what it does:

- Lines between 20 and 22 require some basic input, viz., sitemap url, site title, and site url. (For absolute urls, site url may be left blank. Since, I use relative urls, I define a root.)
- Line 22 defines the sitemap, and is called into BeautifulSoup on line 29.
- Line 26 converts a list of servers/services (one per line) from `srvclst.txt` and turns it in to a proper python list.
- Each link (within `a` html tags), together with the linked text as its title in sitemap (or my Archive page) is pushed to all servers/services in the list --- defined above (line 30).
- Line 36 prints the title of the page, and each server's response to the push.

## My blog is now powered by Chisel. How do I automate all this?

Easy. Put this in a script (say, `log.sh`, for example) like the example below (do take note of folders, these are from my set-up, if yours is setup differently, then do make those changes in lines 3, 5, and 10 below):

    #!/usr/bin/env sh
    echo ""
    cd ~/Sites/chisel
    python chisel.py
    cd ~/Sites/mysiterepo.github.io
    echo "Updating log.."
    git add -A
    git commit -m 'Updating log.'
    git push -u origin master
    cd ~/Sites/chisel
    echo "Pinging Pingomatic.."
    python ping.py
    cd ~/
    echo ""
    echo "All done."

When you're ready to generate and post it to your site, run `sh log.sh`, and your post(s) are published.

## MathJax support

For enabling MathJax (TEX-AMS_HTML), the following script may be added in the `head` section:

    <script defer src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
    
The URL may be suitably changed to suit if other forms of markup is desired for for rendering. Please see mathjax website for more details on implementation.

For inline TEX rendering, the following may be added before the `</head>` tag in `base.html` template.

    <script type="text/x-mathjax-config">
       MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
    </script>

For a new equation, remember to use `\newline` instead of `\n`.

[ss]: http://www.cyberciti.biz/faq/unix-linux-replace-string-words-in-many-files/
[ep]: https://github.com/thomasf/exitwp
[dz]: https://github.com/dz
[ch]: https://github.com/ckunte/chisel
[ftp]: http://panic.com/transmit/
[py]: http://www.python.org/
[ji]: http://jinja.pocoo.org/docs/
[md]: http://daringfireball.net/projects/markdown/
[sp]: http://daringfireball.net/projects/smartypants/
[ad]: http://www.dalkescientific.com
[pt]: http://www.pocoo.org/ "Led by Georg Brandl and Armin Ronacher."
[jg]: http://daringfireball.net/ "John Gruber"
[rsync]: http://en.wikipedia.org/wiki/Rsync
[git]: http://git-scm.com
[u]: http://www.ubuntu.com/
[m]: http://www.apple.com/macosx
[pip]: http://pypi.python.org/pypi/pip
[nb]: http://nedbatchelder.com/blog/200406/pingomatic_and_xmlrpc.html "Ping-o-matic and xml-rpc"
[p]: http://pingomatic.com/
[mj]: http://www.mathjax.org/
[tx]: http://en.wikipedia.org/wiki/LaTeX
[c]: https://github.com/ckunte
[jm]: https://github.com/danielchatfield/jinja2_markdown