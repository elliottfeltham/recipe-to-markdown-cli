# Recipe to Markdown Parser

A simple CLI which lets you enter the URL of a recipe from a webpage and then format it into a markdown file.

Currently this works with several recipe websites which use the [schema.org JSON-LD](https://schema.org/Recipe) JSON-LD format. The program scrapes the webpage and parses the data from the correct JSON-LD and then saves the recipe as Markdown in my Obsidian folder!

A better way to do this for a more usable product would be to use a well established library like [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) which has support for a huge growing list of recipe sites, but as a learning project I wanted to explore web scraping in a way that was practical and useful for myself.

I plan on making a better version as a simple web app which will use the `recipe-scrapers` library.
