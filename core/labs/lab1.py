from tqdm import tqdm
from core.labs.titles import LAB1
from core.math.resampling import resampling
from core.math.halftoning import halftone
from core.math.thresholding import kristian_threshold
from PIL import Image
from core.labs.lab import Lab
import os

class Lab1(Lab):

    input_path: str = ''
    output_path: str = 'LAB1' # рабочий каталог
    filelist: list = []

    result_dir = 'results' # каталог для сохранения выходных изображений
    report_path = 'README.md' # путь к отчету

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = os.path.join(output_path, self.output_path)
        self.report_path = os.path.join(self.output_path, self.report_path)
        self.result_dir = os.path.join(self.output_path, self.result_dir)

        self.first_step_resampling_path = os.path.join(self.result_dir, 'resampling')
        self.first_step_two_step_resampling_path = os.path.join(self.result_dir, 'two_step_resampling')
        self.first_step_down_path = os.path.join(self.result_dir, 'downsampling')
        self.first_step_up_path = os.path.join(self.result_dir, 'upsampling')
        
        self.second_step_halftone_path = os.path.join(self.result_dir, 'halftoning')

        self.third_step_path = os.path.join(self.result_dir, 'thresholding')

        super().create_dirs([
            self.result_dir, 
            self.first_step_resampling_path,
            self.first_step_two_step_resampling_path,
            self.first_step_down_path,
            self.first_step_up_path,
            self.second_step_halftone_path,
            self.third_step_path,
            ])

        self.filelist = super().get_files(self.input_path)
        
    def run(self):
        self.first_step()
        self.second_step()
        self.third_step()
    
    def gen_report(self, student_name):
        super().gen_report(self.report_path, LAB1, 1, student_name)
        
    def first_step(self):
        title = "### 1. Передисретизация"
        with open(self.report_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{title}\n")
            for file in tqdm(self.filelist, ascii=True, desc=title):
                filename = file.split('\\')[-1]
                original = Image.open(file)

                downsample_image_path = os.path.join(self.first_step_down_path, filename)
                downsample_image = resampling(original, 1/2)
                downsample_image.save(downsample_image_path)

                upsample_image_path = os.path.join(self.first_step_up_path, filename)
                upsample_image = resampling(original, 3)
                upsample_image.save(upsample_image_path)
                
                resample_image_path = os.path.join(self.first_step_resampling_path, filename)
                resample_image = resampling(original, 3/2)
                resample_image.save(resample_image_path)

                two_step_resample_image_path = os.path.join(self.first_step_two_step_resampling_path, filename)
                two_step_resample_image = resampling(upsample_image, 1/2)
                two_step_resample_image.save(two_step_resample_image_path)

                f.write(f'''
Исходное изображение :

![Original]({file})

Интерполяция в 3 раза.

![UpsamplingX3]({upsample_image_path})

Децимация в 2 раза.

![DownsamplingX2]({downsample_image_path})

Передискретизация изображения в K=3/2 за два прохода.

![Resampling2loop]({two_step_resample_image_path})

Передискретизация изображения в K=3/2 за один проход.

![Resampling1loop]({resample_image_path})
''')

    def second_step(self):
        title = "### 2. Приведение полноцветного изображения к полутоновому"
        with open(self.report_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{title}\n")
            for file in tqdm(self.filelist, ascii=True, desc=title):
                filename = file.split('\\')[-1]
                original = Image.open(file)
                halftoning_image_path = os.path.join(self.second_step_halftone_path, filename)
                halftoning = halftone(original)
                halftoning.save(halftoning_image_path)

                f.write(
f'''
Исходное изображение :

![Original]({file})

Результирующее изображение :

![Semitone]({halftoning_image_path})
''')

    def third_step(self):
        title = "### 3. Приведение полутонового изображения к монохромному методом пороговой обработки"
        B = [20, 40, 80]
        K = [0.2, .6, 0.8]
        with open(self.report_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{title}\n")
            for file in tqdm(self.filelist, ascii=True, desc=title):
                filename = file.split('\\')[-1]
                original = Image.open(file)

                halftoning = halftone(original)
                f.write('''
Исходное изображение :

![Original]({file})''')
                for b, k in [(b, k) for b in B for k in K]:
                    threshold_image_path = os.path.join(self.third_step_path, f"b{b}_k{k}_{filename}")
                    threshold_image = kristian_threshold(image=halftoning, b=b, k=k)
                    threshold_image.save(threshold_image_path)

                    f.write(f'''
B = {b}, K = {k} : 

![thresholding{b}x{k}]({threshold_image_path})
''')

                