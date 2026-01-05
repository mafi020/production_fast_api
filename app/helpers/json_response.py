from fastapi.responses import JSONResponse

def success_response(data, status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "success": True,
            "body": data,
            "error": None,
        }
    )

def error_response(message, status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "success": False,
            "body": None,
            "error": message,
        }
    )
