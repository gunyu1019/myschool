from multiprocessing import cpu_count

bind = "unix:api_website.sock"

workers = cpu_count() * 2 + 1
worker_class = "gevent"

wsgi_app = "app:create_app()"

accesslog = "-"
