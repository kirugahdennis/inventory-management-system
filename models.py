
import database


class Item:
    def __init__(self, id, name, barcode=None, quantity=0, price=0.0,
                 category=None, brand=None, image_url=None,
                 ingredients_text=None):
        self.id = id
        self.name = name
        self.barcode = barcode
        self.quantity = quantity
        self.price = price
        self.category = category
        self.brand = brand
        self.image_url = image_url
        self.ingredients_text = ingredients_text

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def _from_dict(cls, d):
        return cls(**d) if d else None

    @classmethod
    def create(cls, name, barcode=None, quantity=0, price=0.0,
               category=None, brand=None, image_url=None,
               ingredients_text=None):
        new_item = {
            "id": database.get_next_id(),
            "name": name,
            "barcode": barcode,
            "quantity": quantity,
            "price": price,
            "category": category,
            "brand": brand,
            "image_url": image_url,
            "ingredients_text": ingredients_text,
        }
        database.items.append(new_item)
        return cls._from_dict(new_item)

    @classmethod
    def find_all(cls):
        return [cls._from_dict(d) for d in database.items]

    @classmethod
    def find_by_id(cls, item_id):
        for d in database.items:
            if d["id"] == item_id:
                return cls._from_dict(d)
        return None

    def update(self, **fields):
        for d in database.items:
            if d["id"] == self.id:
                d.update({k: v for k, v in fields.items() if k in d})
                for k, v in d.items():
                    setattr(self, k, v)
                return self
        return None

    def delete(self):
        global_items = database.items
        database.items[:] = [d for d in global_items if d["id"] != self.id]

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r} quantity={self.quantity}>"