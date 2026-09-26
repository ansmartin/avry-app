
class StatusCode:
    
    def ok() -> dict:
        return { "status":200, "message":"Ok" }

    def not_found() -> dict:
        return { "status":404, "message":"Not Found" }

    def duplicated() -> dict:
        return { "status":409, "message":"Duplicated" }

    def error() -> dict:
        return { "status":500, "message":"Internal Server Error" }
