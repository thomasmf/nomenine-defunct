---
layout: default
---

<div class="nom-posts">
  {% for post in site.posts %}
    {% include post.html-fragment %}
  {% endfor %}
</div>

