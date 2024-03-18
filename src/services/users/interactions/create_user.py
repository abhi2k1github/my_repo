from services.users.models.user import User


def create_user(request):
    with User._meta.database.atomic():
        return execute_transaction(request)
    
def execute_transaction(request):
    user = User.select().where(User.email == request.email)
    if not user:
        create_params = get_create_params(request)
        if not create_params["status"]:
            create_params["status"] = "active"
        user = User(**create_params)
    if create_params["password"]:
        password_hash = user.get_password_hash(request.password)
        user.password_digest = password_hash
    user.save()

    return {"id": user.id}


def get_create_params(request):
    return request.model_dump(
        include={"name", "email", "mobile_number", "mobile_country_code", "status"},
        exclude_none=True,
    )
