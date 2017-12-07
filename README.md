# resume
Produce a CV in any format you like using Jinja2 templates. See my 
[blog entry](http://wtbarnes.github.io/2016/08/28/cv-howto/) about developing and using this method for 
building my CV.

The templates included in `templates/` are for:

* markdown
* HTML
* LaTeX (`moderncv` class)

## LaTeX moderncv options
These are some options for different configurations of the `moderncv` TeX class. I've copied these out of a header from an old template courtesy of the LaTeX project and Xavier Danaux.

###Preamble

| font size | paper size | font family | style | color |
|:---------:|:----------:|:-----------:|:-----:|:-----:|
| 10pt | a4paper | sans | casual (default) | blue (default)|
| 11pt | a5paper | roman | classic | orange |
| 12pt | letterpaper |  | oldstyle | green |
|  | legalpaper |  | banking | red |
|  | executivepaper |  | | purple |
|  | landscape |  | | grey |
|  |  |  | | black |

Use `\nopagenumbers{}` to suppress automatic numbering on CVs more than one page.

All personal data is optional except the first and last name.

### Body
In `\cventry`, arguments 3 to 6 can be left empty.

### BibTeX Integration
Publications from a BibTeX file without multibib:
```
\nocite{*}
\bibliographystyle{plain}
\bibliography{publications}
```
where `publications` is the name of the `.bib` file.
