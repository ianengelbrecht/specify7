import { stringify } from 'csv-stringify/browser/esm';

import { downloadFile } from '../Molecules/FilePicker';
import { getUserPref } from '../UserPreferences/helpers';
import type { Dataset } from '../WbPlanView/Wrapped';

export const downloadDataSet = async ({
  name,
  rows,
  columns,
}: Dataset): Promise<void> =>
  new Promise((resolve, reject) =>
    stringify(
      [columns, ...rows],
      {
        delimiter: getUserPref('workBench', 'editor', 'exportFileDelimiter'),
      },
      (error, output) => {
        if (error === undefined)
          resolve(
            downloadFile(name.endsWith('.csv') ? name : `${name}.tsv`, output)
          );
        else reject(error);
      }
    )
  );
