---
Title: CV
---
{% for section in db.sections %}
{% if section.title=='Education' or section.title=='Computing Skills' or section.title=='Publications' or section.title=='Talks and Posters'%}
## {{ section.title }}
{% if section.cvitems %}
{% for item in section.cvitems %}
* <div class="lead">{{ item.name }}: {{ item.value }}</div>
{% endfor %}
{% elif section.cvlistitems %}
{% for item in section.cvlistitems %}
* <div class="lead">{{ item }}</div>
{% endfor %}
{% else %}
{% for entry in section.entries %}
* <div class="lead">{{ entry|md_section_sorter(section.title) }}</div>
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}
{% if pdf_link %}
<center><div class="lead">A complete version of my CV can be found [here]({{ pdf_link }})</div></center>
{% endif %}
