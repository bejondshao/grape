def calculate_turnover(collection, code):
    print("Calculate turnover. Code: " + code)

    stock_hist = collection.find(
        {'code': code},
        {'_id': 1,
         'code': 1,
         'date': 1,
         'close': 1}
    ).sort([('date', 1)])