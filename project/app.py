import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Фиксированный курс обмена: 1 доллар = 0.00027 ETH
FIXED_ETH_TO_USD_RATE = 0.00027
API_URL = 'https://api.qrserver.com/v1/create-qr-code/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    # Логика для отображения деталей проекта
    return render_template('project_detail.html', project_id=project_id)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help/animals')
def help_animals():
    animals = [
        {"name": "Кошка Луна", "image": "cat-1.jpg", "description": "Луна нуждается в вашей помощи, чтобы найти новый дом, где её будут любить и заботиться о ней. На улице она столкнулась с множеством трудностей: нехватка пищи, постоянный стресс и опасности, связанные с погодными условиями и другими животными. У Лунны также есть небольшой дефект на лапке, который требует ветеринарного осмотра и, возможно, лечения."},
        {"name": "Щенок Барбос", "image": "dog-1.jpg", "description": "Барбос попал к нам после того, как его нашли на улице в холодный зимний день. Он был напуган и голоден, но, несмотря на это, сразу начал доверять людям, которые его спасли. Барбосу требуется ваша помощь, чтобы найти любящую семью, которая сможет подарить ему тепло и заботу, которых он заслуживает."},
        {"name": "Кот Малыш", "image": "cat-2.png", "description": "Малыш был найден на улице, где он одиноко бродил в поисках еды и тепла. К счастью, его заметили добрые люди и принесли к нам. Теперь Малышу нужно ваше внимание и поддержка, чтобы он мог вырасти в здорового и счастливого кота. Ваше пожертвование поможет нам обеспечить его всем необходимым: качественным кормом, медицинскими обследованиями и уютным временным домом. "},
        {"name": "Кошка Карамелька", "image": "cat-3.jpg",
         "description": "Карамелька нуждается в вашей помощи, чтобы обрести новый дом, где её будут всегда любить и заботиться о ней. На улице она столкнулась со многими трудностей: нехватка пищи, постоянный стресс и опасности, связанные с погодными условиями и другими животными. У Лунны также есть небольшой дефект на лапке, который требует ветеринарного осмотра и, возможно, лечения."},
        {"name": "Щенок Пират", "image": "dog-2.jpg",
         "description": "Пират попал к нам после того, как его нашли на улице пол года назад. Он был напуган и истощен, но, несмотря на это, сразу начал доверять людям, которые его спасли. Пирату требуется ваша помощь, чтобы найти любящую семью, которая сможет подарить ему тепло и заботу, чего заслуживаем каждое живое существо."},
        {"name": "Кот Дантес ", "image": "cat-4.jpg",
         "description": " был найден на улице, где он одиноко бродил в поисках еды и тепла. К счастью, его заметили добрые люди и принесли к нам. Теперь Малышу нужно ваше внимание и поддержка, чтобы он мог вырасти в здорового и счастливого кота. Ваше пожертвование поможет нам обеспечить его всем необходимым: качественным кормом, медицинскими обследованиями и уютным временным домом. "},
    ]
    return render_template('help.html', title='Помощь животным', items=animals)

@app.route('/help/people')
def help_people():
    people = [
        {"name": "Хуан Мартинес", "image": "person-1.jpg", "description": "Иван борется с тяжелым заболеванием и нуждается в лечении."},
        {"name": "Лейла Хасан", "image": "person-2.jpg", "description": "Мария потеряла крышу над головой из-за стихийного бедствия."},
        {"name": "Карлос Сантос", "image": "person-3.jpg", "description": "Иван борется с тяжелым заболеванием и нуждается в лечении."},
        {"name": "Юрий Новак", "image": "person-4.jpg", "description": "Иван борется с тяжелым заболеванием и нуждается в лечении."},
        {"name": "Роберт Вильямс", "image": "person-5.jpg", "description": "Иван борется с тяжелым заболеванием и нуждается в лечении."},
        {"name": "Давид Моралес", "image": "person-6.jpg", "description": "Иван борется с тяжелым заболеванием и нуждается в лечении."}
    ]
    return render_template('help.html', title='Помощь людям', items=people)

@app.route('/donate/<string:recipient>', methods=['GET', 'POST'])
def donate(recipient):
    if request.method == 'POST':
        try:
            amount_in_usd = float(request.form['amount'])
            amount_in_eth = amount_in_usd * FIXED_ETH_TO_USD_RATE
            amount_in_wei = int(amount_in_eth * 1e18)  # Конвертация в wei

            ethereum_address = "0x1234567890abcdef1234567890abcdef12345678"  # Замените на ваш адрес Ethereum

            # Формируем диплинк для Metamask
            ethereum_uri = f"ethereum:{ethereum_address}?value={amount_in_wei}"

            # Генерируем QR-код на основе диплинка
            params = {
                'data': ethereum_uri,
                'size': '200x200',  # Размер QR-кода
            }
            response = requests.get(API_URL, params=params)
            qr_code_url = response.url

            return render_template('donate.html', recipient=recipient, ethereum_address=ethereum_address, amount_in_usd=amount_in_usd, amount_in_eth=amount_in_eth, qr_code_url=qr_code_url)

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return "Произошла ошибка при обработке вашего запроса."

    return render_template('donate_form.html', recipient=recipient)

if __name__ == '__main__':
    app.run(debug=True)























