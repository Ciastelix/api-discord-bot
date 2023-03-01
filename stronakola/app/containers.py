from dependency_injector import containers, providers
from app.db import Database
from app.repository import UserRepository
from app.services import UserService
from dotenv import load_dotenv
class Container(containers.DeclarativeContainer):
    load_dotenv()
    wiring_config = containers.WiringConfiguration(modules=["app.endpoints"])
    config = providers.Configuration()
    config.db.url.from_env("DATABASE_URL")  
    db = providers.Singleton(Database, db_url=config.db.url)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
        
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )   
