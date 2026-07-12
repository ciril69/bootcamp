from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

# Specific Subclasses of AppException
class ProductNotFound(AppException):
    def __init__(self, message: str = "The requested product could not be found."):
        super().__init__(
            code="PRODUCT_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class CategoryNotFound(AppException):
    def __init__(self, message: str = "The requested category could not be found."):
        super().__init__(
            code="CATEGORY_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class CartNotFound(AppException):
    def __init__(self, message: str = "The requested cart could not be found."):
        super().__init__(
            code="CART_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class OrderNotFound(AppException):
    def __init__(self, message: str = "The requested order could not be found."):
        super().__init__(
            code="ORDER_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class InvalidQuantity(AppException):
    def __init__(self, message: str = "The quantity must be a positive integer."):
        super().__init__(
            code="INVALID_QUANTITY",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed."):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(f"AppException: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message
                }
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")
        code = "HTTP_ERROR"
        if exc.status_code == 404:
            code = "RESOURCE_NOT_FOUND"
        elif exc.status_code == 401:
            code = "UNAUTHORIZED"
        elif exc.status_code == 403:
            code = "FORBIDDEN"
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": str(exc.detail)
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(f"ValidationError: {exc.errors()}")
        # Format validation error message
        errors = exc.errors()
        messages = []
        for error in errors:
            loc = " -> ".join(str(x) for x in error.get("loc", []))
            msg = error.get("msg", "invalid value")
            messages.append(f"{loc}: {msg}")
        
        detail_message = "; ".join(messages) if messages else "Validation failed"
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": detail_message
                }
            }
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unexpected error occurred")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later."
                }
            }
        )
