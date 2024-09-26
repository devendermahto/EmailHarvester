app_emailharvester = None

def search(domain, limit):
    # Naver search query URL
    url = "https://search.naver.com/search.naver?query=%40{word}&start={counter}"
    app_emailharvester.init_search(url, domain, limit, 0, 50, 'Naver')
    app_emailharvester.process()
    return app_emailharvester.get_emails()

class Plugin:
    def __init__(self, app, conf):
        global app_emailharvester, config
        # Register the Naver plugin
        app.register_plugin('naver', {'search': search})
        app_emailharvester = app
