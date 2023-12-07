from fastapi import status
from fastapi.exceptions import HTTPException
from api.entidades.Item import Categoria
from infra.repository.category_repository import CategoryRepository, Category

class CategoryMediator:
    def __init__(self):
        self.repo = CategoryRepository()
    
    def create_category(self, categoria:Categoria):
        '''Verifica se a categoria já existe no banco. Caso esteja tudo OK cria a categoria no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será criado no banco de dados
        '''
        if self.get_category(categoria):
            raise HTTPException(
                detail="Categoria já existente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        category_db = Category(
            nome=categoria.nome.capitalize(),
            descricao=categoria.descricao
        )
        self.repo.insert(category_db)
    
    def get_category(self, categoria:Categoria):
        '''Verifica se a categoria existe no banco de dados
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será verificado no banco de dados
        '''
        return self.repo.select_by_name(categoria)
    
    def get_categories(self):
        '''Retorna todas as categorias do banco de dados'''
        return self.repo.select()
    
    def edit_category(self, categoria:Categoria):
        '''Verifica se a categoria existe no banco de dados. Caso esteja tudo OK acessa
        a categoria e edita os dados no banco de dados. Caso não retorna uma mensagem de erro
        
        Keyword arguments:

        categoria -- Objeto do tipo Categoria que será editado no banco de dados
        '''
        if not self.get_category(categoria):
            raise HTTPException(
                detail="Categoria não existente",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        self.repo.update(categoria)