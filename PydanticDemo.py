from enum import Enum
from typing import Tuple

from pydantic import BaseModel, Field, validator, root_validator


class Topping(str, Enum):
    hot_fudge = 'hot_fundge'
    flakes = 'flakes'
    cinnamon = 'cinnamon'


class Flavor(str, Enum):
    mint = 'mint'
    chocolate = 'chocolate'
    coffee = 'coffee'


class Container(str, Enum):
    cup = 'cup',
    cone = 'cone',
    waffle_cone = 'waffle cone'


class IceCreamMix(BaseModel):
    name: str
    container: Container
    flavor: Flavor
    toppings: Tuple[Topping, ...]
    scoops: int = Field(..., gt=0, lt=5)

    @validator('toppings')
    def check_toppings(cls, toppings):
        if len(toppings) > 4:
            raise ValueError('Too many toppings')
        return toppings

    @root_validator
    def check_cone_toppings(cls, values):
        container = values.get('container')
        toppings = values.get('toppings')
        if container == Container.cone or Container.waffle_cone:
            if Topping.hot_fudge in toppings:
                raise ValueError('Cones cannot have hot fudge')
        return values


def main():
    ice_cream_mix = IceCreamMix(
        name="black and white",
        container=Container.waffle_cone,
        flavor=Flavor.chocolate,
        toppings=(Topping.flakes, Topping.cinnamon),
        scoops=2
    )

    print(ice_cream_mix.json())


if __name__ == '__main__':
    main()
