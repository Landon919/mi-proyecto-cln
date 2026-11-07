from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database import Base

class PedidoModel(Base):
    __tablename__ = "pedidos"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    cliente_id: Mapped[str] = mapped_column(String)
    estado: Mapped[str] = mapped_column(String)
    promocion_activa: Mapped[bool] = mapped_column(Boolean, default=False)
    autorizado: Mapped[bool] = mapped_column(Boolean, default=True)
    motivo_cancelacion: Mapped[str | None] = mapped_column(String, nullable=True)
    lineas: Mapped[list] = mapped_column(JSON)