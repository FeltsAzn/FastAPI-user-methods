import uvicorn
from fastapi import FastAPI, Query, Path, Body

from schemas import Worker, Superiors, Clients, ClientOut

app = FastAPI()


@app.get('/')
def home():
    return 'Homepage'


@app.post('/clients', response_model=ClientOut, response_model_exclude_unset=True, response_model_exclude={"age"})
def get_all_clients_info(item: Clients):
    """
    response_model=Class - Для отображения информации о том, какой ответ от сервера мы ожидаем,

    response_model_exclude_unset=True - Для сокрытия необязательных параметров,

    response_model_exclude={"parameter", ...} - Убрать отображение некоторых заданных параметров, которые
    не нужны в ответе от сервера.

    response_model_include={"parameter", ...} - Выбрать отображение некоторых заданных параметров, которые
    требуются в ответе от сервера.



    ВАЖНО: при задания модели отображения данных их нужно возвращать только в том виде, которые они
    представлены в самом классе без доп.параметров или каких-либо преобразований. Либо, модернизируется
    возврат значения таким образом, чтобы он совпадал с серверным ответом.
    """
    return ClientOut(**item.dict(), id=10)  # Преобразуем в словарь Json ответ, распаковываем
    # и отправляем в модернизированный класс


@app.post('/worker')
def create_worker(item: Worker, quentity: int, superiors: str = Body(...)):
    """ Для передачи наших параметров в тело запроса - используем метод Body,
    что помагает нам в формировании нужного нам вида в request-body. Таким образом,
    данные параметры не учитываются в url-parameters, а передаются только в теле запроса
    """
    return {'item': item, 'superiors': superiors, 'quentity': quentity}


@app.post('/superior')
def post_superior(item: Superiors = Body(..., embed=True)):
    """Используем метод Body(..., embed=True) для отображения ключа в нашем теле запроса"""
    return {'item': item}


@app.get('/workers_items', response_model_exclude_defaults=True)
def worker_items(q: list[str] = Query('start', max_length=10, min_length=2, description='kek')) -> Query:
    """
    Query - параметры в запросе '?параметр=значение', можно задавать ограничение,
    базовое значение и объявлять этот запрос устаревшим.
    Параметры 'max_length' и 'min_length' относятся к строковому типу данных
    Для числовых параметров такие как int или float - используется: 'gt' - минимальное значение
    и 'le' - максимальное значение
    """
    return q


@app.get('/worker/{pk}')
def get_single_worker(pk: int = Path(..., gt=1, le=20)):
    """
    Path - дополнительные параметры проверки для нашего запроса (минимальное значение, максимальное значение)
    Конструкция '...' означает pass, но в отличии от pass, '...' можно передавать как параметр
    Так же дополнительные параметры в Path 'gt' - минимальное значение и 'le' - максимальное значение,
    работают целочисленные параметры (int)
    """
    return {'pk': pk}


if __name__ == '__main__':
    uvicorn.run(app, reload=True)

