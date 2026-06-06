{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :no-members:
   :show-inheritance:

{% block attributes %}
{% if attributes %}
.. rubric:: {{ _('Attributes') }}

{# Removed :toctree: so it doesn't create duplicate files #}
.. autosummary::
{% for item in attributes %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block methods %}
{% if methods %}
.. rubric:: {{ _('Methods') }}

{# Removed :toctree: so it doesn't create duplicate files #}
.. autosummary::
   :nosignatures:
{% for item in methods %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{# Detailed docstrings for everything #}
.. rubric:: Detailed Members Reference

{% block attributes_documentation %}
{% if attributes %}
{% for item in attributes %}
.. autoattribute:: {{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block methods_documentation %}
{% if methods %}
{% for item in methods %}
{% if item != '__init__' %}
.. automethod:: {{ name }}.{{ item }}
{% endif %}
{%- endfor %}
{% endif %}
{% endblock %}

.. minigallery:: {{ fullname }}
   :add-heading: