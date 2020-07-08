import sklearn.metrics as metrics
from os.path import join as join
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_path', help='Absolute path for samples files')
    parser.add_argument('--labels_folder', help='Absolute path for folder where to find labels')
    parser.add_argument('--save_path', help='Absolute path for saving report csv')
    args = parser.parse_args()

    sample_paths = [f'{args.samples_path}/data_{i}.csv' for i in range(1, 5)]
    report_df = pd.DataFrame(columns=['dataset', 'metric', 'method', 'score'])

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        sample_path = f'data_{i+1}'
        print(f'{sample_path}')

        for distance in ['cosine', 'jaccard']:
            print(f'\t {distance}')

            for method in ['average', 'ward']:
                print(f'\t\t {method}')

                path = join(args.labels_folder, f'{sample_path}/{distance}_{method}')
                lbl_path = join(path, f'{sample_path}_{distance}_{method}.csv')

                df_labels = pd.read_csv(lbl_path)
                df_labels = df_labels.drop('Unnamed: 0', axis=1)

                score = metrics.silhouette_score(df, df_labels['labels'], metric=distance)
                
                report_df = report_df.append(
                    { 'dataset': sample_path, 'metric': distance, 'method': method, 'score': score}, 
                    ignore_index=True
                )
                print(f'\t\t Score: {score}')
                
        print('Done!')
        print('-------------------------------------------------\n')  
        
    report_df.to_csv(args.save_path)

if __name__ == '__main__':
    main()