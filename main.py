import cv2
import imageio
import os
import natsort
import shutil
from PIL import Image
from PIL import ImageFilter
from datetime import datetime


def movie_to_image(
    video_name: str, image_folder: str, DROP_COUNT_MAX: int, END_FRAME: int
) -> None:
    """
    영상을 이미지로 만들어줍니다.
    Args:
        video_name (str) : 비디오 경로를 지정합니다.
        image_folder (str) : 비디오에서 변환된 이미지를 저장하는 폴더 경로를 지정합니다.
        DROP_COUNT_MAX (int) : 동영상 앞에 버릴 부분을 지정합니다.
        END_FRAME (int) : 동영상 끝에 버릴 부분을 지정합니다.
    Return
        None
    """
    vidcap = cv2.VideoCapture(video_name)
    FRAME_MAX = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    FILE_NAME_COUNT = 0
    FRAME_COUNT = 0
    if DROP_COUNT_MAX < END_FRAME:
        try:
            while vidcap.isOpened():
                ret, image = vidcap.read()
                FRAME_COUNT += 1
                if FRAME_COUNT > DROP_COUNT_MAX:
                    if int(vidcap.get(1)) % 3 == 0:
                        cv2.imwrite(
                            "{}/{}_frame.png".format(image_folder, FILE_NAME_COUNT),
                            image,
                        )
                        FILE_NAME_COUNT += 1
                    if FRAME_MAX == FRAME_COUNT or END_FRAME == FRAME_COUNT:
                        vidcap.release()
        except Exception as e:
            print(e)

    else:
        print("DROP_COUNT_MAX > END_FRAME")


def makeGif(image_folder: str) -> None:
    """
    지정된 이미지 폴더를 GIF로 만들어줍니다.
    Args:
        image_folder (str) : GIF로 만들어줄 이미지 폴더를 지정합니다.
    Return
        None
    """
    path = ["{}/{}".format(image_folder, i) for i in os.listdir(image_folder)]
    path.sort()
    path = natsort.natsorted(path)
    paths = [Image.open(i) for i in path]
    current_dateTime = datetime.now()
    str_now = current_dateTime.strftime("%Y년%m월%d일_%H시%M분%S초")
    imageio.mimsave("result/{}.gif".format(str_now), paths, fps=12)


def counting_max_frame(video_name: str) -> int:
    """
    비디오의 최대 프레임수를 계산합니다.
    Args:
        video_name (str) : 비디오의 경로를 지정합니다.
    Return
        FRAME_MAX (int) : 영상의 최대프레임 수
    """
    vidcap = cv2.VideoCapture(video_name)
    FRAME_MAX = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    return FRAME_MAX


# 사진 사이즈 조절 기능
def filter(
    image_sample_show: bool = True,
    filter: bool = False,
    image_folder: str = "./assets/image",
) -> None:
    """
    사진의 사이즈를 조절하고 필터를 합니다.
    Args:
        image_sample_show (bool) : 샘플유무를 지정합니다.
        filter (bool) : 필터유무를 지정합니다.
        image_folder (str) : gif로 만들 이미지의 폴더경로를 지정합니다.
    Return
        None
    """
    if image_sample_show:
        image1 = Image.open("assets/image/0_frame.png")

        # 이미지의 크기 출력
        print(image1.size)
        croppedImage = image1.crop((0, 0, 504, 540))
        croppedImage.show()
    if filter:
        path = ["{}/{}".format(image_folder, i) for i in os.listdir(image_folder)]
        paths = [Image.open(i) for i in path]
        # crop_images = [i.filter(ImageFilter.SMOOTH_MORE) for i in paths]
        crop_images = [i.filter(ImageFilter.DETAIL) for i in paths]
        # crop_images = [i.filter(ImageFilter.FIND_EDGES) for i in paths]
        # crop_images = [i.filter(ImageFilter.EDGE_ENHANCE_MORE) for i in paths]
        crop_images = [i.crop((0, 0, 504, 540)) for i in crop_images]

        for pth, image in zip(path, crop_images):
            image.save(pth)


def reset(image_folder: str) -> None:
    """
    이미지 폴더를 삭제하고 다시 작성합니다.
    Args:
        image_folder (str) : 비워낼 이미지 폴더를 지정합니다.
    Return
        None
    """
    shutil.rmtree(image_folder)
    os.mkdir(image_folder)


def main():
    # gif로 쓰일 이미지 폴더지정 및 비디오 설정
    image_folder = "./assets/image"
    video_name = "./assets/movie/Test01.mp4"

    # 프레임 시작 끝 조절
    START_FRAME = 10
    END_FRAME = counting_max_frame(video_name)

    # 이전에 했던 작업 지우기
    reset(image_folder)

    # 영상에서 사진 가져오기
    movie_to_image(video_name, image_folder, START_FRAME, END_FRAME)

    # 사진 사이즈, 필터를 통한 후보정
    filter(False, True)

    # GIF생성
    makeGif(image_folder)


main()
