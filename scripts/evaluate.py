import sklearn.metrics as metrics
from os.path import join as join

if __name__ == '__main__':
    sample_paths = [f'/sbgenomics/project-files/data_{i}.csv' for i in range(1, 5)]
    report_df = pd.DataFrame(columns=['dataset', 'metric', 'method', 'score'])

    folder = 'agl_scipy'

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

                path = join(folder, f'{sample_path}/{distance}_{method}')
                lbl_path = join(path, f'{sample_path}_{distance}_{method}.csv')

                df_labels = pd.read_csv(lbl_path)
                df_labels = df_labels.drop('Unnamed: 0', axis=1)

                score = metrics.silhouette_score(df, df_labels['labels'], metric=distance)
                
                report_df = report_df.append(
                    { 'dataset': sample_path, 'metric': distance, 'method': method, 'score': score}, 
                    ignore_index=True
                )
                print(f'\t\t Score: {score}')
            
    #         break
                
        print('Done!')
        print('-------------------------------------------------\n')  
        
    #     break
    report_df.to_csv('report.csv')