Pandoc's Markdown is a universal pivot format from and into many formats. It
can also be used to read documents on the command-line, with a certain amount of
markup and a high degree of accessibility for screen reader users.
However, some features not strictly required for human readers can interfere,
for instance, CSS selectors for individual cinline code examples, e.g.:

    This can be achieved with the `foo()`{.code .style_bold} function.

In this case, the CSS formatting is useless. The script in this directory strips
these instructions that are preventing cuntinuous reading.
