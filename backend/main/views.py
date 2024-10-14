import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger("django")

class LoggedListModelMixin:
    def list(self, request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return super().list(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

class LoggedCreateModelMixin:
    def create(self, request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return super().create(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

class LoggedRetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return super().retrieve(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

class LoggedUpdateModelMixin:
    def update(self, request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return super().update(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

class LoggedDestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return super().destroy(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

def make_logged(func): 
    def new_func(request, *args, **kwargs):
        caption = f"[{request.method}] {request.get_full_path()}"
        try:
            logger.info(f"{caption}: started")
            return func(request, *args, **kwargs)
        except:
            logger.error(f"{caption}: exception")
            raise
        finally:
            logger.info(f"{caption}: succesfully ended")

    return new_func 