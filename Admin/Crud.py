from abc import ABC, abstractmethod
import json

class CRUD(ABC):
    objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        if len(cls.objetos) == 0:
            new_id = 1
        else:
            new_id = (max(cls.objetos, key=lambda x: x.id)).id + 1
        obj.id = new_id
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls) -> list[object]:
        cls.abrir()
        return list(cls.objetos)

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.objetos:
            if obj.id == id:
                return obj
        return None
    
    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        existing = cls.listar_id(obj.id)
        if existing is not None:
            cls.objetos.remove(existing)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        existing = cls.listar_id(obj.id)
        if existing is not None:
            cls.objetos.remove(existing)
            cls.salvar()

    @classmethod
    @abstractmethod
    def abrir(cls):
        pass

    @classmethod
    @abstractmethod
    def salvar(cls):
        pass