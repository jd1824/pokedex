import flet as ft
import asyncio
import aiohttp

pokemon_actual = 0
async def main(page: ft.page):
    page.window_width = 600
    page.window_height = 750
    page.window_resizable = False
    page.padding = 0
    

    #funciones
    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def evento_get_pokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -= 1

        numero = (pokemon_actual%150)+1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos = f"Name: {resultado['name']}\n\nAbilities:"
        for elemento in resultado['abilities']:
            habilidad = elemento["ability"]["name"]
            datos += f"\n{habilidad}"
        datos += f"\n\nHeight: {resultado['height']}"

        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url

        texto.value = datos
        await page.update_async()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()

    luz_azul = ft.Container(width=70, height=70, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=50)
    boton_azul = ft.Stack([
        ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=50),
        luz_azul
    ])

    items_superior = [
        ft.Container(boton_azul ,width=80, height=80),
        ft.Container(width=40, height=40, bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.GREEN, border_radius=50)
        ]

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    imagen = ft.Image(
        src=sprite_url,
         scale=10,
         width=20,
        height=20,
        top=200/2,
        right=350/2
    )
    stack_central = ft.Stack([
        ft.Container(width=400, height=300, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(width=350, height=200, bgcolor=ft.colors.BLACK, top=25, left=25),
        imagen,

    ])

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(30, 0),
            ft.canvas.Path.LineTo(0, 30),
            ft.canvas.Path.LineTo(60, 30)
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL,
            ),
        ),
    ],
    width=80,
    height=25
    )

    flecha_superior = ft.Container(triangulo ,width=80, height=40, on_click=evento_get_pokemon)
    flechas = ft.Column(
        [
            flecha_superior,
            ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159) ,width=80, height=40, on_click=evento_get_pokemon),
        ]
    )

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=18
        )

    items_inferior = [
        ft.Container(width=50), #margen izquierdo
        ft.Container(texto, padding=10, width=225, height=225, bgcolor=ft.colors.GREEN, border_radius=20),#cosa verde
        ft.Container(flechas ,width=60, height=100),
        ft.Container(width=47) #margen derecho
    ]

    superior = ft.Container(content=ft.Row(items_superior), width=400, height=80, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central ,width=400, height=250, margin=ft.margin.only(top=40),
                          alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior) ,width=400, height=250, margin=ft.margin.only(top=40))

    col = ft.Column(spacing=0, controls=(
        superior,
        centro,
        inferior,
    ))
    contenedor = ft.Container(col, width=720, height=1200, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blink()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)