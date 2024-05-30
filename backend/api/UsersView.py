from starlette.responses import JSONResponse, Response
from backend.managers.UsersManager import UsersManager
from backend.paths import api_base_url

class UsersView:
    def __init__(self):
        self.um = UsersManager()

    async def get(self, user_id: str):
        user = await self.um.retrieve_user(user_id)
        if user is None:
            return JSONResponse(status_code=404, headers={"error": "User not found"})
        return JSONResponse(user, status_code=200)

    async def post(self, body: dict):
        user_id = await self.um.create_user(body['name'], body['email'])
        return JSONResponse({"id": user_id}, status_code=201, headers={'Location': f'{api_base_url}/users/{user_id}'})
    
    async def put(self, user_id: str, body: dict):
        await self.um.update_user(user_id, body['name'], body['email'])
        return JSONResponse({"message": "User updated successfully"}, status_code=200)

    async def delete(self, user_id: str):
        await self.um.delete_user(user_id)
        return Response(status_code=204)

    # TODO: support react-admin GET /api/v1/users?id=5bae4a90-ce69-4483-86ef-d723258f21e5&id=432ec697-fd50-495b-bb35-cf0c9fcd92bb HTTP/1.1 ?
    async def search(self, limit=100):
        users = await self.um.retrieve_all_users(limit)
        return JSONResponse(users, status_code=200, headers={'X-Total-Count': str(len(users))})
