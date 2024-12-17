from PIL import Image
from masks import bbb_mask, bbw_mask, bwb_mask, bww_mask, wbb_mask, wbw_mask, wwb_mask, www_mask, work_matrix 

def process_image(image_path): 
    try:
        img = Image.open(image_path).convert("L")
        width, height = img.size

        if width != 1600 or height != 1600:
            print("Размер изображения должен быть 1600*1600 пикселей")
            return None

        x_start = 128
        y_start = 128
        x_end = 1472
        y_end = 1472

        cropped_img = img.crop((x_start, y_start, x_end, y_end)) 

        square_size = 1344 // 21  
        result_matrix = []

        for i in range(21):
            row = []
            for j in range(21):
                x1 = j * square_size
                y1 = i * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                cropped_square = cropped_img.crop((x1, y1, x2, y2))
                black_pixels = 0
                white_pixels = 0
                for pixel in cropped_square.getdata():
                    if pixel < 128:
                        black_pixels += 1
                    else:
                        white_pixels += 1

                if black_pixels > white_pixels:
                    row.append(1)
                else:
                    row.append(0)
            result_matrix.append(row)

        return result_matrix

    except FileNotFoundError:
        print("Файл изображения не найден")
        return None
    except Exception as e:
        print("Произошла ошибка")
        return None


image_path = input('Введите адрес изображения ')
result = process_image(image_path)



def apply_mask(result, work_matrix):
    mask_mapping = {
        (1, 1, 1): bbb_mask,
        (1, 1, 0): bbw_mask,
        (1, 0, 1): bwb_mask,
        (1, 0, 0): bww_mask,
        (0, 1, 1): wbb_mask,
        (0, 1, 0): wbw_mask,
        (0, 0, 1): wwb_mask,
        (0, 0, 0): www_mask
    }

    mask_key = (result[8][2], result[8][3], result[8][4])
    
    if mask_key in mask_mapping:
        selected_mask = mask_mapping[mask_key]
        for i in range(21):
            for j in range(21):
                work_matrix[i][j] = result[i][j] ^ selected_mask[i][j]
    else:
        print('Ошибка, такой комбинации нет')
    return work_matrix


work_matrix = apply_mask(result, work_matrix)

lenght_message = [work_matrix[18][20], work_matrix[18][19],work_matrix[17][20],work_matrix[17][19],work_matrix[16][20],work_matrix[16][19],work_matrix[15][20],work_matrix[15][19]]
lenght_str = ''.join(map(str, lenght_message))
lenght_value = int(lenght_str, 2)  


def decode_message(work_matrix):
    message_coords = [
        # 1 блок
        [(14, 20), (14, 19), (13, 20), (13, 19), (12, 20), (12, 19), (11, 20), (11, 19)],
        # 2 блок 
        [(10, 20), (10, 19), (9, 20), (9, 19), (9, 18), (9, 17), (10, 18), (10, 17)],
        # 3 блок
        [(11, 18), (11, 17), (12, 18), (12, 17), (13, 18), (13, 17), (14, 18), (14, 17)],
        # 4 блок
        [(15, 18), (15, 17), (16, 18), (16, 17), (17, 18), (17, 17), (18, 18), (18, 17)],
        # 5 блок
        [(19, 18), (19, 17), (20, 18), (20, 17), (20, 16), (20, 15), (19, 16), (19, 15)],
        # 6 блок
        [(18, 16), (18, 15), (17, 16), (17, 15), (16, 16), (16, 15), (15, 16), (15, 15)],
        # 7 блок
        [(14, 16), (14, 15), (13, 16), (13, 15), (12, 16), (12, 15), (11, 16), (11, 15)],
        # 8 блок
        [(10, 16), (10, 15), (9, 16), (9, 15), (9, 14), (9, 13), (10, 14), (10, 13)],
        # 9 блок
        [(11, 14), (11, 13), (12, 14), (12, 13), (13, 14), (13, 13), (14, 14), (14, 13)],
         # 10 блок
        [(15, 14), (15, 13), (16, 14), (16, 13), (17, 14), (17, 13), (18, 14), (18, 13)],
        # 11 блок
        [(19, 14), (19, 13), (20, 14), (20, 13), (20, 12), (20, 11), (19, 12), (19, 11)],
        # 12 блок
        [(18, 12), (18, 11), (17, 12), (17, 11), (16, 12), (16, 11), (15, 12), (15, 11)],
        # 13 блок
         [(14, 12), (14, 11), (13, 12), (13, 11), (12, 12), (12, 11), (11, 12), (11, 11)],
        # 14 блок
        [(10, 12), (10, 11), (9, 12), (9, 11), (8, 12), (8, 11), (7, 12), (7, 11)],
         # 15 блок
        [(5, 12), (5, 11), (4, 12), (4, 11), (3, 12), (3, 11), (2, 12), (2, 11)],
        # 16 блок
        [(1, 12), (1, 11), (0, 12), (0, 11), (0, 10), (0, 9), (1, 10), (1, 9)],
        # 17 блок
         [(2, 10), (2, 9), (3, 10), (3, 9), (4, 10), (4, 9), (5, 10), (5, 9)]
    ]

    decoded_message = []
    for coords in message_coords:
        element_message = [work_matrix[row][col] for row, col in coords]
        element_str = ''.join(map(str, element_message))
        element_value = chr(int(element_str, 2))
        decoded_message.append(element_value)

    return ''.join(decoded_message)  


decoded_message = decode_message(work_matrix)[:lenght_value]
print('Декодированное сообщение: ', decoded_message)



