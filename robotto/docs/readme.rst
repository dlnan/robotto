The Imperative CMS!
===================

Robotto is a content management system made available entirely as a
library.

.. note:: This project is currently pure fiction. It's an experiment in documentation-driven development.

It stores content in native file formats in a human-readable hierarchy
on the file system. First-class content objects map to directories
with the convention that the content has the filename ``index.*``
where the extension determines the file format::

  /index.html
  /about/index.rst

We usually want to give content a human-readable short name, and the
directory model allows us to do this and still use the file extension
to determine the file type::

  http://localhost:8080/about

Thus we change content type without changing location.

Why?
----

The existing content management systems fall into two categories:
*frameworks* and *publishers*. The former are complex applications
that you must plug into, the latter output static content. The aim of
:mod:`Robotto` is to let you write CMS applications imperatively. The
batteries which frameworks typically provide are still included, but
you're in charge of connecting them.

Development is driven by documentation; no code is laid down before
it's been documented including a complete working example [#]_. These
examples make it easy to get started, simply by copying and
pasting. It also means the library is kept simple enough that an
example is all you need to have a running application.

.. [#] All examples are written using the :mod:`manuel` documentation testing framework. This allows us to continuously test the documentation against the library code and make sure that everything's in sync.

Batteries
---------

Out of the box comes support for HTML, formatted text and images.


Hello Robotto!
--------------

Below is a complete example application.

The application lets you view and edit supported files under some path
on the file system. During the course of the documentation, it will
evolve into an actual website, complete with a custom theme.

.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  import robotto
  import webob.exc
  import wsgiref.simple_server

  # use current directory as content repository; the repository
  # implements path traversal which maps the directory to a URL
  # mount point
  repo = robotto.Repository(".")

  app = robotto.Application(repo)

  edit = app.route("/\*/edit")
  view = app.route("/\*")

  @edit.controller(method="GET")
  def get(context, request):
      form = robotto.Form(context, params=request.params)
      return form(request)

  @edit.controller(method="POST")
  def post(context, request):
      form = robotto.Form(context, params=request.params)
      if form.validate():
         context.save()
         return webob.exc.HTTPTemporaryRedirect(
             location=view.path(context))
      return form(request)

  @view.controller
  def view(context, request):
      return context(request)

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Browse to any existing path relative to the current directory to see
the file. If we add ``/edit``, we can make changes and save the file.

All Robotto-objects know how to render themselves (to responses);
simply call them with a ``request`` object which asks for a particular
response type (browsers will normally ask for ``text/html``). See the
:ref:`getting started <getting-started>` section to learn how to give
your application a custom look and feel.

License
-------

This software is made available under the GPL license.

Getting started
===============

Setting out with the first example at hand, this section examines the
next steps in getting a site ready.

