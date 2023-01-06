---
layout: page
title: Categories
permalink: /categories/
---

<div id="archives">
{% for category in site.categories %}
  <div class="archive-group">
    {% capture category_name %}{{ category | first }}{% endcapture %}
    <div id="#{{ category_name | slugize }}"></div>
    <h5 class="category-head font-weight-bold m-0 pt-3 pt-md-4 pt-lg-5">{{ category_name | capitalize }}</h5>
    <a name="{{ category_name | slugize }}"></a>
    {% for post in site.categories[category_name] %}
    <article class="archive-item">
      <p><a href="{{ post.url | relative_url }}">{{post.title}}</a></p>
		{% if post.podcast_link %}
			<audio src="{{post.podcast_link}}" preload="auto" controls></audio>
		{% endif %}
    </article>
    {% endfor %}
  </div>
{% endfor %}
</div>