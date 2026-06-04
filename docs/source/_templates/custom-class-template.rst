{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

{# 1. Render ONLY the main class docstring and Parameters #}
.. autoclass:: {{ objname }}
   :no-members:
   :show-inheritance:


{% block attributes %}
{% if attributes %}
.. rubric:: {{ _('Attributes') }}

{# 2. Render the Attributes Summary Table #}
.. autosummary::
   :toctree:
{% for item in attributes %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


{% block methods %}
{% if methods %}
.. rubric:: {{ _('Methods') }}

{# 3. Render the Methods Summary Table #}
.. autosummary::
   :toctree:
   :nosignatures:
{% for item in methods %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


{# 4. Now render the detailed docstrings for everything #}
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
{# Skip __init__ since your conf.py excludes it #}
{% if item != '__init__' %}
.. automethod:: {{ name }}.{{ item }}
{% endif %}
{%- endfor %}
{% endif %}
{% endblock %}


.. minigallery:: {{ fullname }}
   :add-heading: