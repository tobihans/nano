# Nano

> Django is one of the most interesting framework to me for many reasons.
> But the lack of proper integration with modern frontend tools makes it
> difficult for me to prototype my apps like I can easily do in Rails.
> This template is my attempt to that have a simple build
> pipeline inspired by Rails assets build system.

## Stack

- **Backend**: Django 6, SQLite (WAL mode), pydantic-settings
- **Frontend**: Tailwind CSS v4, basecoat-css, Alpine.js, esbuild
- **Auth**: Custom email-based (signup w/ verification, login, logout, password reset)
- **Emails**: MJML templates via mrml
- **Dev**: mprocs (parallel processes), django-debug-toolbar, django-browser-reload

## Getting Started

```bash
uv sync
npm install
cp .env.example .env  # configure your env
uv run python manage.py migrate
mprocs
```

## TODO

- [ ] Make notes demo behave like SPA with alpine-ajax
- [ ] Custom `collectstatic` management command that runs esbuild and compiles Tailwind before collecting
