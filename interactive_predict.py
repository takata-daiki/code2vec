from pathlib import Path
from common import common
from extractor import Extractor

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'

ROOT_PATH = Path('/Users/daiki-tak/GitHub/ojcode-metric-extractor/data/aoj/0089@test')
SRC_PATH = ROOT_PATH / 'tmp'
DST_PATH = ROOT_PATH / 'codevec'


class InteractivePredictor:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model, ipath=SRC_PATH, opath=DST_PATH):
        global SRC_PATH, DST_PATH
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(
            config,
            jar_path=JAR_PATH,
            max_path_length=MAX_PATH_LENGTH,
            max_path_width=MAX_PATH_WIDTH)
        SRC_PATH = Path(ipath)
        DST_PATH = Path(opath)
        print('---')
        print(f'SRC_PATH={ipath}')
        print(f'DST_PATH={opath}')

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    # cusomized function to perform prediction from input files
    def predict(self):
        print(
            'NOTICE: The cusomized version of predict() in interactive_predict.py was called!'
        )

        input_filenames = [SRC_PATH]
        if not SRC_PATH.match('*.java'):
            input_filenames = sorted(SRC_PATH.glob('*.java'))

        for input_filename in input_filenames:
            print(input_filename)
            try:
                predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(
                    input_filename.as_posix())
            except ValueError as e:
                print(e)
                continue
            results, code_vectors = self.model.predict(predict_lines)
            prediction_results = common.parse_results(
                results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)

            f_out = DST_PATH
            if not DST_PATH.match('*.txt'):
                DST_PATH.mkdir(parents=True, exist_ok=True)
                f_out = DST_PATH / f'{input_filename.stem}.txt'

            with f_out.open(mode='w') as f:
                for i, method_prediction in enumerate(prediction_results):
                    print('Original name:\t' + method_prediction.original_name)
                    #  for name_prob_pair in method_prediction.predictions:
                    #      print('\t(%f) predicted: %s' % (
                    #          name_prob_pair['probability'], name_prob_pair['name']))
                    #  print('Attention:')
                    #  for attention_obj in method_prediction.attention_paths:
                    #      print('%f\tcontext: %s,%s,%s' %
                    #            (attention_obj['score'], attention_obj['token1'],
                    #             attention_obj['path'], attention_obj['token2']))
                    if self.config.EXPORT_CODE_VECTORS:
                        cv = ' '.join(map(str, code_vectors[i]))
                        print('Code vector:')
                        print(cv)
                        # write code vector in text files
                        f.write('{},{}\n'.format(
                            method_prediction.original_name, cv))
