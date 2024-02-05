from telebot.types import InputMediaPhoto
from car import Car, CarStatus


def car_to_message(car: Car) -> list[InputMediaPhoto]:
    media_group = []
    for index, photo in enumerate(car.images):
        media_photo = InputMediaPhoto(photo, parse_mode='HTML')
        if index == 0:
            media_photo.caption = get_car_text(car)
        media_group.append(media_photo)

    return media_group


def get_car_text(car: Car):
    return f"""<b>{get_car_status_text(car)}</b>
🚗 <a href='{car.autoria_link}'>{car.name}</a>
💵 {car.new_price:0,.0f}
⚙️ {car.mileage}
📌 {car.city}
{("🇺🇸" + "<a href='" + car.bidfax_link + "'>bidfax</a>") if car.bidfax_link else ''}"""



def get_car_status_text(car: Car):
    match car.status:
        case CarStatus.new:
            return "🆕 З'явилась нова машина!"
        case CarStatus.price_changed:
            price_difference = (car.new_price - car.old_price) * -1
            return f'📈 Ціна виросла на +{price_difference}' if price_difference > 0 else f'📉 Ціна знизилась на -{price_difference}'
