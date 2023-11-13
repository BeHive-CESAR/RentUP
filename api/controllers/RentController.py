from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from api.mediators.rent_mediator import RentMediator, Rent, Status, UserMediator, ItemMediator
from api.mediators.item_mediator import BaseItem
from api.depends import auth_admin


class RentController:
    def __init__(self):
        self.router = APIRouter()

        @self.router.post("/rent")
        def rent_item(rent: Rent):
            RentMediator().rentup_item(rent)
            return JSONResponse(
                content='Empréstimo realizado com sucesso',
                status_code=status.HTTP_201_CREATED
            )

        @self.router.put("/return")
        def return_item(rent_id:int):
            RentMediator().return_item(rent_id)
            return JSONResponse(
                content='Devolução realizada com sucesso',
                status_code=status.HTTP_201_CREATED
            )

        @self.router.get("/history")
        def get_history(token_verify=Depends(auth_admin)):
            history = RentMediator().get_history()
            
            history_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, } for item_data in history]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=history_data
            )


        @self.router.get("/history-item")
        def get_history_by_item(item:str):
            history_item = RentMediator().get_history_by_item(BaseItem(nome=item))
            
            history_item_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, }for item_data in history_item]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"rents": history_item_data}
            )

        @self.router.get("/history-user")
        def get_history_by_user(user_email:str):
            history_user = RentMediator().get_history_by_user(user_email)
            history_user_data = [{
                'id': item_data.id,
                'user': UserMediator().get_user_by_id(item_data.user_id).nome,
                'item': ItemMediator().get_item_by_id(item_data.item_id).nome_item,
                'data_emprestimo': str(item_data.data_emprestimo),
                'data_devolução': str(item_data.data_devolucao),
                'estado': item_data.estado, }for item_data in history_user]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"rents": history_user_data}
            )

        @self.router.put("/update-status")
        def update_status(id_rent:int, stat:Status, token_verify=Depends(auth_admin)):
            RentMediator().update_status(id_rent, stat)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Status atualizado com sucesso"}
            )
        
        
