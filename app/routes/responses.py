def build_response(
    data: dict, status: int, message: str, error: str = ""
) -> tuple[dict, int]:
    response_dict = {"data": data, "status": status, "message": message, "error": error}
    return response_dict, status
