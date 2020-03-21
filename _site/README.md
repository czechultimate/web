# czechultimate website

## TODO

- `jekyll build` volat automaticky v CI .. to asi dela sam github v pripade GH pages
- aby node_modules nebyly ignorovany v GH pages: https://www.bennadel.com/blog/3181-including-node-modules-and-vendors-folders-in-your-github-pages-site.htm

## Prerequisites

Install docker and docker-compose.

## How to run

Run `docker-compose up` and open `localhost:4000` in your favourite web browser.

## How to build

Only if you need that. It's not necessary to run it.

```
docker run --rm -it --volume="$PWD:/srv/jekyll" --env JEKYLL_ENV=production jekyll/jekyll jekyll build
```

## How to add dependency

Update Gemfile and run `docker-compose down && docker-compose up`.

## Semantic UI

### How to install

```bash
# install nodejs and gulp
npm install semantic-ui --save
cd semantic/
gulp build
```

### How to update

```
npm update
```
