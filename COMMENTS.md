During the development of the project, I focused on using async requests whenever possible.

That's because of the cases which we have external API calls alongside DB operations (such as getting average ratings).

The Gutendex API do not provide an way to query only by the book title. Instead, it appears to use a similarity query for both the title or book author.
