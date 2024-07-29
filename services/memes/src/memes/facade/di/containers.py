from dishka import make_async_container

from memes.facade.di import providers


adapter_container = make_async_container(providers.AdapterProvider())
