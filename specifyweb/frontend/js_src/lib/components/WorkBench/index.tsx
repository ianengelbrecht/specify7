import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { useAsyncState } from '../../hooks/useAsyncState';
import { useBooleanState } from '../../hooks/useBooleanState';
import { useErrorContext } from '../../hooks/useErrorContext';
import { commonText } from '../../localization/common';
import { wbText } from '../../localization/workbench';
import { ajax } from '../../utils/ajax';
import { f } from '../../utils/functools';
import type { GetSet } from '../../utils/types';
import { LoadingContext } from '../Core/Contexts';
import { useMenuItem } from '../Header/MenuContext';
import { treeRanksPromise } from '../InitialContext/treeRanks';
import { LoadingScreen } from '../Molecules/Dialog';
import { Dialog } from '../Molecules/Dialog';
import { NotFoundView } from '../Router/NotFoundView';
import type { Dataset } from '../WbPlanView/Wrapped';
import { WbView } from './WbView';

export function WorkBench(): JSX.Element {
  useMenuItem('workBench');

  const [treeRanksLoaded = false] = useAsyncState(fetchTreeRanks, true);
  const { id } = useParams();
  const datasetId = f.parseInt(id);

  const [dataset, setDataset] = useDataset(datasetId);
  useErrorContext('dataSet', dataset);
  const loading = React.useContext(LoadingContext);

  const [isDeleted, handleDeleted] = useBooleanState();
  // @ts-expect-error figure out how handleDeletedConfirmation was being used in Backbone. possibly not used at all
  const [isDeletedConfirmation, handleDeletedConfirmation] = useBooleanState();

  const navigate = useNavigate();

  if (dataset === undefined || !treeRanksLoaded) return <LoadingScreen />;

  const triggerDatasetRefresh = () => {
    loading(fetchDataset(dataset.id).then(setDataset));
  };

  return datasetId === undefined ? (
    <NotFoundView />
  ) : isDeleted ? (
    <>{wbText.dataSetDeletedOrNotFound()}</>
  ) : isDeletedConfirmation ? (
    <Dialog
      buttons={commonText.close()}
      header={wbText.dataSetDeleted()}
      onClose={(): void => navigate('/specify/', { replace: true })}
    >
      {wbText.dataSetDeletedDescription()}
    </Dialog>
  ) : (
    <WbView
      dataset={dataset}
      key={dataset.id}
      triggerDatasetRefresh={triggerDatasetRefresh}
      onDatasetDeleted={handleDeleted}
    />
  );
}

const fetchTreeRanks = async (): Promise<true> => treeRanksPromise.then(f.true);

// BUG: intercept 403 (if dataset has been transferred to another user)
function useDataset(
  datasetId: number | undefined
): GetSet<Dataset | undefined> {
  return useAsyncState(
    React.useCallback(
      async () =>
        typeof datasetId === 'number' ? fetchDataset(datasetId) : undefined,
      [datasetId]
    ),
    true
  );
}

const fetchDataset = async (datasetId: number): Promise<Dataset> =>
  ajax<Dataset>(`/api/workbench/dataset/${datasetId}/`, {
    headers: { Accept: 'application/json' },
  }).then(({ data }) => data);
