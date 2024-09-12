# 1. 배경 : 흰색 책상, 우드 테이블
# 2. 데이터 증식 조건
#    2-0. 스마트폰으로 사진 촬영 후 이미지 크기를 줄여주자.
#         대상물 촬영을 어떻게 해야할지 확인
#    2-1. 회전(10~30도) 범위 안에서 어느 정도 각도를 넣어야 인식이 잘 되는가?
#    2-2. hflip, vflip : 이 기능이 도움이 되는가?(물체별로 필요 없을 수 있음) 넣을 것인가?
#    2-3. resize, crop : 가능하면 적용해 보자.
#    2-4. 파일명을 다르게 저장 cf) jelly_wood.jpg, jelly_white.jpg
#         jelly_wood_rot_15.jpg, jelly_wood_hflip.jpg, jelly_wood_resize.jpg 등...
#    2-5. 클래스 별로 폴더를 생성
#    2-6. 데이터를 어떻게 넣느냐에 따라 어떻게 동작되는지 1-2줄로 요약
# (+) 그 밖에 원하는 기능들 자유롭게 추가해보기


# 프로그램 구성 순서
# 1. 촬영한다
# 2. 이미지를 컴퓨터로 복사, resize한다
# 3. 육안으로 확인, 이렇게 사용해도 되는가?
# 4. 함수들을 만든다. resize, rotate, hflip, vflip, crop,
#    원본 파일명을 읽어서 파일 명을 생성하는 기능은 모든 함수에 있어야 한다.(함수)
# 5. 단일 함수들 검증 (함수마다 구현ㅇ)
# 6. 함수를 활용해서 기능 구현
# 7. 테스트(경우의수 모두 검토)
# 8. 데이터셋을 teachable machine 사이트에 올려서 테스트
# 9. 인식이 잘 되는 케이스를 분석하고 케이스 추가, 1~8에서 구현된 기능을 이용


import cv2
import numpy as np
import os


# 이미지 크기 적절히 resize하는 함수
def resize_image(image, width, height, output_path):
    resized_img = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    print(f"Saving resized image to: {output_path}")
    cv2.imwrite(output_path, resized_img)
    return resized_img

# 이미지 Rotate 함수
def rotate_image(image, angle, output_path):
    if angle == 90:
        rotated_img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) # 시계방향으로 90도 회전
    elif angle == 180:
        rotated_img = cv2.rotate(image, cv2.ROTATE_180) # 180도 회전
    elif angle == 270:
        rotated_img = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE) # 반시계방향으로 90도 회전
    else: # 30도와 같은 임의의 각도 회전
        print("지원하지 않는 회전 각도입니다.", angle)
        return image
    print(f"Saving rotated image (angle {angle}) to: {output_path}")
    cv2.imwrite(output_path, rotated_img)
    return rotated_img

# 이미지 flip (horizontal / vertical) 함수
def flip_image(image, direction, output_path):
    if direction == 'horizontal':
        flipped_img = cv2.flip(image, 1) # 좌우 대칭
    elif direction == 'vertical':
        flipped_img = cv2.flip(image, 0) # 상하 대칭
    else:
        print("지원하지 않는 방향입니다.")
        return image
    print(f"Saving flipped image to: {output_path}")
    cv2.imwrite(output_path, flipped_img)
    return flipped_img

# 이미지 crop 함수
def crop_image(image, start_row, end_row, start_col, end_col, output_path):
    cropped_img = image[start_row:end_row, start_col:end_col]
    print(f"Saving cropped image to: {output_path}")
    cv2.imwrite(output_path, cropped_img)
    return cropped_img

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"Creating folder: {folder_path}")
        os.makedirs(folder_path)

# 파일명에서 확장자를 분리하고 새로운 파일명을 만드는 함수
def modify_filename(folder, filename, suffix):
    base_name, ext = os.path.splitext(filename)
    new_filename = base_name + suffix + ext
    return os.path.join(folder, new_filename)


# 메인 함수 - 실행해보기
if __name__ == '__main__':
    dataPath = os.path.join(os.getcwd(), 'dataAug')
    dataOrg = os.path.join(dataPath, 'org')
    dataProcessed = os.path.join(dataPath, 'processed')
    
    # 기능별 폴더 경로 설정
    resize_folder = os.path.join(dataProcessed, 'resize')
    rotate_folder = os.path.join(dataProcessed, 'rotate')
    flip_folder = os.path.join(dataProcessed, 'flip')
    crop_folder = os.path.join(dataProcessed, 'crop')
    
    # 기능별 폴더 생성
    create_folder_if_not_exists(resize_folder)
    create_folder_if_not_exists(rotate_folder)
    create_folder_if_not_exists(flip_folder)
    create_folder_if_not_exists(crop_folder)
    
    # 원하는 사진 받아와서 실행해보기
    fileName = 'silver_black_1.jpg'
    filePath = os.path.join(dataOrg, fileName)
    img = cv2.imread(filePath)
    
    # resize 이미지
    resize_output = modify_filename(resize_folder, fileName, '_resize')
    img_resize = resize_image(img, 300, 400, resize_output)
    cv2.imshow('resize', img_resize)
    
    # rotate 이미지
    rotate_output_90 = modify_filename(rotate_folder, fileName, '_rot_90')
    rotate_output_180 = modify_filename(rotate_folder, fileName, '_rot_180')
    rotate_output_270 = modify_filename(rotate_folder, fileName, '_rot_270')
    
    img_rot_90 = rotate_image(img_resize, 90, rotate_output_90)
    img_rot_180 = rotate_image(img_resize, 180, rotate_output_180)
    img_rot_270 = rotate_image(img_resize, 270, rotate_output_270)
    
    cv2.imshow('rotate90', img_rot_90)
    cv2.imshow('rotate180', img_rot_180)
    cv2.imshow('rotate270', img_rot_270)
    
    # flip 이미지
    flip_output = modify_filename(flip_folder, fileName, '_hflip')
    img_hflip = flip_image(img_resize, 'horizontal', flip_output)
    
    flip_output = modify_filename(flip_folder, fileName, '_vflip')
    img_vflip = flip_image(img_resize, 'vertical', flip_output)
    
    cv2.imshow('h_flip', img_hflip)
    cv2.imshow('v_flip', img_vflip)
    
    # crop 이미지
    crop_output = modify_filename(crop_folder, fileName, '_crop')
    img_crop = crop_image(img_resize, 50, 150, 20, 200, crop_output)
    cv2.imshow("crop", img_crop)

cv2.waitKey()
cv2.destroyAllWindows()