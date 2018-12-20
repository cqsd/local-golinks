## local-go-slash

Simple Python link shortener intended to run on `localhost`. I use mine to
provide a local `go/` link shortener, since my company doesn't yet have one
(or any extant want for one).

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

127.0.0.1 go
```

#### In general,
* Clone this repo somewhere (and add `go-slash` to your path)
* Create a sqlite database file somewhere to keep your links
* Set a `LOCAL_GO_SLASH_DB_FILE` in your env pointing to the database file
* Run. `go-slash -h` for help

#### To replicate my specific setup,
```
mkdir -p ~/bin/src/
git clone git@github.com:cqsd/local-go-slash.git ~/bin/src/
cd ~/bin/src/local-go-slash
sqlite3 links.db < schema.sql
ln -sf ~/bin/src/local-go-slash/go-slash ~/bin/
```

Then add `~/bin` to your path, and set `LOCAL_GO_SLASH_DB_FILE` in your env
pointing to `~/bin/src/local-go-slash/links.db`.
