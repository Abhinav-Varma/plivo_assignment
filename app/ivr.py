from fastapi import APIRouter, Request
from fastapi.responses import Response
from plivo import xml

from app.config import ASSOCIATE_NUMBER, BASE_URL

router = APIRouter()


@router.post("/ivr")
async def language_menu(request: Request):
    response = xml.ResponseElement()

    get_digits = xml.GetDigitsElement(
        action=f"{BASE_URL}/menu",
        method="POST",
        timeout=7,
        num_digits=1,
        retries=2
    )

    get_digits.add(
        xml.SpeakElement(
            "Press 1 for English. Press 2 for Spanish."
        )
    )

    response.add(get_digits)
    response.add(xml.SpeakElement("No input received. Goodbye."))

    return Response(content=response.to_string(), media_type="application/xml")


@router.post("/menu")
async def second_menu(request: Request):
    form = await request.form()
    digit = form.get("Digits")

    response = xml.ResponseElement()

    if digit in ["1", "2"]:
        get_digits = xml.GetDigitsElement(
            action=f"{BASE_URL}/action",
            method="POST",
            timeout=7,
            num_digits=1,
            retries=2
        )

        get_digits.add(
            xml.SpeakElement(
                "Press 1 to hear a message. Press 2 to talk to an associate."
            )
        )

        response.add(get_digits)

    else:
        response.add(xml.SpeakElement("Invalid input. Try again."))
        response.add(
            xml.RedirectElement(f"{BASE_URL}/ivr")
        )

    return Response(content=response.to_string(), media_type="application/xml")


@router.post("/action")
async def action_menu(request: Request):
    form = await request.form()
    digit = form.get("Digits")

    response = xml.ResponseElement()

    if digit == "1":
        response.add(
            xml.PlayElement(
                "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            )
        )

    elif digit == "2":
        dial = xml.DialElement()
        dial.add(xml.NumberElement(ASSOCIATE_NUMBER))
        response.add(dial)

    else:
        response.add(xml.SpeakElement("Invalid input."))
        response.add(xml.RedirectElement(f"{BASE_URL}/menu"))

    return Response(content=response.to_string(), media_type="application/xml")
