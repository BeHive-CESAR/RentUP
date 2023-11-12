from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from api.mediators.rent_mediator import RentMediator, Rent

'''
rentup_item(Rent)
+ return_item(Rent)
+ get_history()
+ get_history_by_item(Item)
+ get_history_by_user(User)
'''

class RentController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/rent")
        def rent_item(rent: Rent):
            try:
                RentMediator().rentup_item(rent)
                return JSONResponse(content='Empréstimo realizado com sucesso' ,status_code=status.HTTP_201_CREATED)
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content=e.detail)

        @self.router.post("/return")
        def return_item(rent):
            try:
                RentMediator().return_item(rent)
                return JSONResponse(content='Devolução realizada com sucesso' ,status_code=status.HTTP_201_CREATED)
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content=e.detail)

        @self.router.get("/history")
        def get_history(self):
        try:
            history = RentMediator().get_history()
            return JSONResponse(status_code=status.HTTP_200_OK, content=history)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


        @self.router.get("/history-item")
        def get_history_by_item(item):
            pass

        @self.router.get("/history-user")
        def get_history_by_user(user):
            pass

        @self.router.put("/update-status")
        def update_status(rent, status):
            pass
