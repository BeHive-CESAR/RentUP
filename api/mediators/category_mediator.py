from fastapi import status
from fastapi.exceptions import HTTPException
from api.entidades.Item import Categoria, CategoriaName
from infra.repository.category_repository import CategoryRepository, Category

class CategoryMediator:
    def __init__(self):
        self.repo = CategoryRepository()
    
    def create_category(self, categoria:Categoria):
        '''Verifica se a categoria já existe no banco. Caso esteja tudo OK cria a categoria no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será criado no banco de dados
        '''
        if self.get_category(categoria.nome):
            raise HTTPException(
                detail="Categoria já existente",
                status_code=status.HTTP_409_CONFLICT
            )
        
        category_db = Category(
            nome=categoria.nome.capitalize(),
            descricao=categoria.descricao
        )
        self.repo.insert(category_db)
    
    def get_category(self, categoria:str):
        '''Verifica se a categoria existe no banco de dados
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será verificado no banco de dados
        '''
        return self.repo.select_by_name(categoria.capitalize())
    
    def get_category_by_id(self, categoria_id:int):
        '''Verifica se a categoria existe no banco de dados
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será verificado no banco de dados
        '''
        return self.repo.select_by_id(categoria_id)
    
    def get_categories(self):
        '''Retorna todas as categorias do banco de dados'''
        return self.repo.select()
    
    def edit_category(self, categoria_atual:str ,categoria:Categoria):
        '''Verifica se a categoria existe no banco de dados. Caso esteja tudo OK acessa
        a categoria e edita os dados no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será editado no banco de dados
        '''
        if not self.get_category(categoria_atual):
            raise HTTPException(
                detail="Categoria não existente",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if categoria_atual != categoria.nome:
            if self.get_category(categoria.nome):
                raise HTTPException(
                    detail="Categoria já existente",
                    status_code=status.HTTP_409_CONFLICT
                )
        new_category = Category(
            id = self.get_category(categoria_atual).id,
            nome=categoria.nome.capitalize(),
            descricao=categoria.descricao
        )
        self.repo.update(new_category)
    