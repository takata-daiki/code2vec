import glob
from common import common
from extractor import Extractor

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


class InteractivePredictor:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(
            config,
            jar_path=JAR_PATH,
            max_path_length=MAX_PATH_LENGTH,
            max_path_width=MAX_PATH_WIDTH)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    # cusomized function to perform prediction from input files
    def predict(self):
        print(
            'NOTICE: The cusomized version of predict() in interactive_predict.py was called!'
        )
        data_directory = './data/ALDS1_12_C@test/'  # set your own dataset directory to be converted into code vectors.
        input_filenames = sorted(glob.glob(data_directory + '*.java'))

        for input_filename in input_filenames:
            print(input_filename)
            try:
                predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(
                    input_filename)
            except ValueError as e:
                print(e)
            results, code_vectors = self.model.predict(predict_lines)
            prediction_results = common.parse_results(
                results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)

            f_out = input_filename + '.txt'
            with open(f_out, 'w') as f:
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
                        f.write(method_prediction.original_name + ',' + cv +
                                '\n')
