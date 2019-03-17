## local-go-slash
local link shortener

## Setup
You'll need an `/etc/hosts` entry or something equivalent if you want to
access this thing at (for example) `go/`. Here's mine:

```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1       localhost
255.255.255.255 broadcasthost
::1             localhost

# Add this
127.0.0.1 go
```

#### In general,
* Clone this repo somewhere (and add `slash` to your path)
* Create a sqlite database file somewhere to keep your links
* Set a `LOCAL_GO_SLASH_DB_FILE` in your env pointing to the database file
* Run. `slash -h` for help

#### To replicate my specific setup,
```
mkdir -p ~/bin/src/
git clone git@github.com:cqsd/local-go-slash.git ~/bin/src/
cd ~/bin/src/local-go-slash
sqlite3 links.db < schema.sql
ln -sf ~/bin/src/local-go-slash/slash ~/bin/
```

Then add `~/bin` to your path, and set `LOCAL_GO_SLASH_DB_FILE` in your env
pointing to `~/bin/src/local-go-slash/links.db`.

## Usage
```
$ slash -h
usage: go-slash [-h] [-f PATHS_FILE] {list,ls,add,rm,mv,run} ...

Local go/ server admin tool

optional arguments:
  -h, --help            show this help message and exit
  -f PATHS_FILE, --paths-file PATHS_FILE
                        specific sqlite db to list from

subcommands:
  {list,ls,add,rm,mv,run}
    list (ls)           List available links
    add                 Add a link
    rm                  Remove a link
    mv                  Rename a link
    run                 Run the server
```

#### Example: Add a link and run
```
uid=501|~/b/s/local-go-slash $ slash add tweet https://twitter.com
Added tweet --> https://twitter.com
uid=501|~/b/s/local-go-slash $ slash run 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Assuming you've added the `/etc/hosts` entry, you can now go to `go/tweet`
in your browser, and will be redirected to Twitter.
