---
layout: default
---

<h1>Posts</h1>
<ul class="nom-posts">
  {% for post in site.posts %}
  <li>
    {{ post.date | date:"%Y-%m-%d" }}
    <a href="{{ post.url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>

<div class="nom-posts">
  {% for post in site.posts %}
    {% include post.html-fragment %}
  {% endfor %}
</div>

