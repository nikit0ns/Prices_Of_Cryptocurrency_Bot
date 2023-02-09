from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pycoingecko import CoinGeckoAPI
import asyncio
import config


bot = Bot(token = config.TOKEN) #Ваш токен 
dp = Dispatcher()
coingecko = CoinGeckoAPI()


@dp.message(Command(commands = ['start']))
async def cmd_start(message: types.Message):
    await message.answer('👋 <b>Привіт, я Крипто Бот </b>💎\n'
                         '📊 <b>Ви зможете дізнатися курс Криптовалюти </b>💸\n\n'
                         '📚 <b>Курс Криптовалюти - /price</b>\n'
                         '<code> - Приклад команди - /price Bitcoin</code>\n'
                         '<b>⁉️ Технічна підтримка - /help</b>',
                         parse_mode = 'HTML')


@dp.message(Command(commands = ['help']))
async def cmd_help(message: types.Message):
    await message.answer("⁉️<b> Якщо у вас є проблеми.</b> \n"
                         "✉️ <b>Напишіть мені</b> <a href = 'https://t.me/nikit0ns'>@nikit0ns</a><b>.</b>", 
                         disable_web_page_preview = True, 
                         parse_mode = 'HTML')


@dp.message(Command(commands = 'price'))
async def cmd_price(message: types.Message):
    if message.text == '/price':
        await message.answer('⚠️ <b>Неправильно вибрана команда.</b>', parse_mode = 'HTML')
    else:
        try:
            currency = message.text[7:].capitalize()
            currency_symbol = message.text[7:].lower()
            result = coingecko.get_price(ids = currency, vs_currencies = 'usd', include_market_cap = True, include_24hr_vol = True, include_24hr_change = True)
            price = float(result[currency.lower()]['usd'])
            change = round(float(result[currency.lower()]['usd_24h_change']),1)
            market_cap = round(float(result[currency.lower()]['usd_market_cap']))
            volume = round(float(result[currency.lower()]['usd_24h_vol']))
            symbol = coingecko.get_coin_by_id(currency_symbol)["symbol"].upper()

            switcher_emodji = {
                True: '📈',
                False: '📉',
            }

            sign = '+' if change > 0 else ''
            change_emodji = switcher_emodji.get(change > 0) if change != 0 else '📊'

            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text = '🔄 Оновити', callback_data = f'update_{currency}_{symbol}'))

            await message.answer(f'💎 <b>Криптовалюта: {currency} ({symbol})</b>\n\n'
                                 f'{change_emodji} <b>Зміна ціни: {sign}{change}%</b>\n'
                                 f'💸 <b>Ціна: {price:,}$</b>\n'
                                 f'💰 <b>Ринкова капіталізація: {market_cap:,}$</b>\n'
                                 f'⏱ <b>24-годинний обсяг: {volume:,}$</b>',
                                 parse_mode = 'HTML',
                                 reply_markup = builder.as_markup())
        except (Exception, ValueError):
            await message.answer(f'⚠️ <b>Ця валюта не підтримується або є неправильною.</b>', parse_mode = 'HTML')


@dp.callback_query(Text(startswith = 'update'))
async def cmd_update(callback: types.CallbackQuery):
    _, currency, symbol = callback.data.split("_")
    try:
        result = coingecko.get_price(ids = currency, vs_currencies = 'usd', include_market_cap = True, include_24hr_vol = True, include_24hr_change = True)
        price = float(result[currency.lower()]['usd'])
        change = round(float(result[currency.lower()]['usd_24h_change']),1)
        market_cap = round(float(result[currency.lower()]['usd_market_cap']))
        volume = round(float(result[currency.lower()]['usd_24h_vol']))


        switcher_emodji = {
            True: '📈',
            False: '📉',
        }

        sign = '+' if change > 0 else ''
        change_emodji = switcher_emodji.get(change > 0) if change != 0 else '📊'

        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text = '🔄 Оновити', callback_data = f'update_{currency}_{symbol}'))
    
        await callback.message.edit_text(f'💎 <b>Криптовалюта: {currency} ({symbol})</b>\n\n'
                                         f'{change_emodji} <b>Зміна ціни: {sign}{change}%</b>\n'
                                         f'💸 <b>Ціна: {price:,}$</b>\n'
                                         f'💰 <b>Ринкова капіталізація: {market_cap:,}$</b>\n'
                                         f'⏱ <b>24-годинний обсяг: {volume:,}$</b>',
                                         parse_mode = 'HTML',
                                         reply_markup = builder.as_markup())
    except:
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())